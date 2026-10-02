/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_nvm_port.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/02 §8,
//                07 §5; F02.8 handshake, F07.8 record framing)
//
//  Description : Class-F NVM port — the seam between the record producers
//                behind KL_pp_nvm_mgr_arb (07 §5.3: binding manager, D3 writer)
//                and the physical NVM device behind the side-port/management
//                processor (01 §2: "NVM physical device (behind the NVM
//                port)"). Record-level and device-agnostic per 02 §8: the
//                MANAGER face carries exactly the F02.8 envelope
//                {req, we, record_id[8], streamed bytes, busy/done/err};
//                the DEVICE face is the backing contract 02 §8 leaves free,
//                shaped here as a region port {req/grant, op READ / WRITE /
//                ERASE_REGION, region id + byte offset + length, byte-stream
//                data phases, busy/done/err}. Integrity is IN-BAND (07 §5.2):
//                the framing {magic 0x1722, layout_version, record_id,
//                payload_length, crc16} rides the byte stream; the crc16 is
//                serialized and validated by the MANAGER (07 §5.3), never
//                here. Long device busy periods are expected; commits stay
//                asynchronous to protocol responses (03 §6 ordering rule d)
//                because the port never blocks anything but its own lane.
//
//                The one design decision that matters: the port parses ONLY
//                payload_length (plus magic as a sanity gate) from the
//                in-band header to delimit the byte pump — an unframed or
//                oversize stream cannot be delimited, so it is refused with
//                err BEFORE any device traffic. A commit is ERASE_REGION
//                then WRITE so NOR-flash backends work unmodified (backends
//                without erase semantics answer ERASE with done at once); a
//                restore is a header read (8 B), then a payload read sized
//                by the header. Storage is one 8-byte header lane buffer
//                (flops — deliberately not RAM-shaped); both data phases are
//                pure pass-through. 16-bit header fields ride the byte
//                stream big-endian (network order, as everywhere else in
//                1722.1): magic streams as 0x17 then 0x22.
//
//  Refusals    : (a) req while busy is ignored — single outstanding op
//                (F02.8); (b) a commit stream whose header fails the magic
//                or payload_length bound, or a stored record whose header
//                fails them on restore, ends in a single err pulse with no
//                (further) device traffic. Device err mid-op aborts and
//                surfaces on the manager face exactly once; the bounded
//                retry and the side-port alarm are the manager's job;
//                nvm_err_cause_o names which of the two an err was, so a
//                manager can tell a failing device from a record that is not
//                there (processor issue #93, S1);
//                (c) a dev_done_i observed while this port owns no device
//                command is DISCARDED. 02 §8 leaves the device face free, so
//                the completion contract is stated here: a command is owned
//                from the cycle its grant is observed — that cycle may itself
//                carry the completion, and a completion may land on the same
//                cycle a pump moves its last byte — until the wait state
//                consumes it. Ownership retires at the terminal state, at the
//                next accept and at reset. Outside the window a completion
//                belongs to nobody: remembering one there lets the NEXT wait
//                state short-circuit on it, and a commit then reports done
//                over a region the backend is still erasing;
//                (d) a SHORT command: a completion on an edge that moves no
//                final byte, or one that rode the grant of a command with
//                bytes still to move, ends the operation with one err,
//                cause DEVICE, at once, in all four data phases (the header
//                read always did; processor issue #15).
//
//  Deadline    : (processor issue #15) 02 §8 leaves the device face free,
//                but not silent: the device presents each event it OWES the
//                port within MEM_TIMEOUT_CYC_P owed clocks of the previous
//                one: a grant while a request is up, a byte the port presents
//                or is ready for, a terminal not yet latched once the data
//                phase is over. It owes nothing while the port or the manager
//                holds the operation (header collection and forward, a
//                stalled manager byte), and such a cycle PAUSES the count:
//                only a grant, byte or terminal restarts it, and each
//                operation starts at zero, so a slow device that keeps moving
//                is never refused and no manager handshake pattern holds a
//                silent one off. On the (MEM_TIMEOUT_CYC_P + 1)-th owed cycle
//                without its event the operation ends: one err, cause
//                DEADLINE, never done, busy low at the pulse, MEM_TIMEOUT_CYC_P
//                + 2 clocks after the last restart plus every paused cycle.
//
//                A deadline ends the OPERATION, never the device's command.
//                A command the device accepted and has not ended stays OWED:
//                while it is owed the port requests nothing, takes and
//                discards the bytes of an owed READ, and takes the device's
//                next done or err as that command's end, credited to no
//                operation. A request that arrives meanwhile is accepted and
//                waits for that terminal under the same count: served once
//                the device has ended the abandoned command, one err cause
//                DEADLINE while it stays silent. Nothing is released on
//                time; only the device's own terminal or a reset ends the
//                owed state. An abandoned WRITE whose device waits for its
//                next byte for ever is CONTAINED that way, every later
//                request ending DEADLINE until reset: padding it would close
//                a record whose bytes the manager never supplied, and an
//                abort is an interface this face does not have.
//
//                dev_gnt_i means the device ACCEPTED the command, and it
//                comes at most one cycle after the edge that sampled the
//                request. A backend that registers its grant (the parent's
//                KL_nvm_backend does) can take a request on the very edge a
//                deadline withdraws it, so a grant in the cycle after a
//                deadline in a request state makes that command owed, unless
//                its terminal rides the grant.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_nvm_port #(
    //! largest accepted payload_length in bytes; must be ≤ 65527 so that
    //! dev_len_o = 8 + payload_length always fits 16 bits
    parameter int unsigned MAX_PAYLOAD_P = 1024,
    //! the device-face deadline (banner), in clk_i cycles: class E's
    //! MEM_TIMEOUT_CYC_P (KL_aecp_desc_store, KL_aecp_resp_buf) on class F.
    //! Legal 1 to 2^31 - 1, refused outside at elaboration. 100,000,000 is
    //! 1,000 ms at the F01.5 default P-CLK-HZ of 100 MHz; the top binds
    //! NVM_MEM_TMO_CYC_P = CLK_HZ_P (F01.5 P-NVM-MEM-TMO-CYC, F08.1
    //! T-NVM-PORT-DEADLINE)
    parameter int unsigned MEM_TIMEOUT_CYC_P = 100_000_000,
    //! derived — do not override. Counted at 33 bits so an out-of-range
    //! value still elaborates far enough for the guard to name it: at
    //! 2^32 - 1 the 32-bit sum + 1 wraps to 0
    localparam int unsigned TMO_W_C = (MEM_TIMEOUT_CYC_P < 1) ? 1
                                    : $clog2(33'(MEM_TIMEOUT_CYC_P) + 33'd1)
) (
    input  wire         clk_i,           //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,           //! synchronous active-low reset

    //! ---- manager face (class-F target, exact F02.8 envelope) ----
    input  wire         nvm_req_i,       //! start an op (sampled while idle only)
    input  wire         nvm_we_i,        //! 1 = commit (write), 0 = restore (read)
    input  wire  [7:0]  nvm_record_id_i, //! record id (07 §5.2) = device region
    input  wire         nvm_wvalid_i,    //! commit byte present
    output logic        nvm_wready_o,    //! port accepts the commit byte
    input  wire  [7:0]  nvm_wdata_i,     //! commit byte (framed record, header first)
    output logic        nvm_rvalid_o,    //! restore byte present
    input  wire         nvm_rready_i,    //! manager accepts the restore byte
    output logic [7:0]  nvm_rdata_o,     //! restore byte (framed record, header first)
    output logic        nvm_busy_o,      //! op in flight (long periods expected)
    output logic        nvm_done_o,      //! one-cycle pulse: op complete (busy already low)
    output logic        nvm_err_o,       //! one-cycle pulse: op failed — exactly once per op
    //! the terminal cause, valid with nvm_err_o and 0 otherwise.
    //! 1 DEVICE: the device reported an error in any state, or ended the
    //! 8-byte header read short. 2 UNFRAMED: the device COMPLETED the header
    //! read and the header failed the magic or length gate, or the manager's
    //! own commit header failed it. UNFRAMED says the device answered with
    //! something that is not a record; it does not prove erased media.
    //! 3 DEADLINE: the device owed an event and presented none within
    //! MEM_TIMEOUT_CYC_P (banner): it said nothing, beside DEVICE's said
    //! no and UNFRAMED's not a record.
    output logic [1:0]  nvm_err_cause_o,

    //! ---- device face (initiator toward the side-port backend, 02 §8-free) ----
    output logic        dev_req_o,       //! command request, held until dev_gnt_i
    input  wire         dev_gnt_i,       //! backend ACCEPTED {op, region, offset, len}
    output logic [1:0]  dev_op_o,        //! NVMP_OP_READ_C / _WRITE_C / _ERASE_C
    output logic [7:0]  dev_region_o,    //! region id = record_id (one region per record)
    output logic [15:0] dev_offset_o,    //! byte offset within the region
    output logic [15:0] dev_len_o,       //! byte count (ERASE: 0 = whole region)
    output logic        dev_wvalid_o,    //! write byte present
    input  wire         dev_wready_i,    //! backend accepts the write byte
    output logic [7:0]  dev_wdata_o,     //! write byte
    input  wire         dev_rvalid_i,    //! read byte present
    input  wire  [7:0]  dev_rdata_i,     //! read byte
    output logic        dev_rready_o,    //! port accepts the read byte
    input  wire         dev_busy_i,      //! backend busy (informational; done/err delimit)
    input  wire         dev_done_i,      //! one-cycle pulse: device command complete
    input  wire         dev_err_i,       //! one-cycle pulse: device command failed
    output logic        inv_o
);

  // ---- device-face op codes (2'b11 reserved) -----------------------------
  localparam logic [1:0] NVMP_OP_READ_C  = 2'd0;
  localparam logic [1:0] NVMP_OP_WRITE_C = 2'd1;
  localparam logic [1:0] NVMP_OP_ERASE_C = 2'd2;

  // ---- record framing constants (07 §5.2, F07.8) -------------------------
  localparam logic [7:0]  MAGIC_HI_C = 8'h17;  // magic 0x1722, byte 0
  localparam logic [7:0]  MAGIC_LO_C = 8'h22;  // magic 0x1722, byte 1
  localparam logic [15:0] HDR_LEN_C  = 16'd8;  // magic+version+id+plen+crc16
  localparam logic [15:0] MAXP_C     = 16'(MAX_PAYLOAD_P);

  // ---- elaboration guard ----------------------------------------------------
  //! 0 would make every owed cycle a deadline and 2^31 or more cannot be
  //! counted at the width above
  if ((MEM_TIMEOUT_CYC_P < 1) || (MEM_TIMEOUT_CYC_P > 32'h7FFF_FFFF)) begin : g_tmo_check
    $error("KL_pp_nvm_port: MEM_TIMEOUT_CYC_P=%0d is outside 1 to 2147483647",
           MEM_TIMEOUT_CYC_P);
  end

  // ---- state machine ------------------------------------------------------
  typedef enum logic [3:0] {
    S_IDLE,     // wait for nvm_req_i
    S_WHDR,     // commit: collect the 8 header bytes into the lane buffer
    S_WEREQ,    // commit: request ERASE_REGION
    S_WEWAIT,   // commit: wait erase done
    S_WWREQ,    // commit: request WRITE of 8 + payload_length bytes
    S_WHPUMP,   // commit: pump the buffered header to the device
    S_WDPUMP,   // commit: payload pass-through manager → device
    S_WWAIT,    // commit: wait write done
    S_RHREQ,    // restore: request header READ (8 bytes at offset 0)
    S_RHCOLL,   // restore: collect the 8 header bytes into the lane buffer
    S_RHWAIT,   // restore: wait header-read done, then validate
    S_RHFWD,    // restore: forward the buffered header to the manager
    S_RPREQ,    // restore: request payload READ (payload_length at offset 8)
    S_RPPUMP,   // restore: payload pass-through device → manager
    S_RPWAIT,   // restore: wait payload-read done
    S_FIN       // one cycle: pulse done or err, busy already low
  } state_e;

  state_e            state_r;
  logic              err_r;         // S_FIN flavor: 1 = err, 0 = done
  logic        [7:0] hdr_r [0:8-1]; // the lane buffer: one framed header
  logic        [2:0] hidx_r;        // header byte cursor (collect/pump/forward)
  logic       [15:0] bcnt_r;        // payload bytes moved this phase
  logic       [15:0] plen_r;        // payload_length latched from the header
  logic        [7:0] rec_r;         // record id latched at accept
  logic              done_seen_r;   // sticky dev_done_i for the OWNED command
  logic              owed_r;        // an abandoned device command is still owed
  logic              owed_rd_r;     // ...and it is a READ: drain its bytes
  logic              lg_r;          // last cycle a deadline withdrew a request
  logic [TMO_W_C-1:0] tmo_r;        // owed cycles without the owed event

  // header validation view (bytes 0..5 are in hdr_r before the check fires)
  logic [15:0] hdr_plen_w;
  logic        hdr_ok_w;

  assign hdr_plen_w = {hdr_r[4], hdr_r[5]};
  assign hdr_ok_w   = (hdr_r[0] == MAGIC_HI_C) && (hdr_r[1] == MAGIC_LO_C)
                      && (hdr_plen_w <= MAXP_C);

  // device-command ownership (banner refusal (c)): the window in which a
  // dev_done_i is a completion of OURS — from the grant handshake (dev_req_o
  // is the four *REQ states, so a grant that carries its own done is owned)
  // through every state that runs with the granted command still outstanding.
  // S_WHDR, S_RHFWD, S_FIN, S_IDLE and an ungranted *REQ own nothing.
  logic dev_cmd_owned_w;

  assign dev_cmd_owned_w = (dev_req_o && dev_gnt_i)
                      || (state_r == S_WEWAIT) || (state_r == S_WHPUMP)
                      || (state_r == S_WDPUMP) || (state_r == S_WWAIT)
                      || (state_r == S_RHCOLL) || (state_r == S_RHWAIT)
                      || (state_r == S_RPPUMP) || (state_r == S_RPWAIT);

  // ---- the deadline (banner; processor issue #15) --------------------------
  //! the device owes the port its next event: a grant (or, while a command
  //! is owed, that command's terminal) in a request state, a terminal not
  //! yet latched in a wait state, a byte the port presents or is ready for in
  //! a data phase. A data phase whose manager stalls owes nothing.
  logic req_st_w, rd_st_w, owe_w, prog_w, tmo_hit_w, dl_w;

  assign req_st_w = (state_r == S_WEREQ) || (state_r == S_WWREQ)
                  || (state_r == S_RHREQ) || (state_r == S_RPREQ);
  assign rd_st_w  = (state_r == S_RHREQ) || (state_r == S_RHCOLL)
                  || (state_r == S_RHWAIT) || (state_r == S_RPREQ)
                  || (state_r == S_RPPUMP) || (state_r == S_RPWAIT);
  assign owe_w    = req_st_w
                  || (((state_r == S_WEWAIT) || (state_r == S_WWAIT) || (state_r == S_RHWAIT)
                       || (state_r == S_RPWAIT)) && !done_seen_r)
                  || (state_r == S_WHPUMP) || (state_r == S_RHCOLL)
                  || ((state_r == S_WDPUMP) && nvm_wvalid_i)
                  || ((state_r == S_RPPUMP) && nvm_rready_i);
  //! ...and gives one: a grant, a byte, an err, or a done that ends a
  //! command of ours or the owed one. A done that belongs to nobody (refusal
  //! (c)) is not progress.
  assign prog_w   = dev_err_i
                  || (dev_done_i && (dev_cmd_owned_w || owed_r))
                  || (dev_req_o && dev_gnt_i)
                  || (dev_wvalid_o && dev_wready_i)
                  || (dev_rvalid_i && dev_rready_o);
  assign tmo_hit_w = (tmo_r == TMO_W_C'(MEM_TIMEOUT_CYC_P));
  //! the verdict: owed, still nothing, MEM_TIMEOUT_CYC_P owed cycles already
  //! counted since the last restart. An event in this very cycle is progress
  //! and wins, so a live terminal can never be pending at a verdict.
  assign dl_w = owe_w && !prog_w && tmo_hit_w;

  always_ff @(posedge clk_i) begin : nvm_port_tmo
    if (!rst_n)                             tmo_r <= '0;
    else if (prog_w || (state_r == S_IDLE)) tmo_r <= '0;   // restart; zero between ops
    else if (owe_w && !tmo_hit_w)           tmo_r <= tmo_r + TMO_W_C'(1);  // else held
  end

  //! the owed command. Set when a deadline abandons a command the device
  //! accepted (every state the ownership window names but a request), or
  //! when the device grants a request the deadline withdrew, one cycle
  //! late; cleared only by its done or err, which belongs to no operation,
  //! or by reset. Its kind is taken only while nothing is owed, so a later
  //! deadline never stops the drain of an owed READ.
  always_ff @(posedge clk_i) begin : nvm_port_owed
    if (!rst_n) begin
      owed_r    <= 1'b0;
      owed_rd_r <= 1'b0;
      lg_r      <= 1'b0;
    end else begin
      lg_r <= dl_w && dev_req_o;
      if (dl_w && !owed_r) owed_rd_r <= rd_st_w;
      if (owed_r) begin
        if (dev_done_i || dev_err_i) owed_r <= 1'b0;
      end else if (dl_w && dev_cmd_owned_w) begin
        owed_r <= 1'b1;
      end else if (lg_r && dev_gnt_i && !dev_done_i && !dev_err_i) begin
        owed_r <= 1'b1;
      end
    end
  end

  always_ff @(posedge clk_i) begin : nvm_port_fsm
    if (!rst_n) begin
      state_r     <= S_IDLE;
      err_r       <= 1'b0;
      hidx_r      <= '0;
      bcnt_r      <= '0;
      plen_r      <= '0;
      rec_r       <= '0;
      done_seen_r <= 1'b0;
      for (int unsigned i = 0; i < 8; i++) hdr_r[i] <= '0;
    end else begin
      // device done may land on the same cycle a pump moves its last byte —
      // remember it; the WAIT states consume it (assignment below overrides).
      // Only while we own the command it completes: a done seen outside that
      // window is not ours to consume (banner refusal (c))
      if (dev_done_i && dev_cmd_owned_w) done_seen_r <= 1'b1;

      case (state_r)
        S_IDLE: begin
          err_r <= 1'b0;
          if (nvm_req_i) begin
            rec_r       <= nvm_record_id_i;
            hidx_r      <= '0;
            bcnt_r      <= '0;
            done_seen_r <= 1'b0;
            state_r     <= nvm_we_i ? S_WHDR : S_RHREQ;
          end
        end

        // ---------------------------------------------------------- commit
        S_WHDR: begin
          if (nvm_wvalid_i) begin
            hdr_r[hidx_r] <= nvm_wdata_i;
            hidx_r        <= hidx_r + 3'd1;
            if (hidx_r == 3'd7) begin
              plen_r <= hdr_plen_w;
              if (hdr_ok_w) begin
                state_r <= S_WEREQ;
              end else begin
                err_r   <= 1'b1;      // refused: unframed/oversize (07 §5.2)
                state_r <= S_FIN;     // no device traffic was issued
              end
            end
          end
        end

        S_WEREQ: if (!owed_r) begin   // an owed command blocks the request
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;
          end else if (dev_gnt_i) begin
            state_r <= S_WEWAIT;
          end
        end

        S_WEWAIT: begin
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;         // erase failed: exactly one err, no WRITE
          end else if (dev_done_i || done_seen_r) begin
            done_seen_r <= 1'b0;
            state_r     <= S_WWREQ;
          end
        end

        S_WWREQ: if (!owed_r) begin   // an owed command blocks the request
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;
          end else if (dev_gnt_i) begin
            hidx_r  <= '0;
            state_r <= S_WHPUMP;
          end
        end

        S_WHPUMP: begin
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;
          end else if (done_seen_r || (dev_done_i
                       && !(dev_wready_i && (hidx_r == 3'd7) && (plen_r == 16'd0)))) begin
            err_r   <= 1'b1;          // refusal (d): the WRITE ended short
            state_r <= S_FIN;
          end else if (dev_wready_i) begin
            hidx_r <= hidx_r + 3'd1;
            if (hidx_r == 3'd7) begin
              bcnt_r  <= '0;
              state_r <= (plen_r == 16'd0) ? S_WWAIT : S_WDPUMP;
            end
          end
        end

        S_WDPUMP: begin
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;
          end else if (done_seen_r || (dev_done_i
                       && !(nvm_wvalid_i && dev_wready_i && (bcnt_r == (plen_r - 16'd1)))))
          begin
            err_r   <= 1'b1;          // refusal (d): the WRITE ended short
            state_r <= S_FIN;
          end else if (nvm_wvalid_i && dev_wready_i) begin
            bcnt_r <= bcnt_r + 16'd1;
            if (bcnt_r == (plen_r - 16'd1)) state_r <= S_WWAIT;
          end
        end

        S_WWAIT: begin
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;
          end else if (dev_done_i || done_seen_r) begin
            done_seen_r <= 1'b0;
            state_r     <= S_FIN;     // err_r stays 0: done
          end
        end

        // --------------------------------------------------------- restore
        S_RHREQ: if (!owed_r) begin   // an owed command blocks the request
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;
          end else if (dev_gnt_i) begin
            hidx_r  <= '0;
            state_r <= S_RHCOLL;
          end
        end

        S_RHCOLL: begin
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;
          end else begin
            if (dev_rvalid_i) begin
              hdr_r[hidx_r] <= dev_rdata_i;
              hidx_r        <= hidx_r + 3'd1;
              if (hidx_r == 3'd7) state_r <= S_RHWAIT;
            end
            // refusal (d): done with fewer than 8 bytes delivered, live or
            // latched off the grant, is a short read
            if (done_seen_r || (dev_done_i && !(dev_rvalid_i && (hidx_r == 3'd7)))) begin
              err_r   <= 1'b1;
              state_r <= S_FIN;
            end
          end
        end

        S_RHWAIT: begin
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;
          end else if (dev_done_i || done_seen_r) begin
            done_seen_r <= 1'b0;
            plen_r      <= hdr_plen_w;
            if (hdr_ok_w) begin
              hidx_r  <= '0;
              state_r <= S_RHFWD;     // forward only a validated header
            end else begin
              err_r   <= 1'b1;        // refused: stored record unframed/oversize
              state_r <= S_FIN;       // nothing was forwarded to the manager
            end
          end
        end

        S_RHFWD: begin
          if (nvm_rready_i) begin
            hidx_r <= hidx_r + 3'd1;
            if (hidx_r == 3'd7) begin
              bcnt_r  <= '0;
              state_r <= (plen_r == 16'd0) ? S_FIN : S_RPREQ;  // err_r stays 0
            end
          end
        end

        S_RPREQ: if (!owed_r) begin   // an owed command blocks the request
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;
          end else if (dev_gnt_i) begin
            bcnt_r  <= '0;
            state_r <= S_RPPUMP;
          end
        end

        S_RPPUMP: begin
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;
          end else if (done_seen_r || (dev_done_i
                       && !(dev_rvalid_i && nvm_rready_i && (bcnt_r == (plen_r - 16'd1)))))
          begin
            err_r   <= 1'b1;          // refusal (d): the READ ended short
            state_r <= S_FIN;
          end else if (dev_rvalid_i && nvm_rready_i) begin
            bcnt_r <= bcnt_r + 16'd1;
            if (bcnt_r == (plen_r - 16'd1)) state_r <= S_RPWAIT;
          end
        end

        S_RPWAIT: begin
          if (dev_err_i) begin
            err_r   <= 1'b1;
            state_r <= S_FIN;
          end else if (dev_done_i || done_seen_r) begin
            done_seen_r <= 1'b0;
            state_r     <= S_FIN;     // err_r stays 0: done
          end
        end

        // ------------------------------------------------------------ fin
        S_FIN: begin
          done_seen_r <= 1'b0;        // ownership retires with the op, so a
                                      // completion latched but never consumed
                                      // cannot outlive it (error exits land
                                      // here too)
          state_r     <= S_IDLE;      // one pulse cycle, then idle
        end

        default: state_r <= S_IDLE;
      endcase

      // the deadline: no transition above can fire in its cycle, since any
      // owed event is progress
      if (dl_w) begin
        err_r   <= 1'b1;
        state_r <= S_FIN;
      end
    end
  end

  // ---- the terminal cause (issue #93, S1) ----------------------------------
  //! UNFRAMED only where this port itself refuses a header: one the device
  //! delivered whole (S_RHWAIT, done without err) or the manager streamed
  //! (S_WHDR's eighth byte). DEADLINE only on the deadline's verdict. Every
  //! other err is DEVICE, every short command included. Taken on the
  //! transition into S_FIN and held there, the cycle nvm_err_o pulses.
  localparam logic [1:0] CAUSE_DEVICE_C   = 2'd1;
  localparam logic [1:0] CAUSE_UNFRAMED_C = 2'd2;
  localparam logic [1:0] CAUSE_DEADLINE_C = 2'd3;
  logic [1:0] cause_r;
  logic       refuse_w;

  assign refuse_w = ((state_r == S_RHWAIT) && !dev_err_i
                     && (dev_done_i || done_seen_r) && !hdr_ok_w)
                  || ((state_r == S_WHDR) && nvm_wvalid_i && (hidx_r == 3'd7)
                     && !hdr_ok_w);

  always_ff @(posedge clk_i) begin : nvm_port_cause
    if (!rst_n) begin
      cause_r <= 2'd0;
    end else if (refuse_w) begin
      cause_r <= CAUSE_UNFRAMED_C;
    end else if (dl_w) begin
      cause_r <= CAUSE_DEADLINE_C;
    end else if ((state_r != S_FIN) && (state_r != S_IDLE)) begin
      cause_r <= CAUSE_DEVICE_C;
    end
  end

  assign nvm_err_cause_o = nvm_err_o ? cause_r : 2'd0;

  // ---- manager face outputs ----------------------------------------------
  assign nvm_busy_o   = (state_r != S_IDLE) && (state_r != S_FIN);
  assign nvm_done_o   = (state_r == S_FIN) && !err_r;
  assign nvm_err_o    = (state_r == S_FIN) &&  err_r;

  assign nvm_wready_o = (state_r == S_WHDR)
                      || ((state_r == S_WDPUMP) && dev_wready_i);
  assign nvm_rvalid_o = (state_r == S_RHFWD)
                      || ((state_r == S_RPPUMP) && dev_rvalid_i);
  assign nvm_rdata_o  = (state_r == S_RHFWD) ? hdr_r[hidx_r] : dev_rdata_i;

  // ---- device face outputs -----------------------------------------------
  assign dev_req_o    = req_st_w && !owed_r;         // never over an owed command
  assign dev_region_o = rec_r;

  assign dev_wvalid_o = (state_r == S_WHPUMP)
                      || ((state_r == S_WDPUMP) && nvm_wvalid_i);
  assign dev_wdata_o  = (state_r == S_WHPUMP) ? hdr_r[hidx_r] : nvm_wdata_i;
  assign dev_rready_o = (state_r == S_RHCOLL)
                      || ((state_r == S_RPPUMP) && nvm_rready_i)
                      || (owed_r && owed_rd_r);        // the owed READ's drain

  always_comb begin : dev_cmd
    dev_op_o     = NVMP_OP_READ_C;
    dev_offset_o = 16'd0;
    dev_len_o    = 16'd0;
    case (state_r)
      S_WEREQ: dev_op_o = NVMP_OP_ERASE_C;                 // len 0 = whole region
      S_WWREQ: begin
        dev_op_o  = NVMP_OP_WRITE_C;
        dev_len_o = HDR_LEN_C + plen_r;                    // plen_r ≤ MAXP_C
      end
      S_RHREQ: dev_len_o = HDR_LEN_C;                      // header probe
      S_RPREQ: begin
        dev_offset_o = HDR_LEN_C;
        dev_len_o    = plen_r;
      end
      default: ;
    endcase
  end

  assign inv_o = owed_r && !((state_r == S_IDLE) || (state_r == S_FIN) || (state_r == S_WHDR)
                           || (state_r == S_WEREQ) || (state_r == S_RHREQ));
endmodule

`default_nettype wire
