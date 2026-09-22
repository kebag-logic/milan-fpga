/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_aecp_resp_buf.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/03 §7 response buffers,
//                 06 §8 BUILD_HEADER / BUILD_FIELD / APPEND / COPY_BUFFER,
//                 07 §3.3 the integrator's main memory)
//
//  Description : The AECP RESPONSE BUFFER, held in the integrator's MAIN
//                MEMORY instead of on chip. It takes the µCPU's byte-strobed
//                response-buffer writes, gathers them into 64-bit lanes and
//                writes each finished lane out over the read/write master
//                below; when the µprogram seals the response the buffer reads
//                the emitted payload back as ONE burst and serves it to the
//                frame builder, one byte per `rd_take_i`.
//
//                WHY IT IS NOT ON CHIP. The buffer is 07 §3.2's worst-case
//                descriptor plus its 16-byte prefix — `RESP_BYTES_P` = 592 B
//                at the shipping shape. Held as fabric state it measured
//                5,079 flip-flops and 3,495 LUTs inside KL_aecp_engine on the
//                reference part (xc7a100t, Vivado 2026.1, post-synthesis
//                out-of-context at the 1-stream shape), and it was those flops
//                the placer could not pack on a die whose 135 block-RAM tiles
//                were already 100 % spoken for. It is not a cache, it is never
//                read while it is being written, and nothing but the frame
//                builder ever looks at it — exactly the state that belongs
//                behind a memory port.
//
//                WHY THE LATENCY IS FREE. IEEE 1722.1 §9.2.1.1 gives an AECP
//                command 100 ms before its controller may retry, and the
//                reference SoC measures ~1424 ns on a miss to main memory. The
//                worst-case response here is 73 lane writes plus one read
//                burst — see docs/architecture/08 §4 and the arithmetic in
//                tb/resp_buf/README.md, which the suite measures rather than
//                assumes.
//
//                WHY THE ADDRESS IS A PARAMETER. The same rule as
//                KL_aecp_desc_store's `DESC_BASE_P`: the memory map is fixed
//                when the bitstream is built, so `RESP_BASE_P` is an
//                ELABORATION PARAMETER and never a register — a runtime base
//                would only buy a 32-bit port and the flops behind it. The
//                integrator must reserve `RESP_BYTES_P` bytes there that
//                nothing else writes: unlike the descriptor image this region
//                is written BY THE PROCESSOR, so an overlap with the image is
//                silent corruption of the entity model.
//
//                WRITE ORDER. Ordinary µCPU fields arrive non-decreasing from
//                byte 12 upward. GET_DYNAMIC_INFO adds one deliberate
//                exception: after an ordinary getter has produced a record,
//                the engine revisits that record header to patch its final
//                info_status byte, then resumes at the next record. This is
//                safe because lane writes are serialized, the memory face has
//                byte strobes, and a reopened lane writes only the patched
//                byte. The response-buffer suite exercises the backward patch
//                and the following forward write as a byte-exact contract.
//                Writes below byte 12 are ACCEPTED AND DROPPED: 06 §8's 12-byte
//                header record is not the wire header (KL_aecp_engine
//                synthesises the real 24-byte AECPDU header from the 03 §4
//                transaction), so those bytes have no reader and are not worth
//                a memory cycle.
//
//                BYTE ORDER. `wr_wdata_i` carries a field VALUE right-
//                justified with a low-contiguous `wr_wstrb_i` giving its width
//                (1/2/4 bytes); those m bytes are placed BIG-ENDIAN from
//                `wr_addr_i` upward, which is the IEEE 1722.1 wire order of
//                every AEM field. An accepted write is absorbed ONE BYTE PER
//                CYCLE afterwards, which is what makes a field straddling a
//                lane boundary need no special case: the straddling byte
//                simply flushes the lane and opens the next.
//
//                `wr_ready_o` IS A REGISTER, and that is a timing decision,
//                not a style one. Every write is captured into a one-deep skid
//                and absorbed from there, so `wr_ready_o` depends on this
//                block's state ALONE — never on `wr_addr_i`. Drive it from the
//                address instead and the µCPU's stall path runs
//                uop.fmt -> cursor+len -> rb_addr -> this block's lane compare
//                -> back into `stall_e_w` -> the µcode-ROM address, a round
//                trip that measured 18 logic levels and cost ~1 ns of WNS on
//                the reference part. The skid costs one dead cycle per write
//                and buys the whole loop back.
//
//                WHAT A TIED-OFF MASTER MEANS. Leaving `mem_req_ready_i` and
//                `mem_wr_ready_i` at 0 is a LEGAL wiring, exactly as it is for
//                KL_aecp_desc_store: the no-progress watchdog raises `err_o`
//                and the buffer stops asking. It never stalls the µCPU forever
//                (`wr_ready_o` is forced high once `err_o` is set) and it never
//                serves a byte it did not read (`rd_valid_o` stays low), so the
//                engine turns the failure into a well-formed error response
//                rather than a hang or a lie on the wire.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_aecp_resp_buf #(
    //! Byte address of the response buffer in the integrator's memory map.
    //! COMPILE TIME by contract — see the banner. Must be 8-byte aligned and
    //! must NOT overlap KL_aecp_desc_store's image at `DESC_BASE_P`.
    parameter logic [31:0] RESP_BASE_P       = 32'h2010_0000,
    //! Response-buffer capacity in bytes (03 §7 slot size + the 06 §8 header
    //! record). A byte at or above this is dropped, never wrapped.
    parameter int unsigned RESP_BYTES_P      = 592,
    //! No-progress watchdog on the memory face, in clocks. Same contract as
    //! KL_aecp_desc_store: an absent or wedged bridge must DEGRADE, never
    //! hang. 4096 is 41 µs at P-CLK-HZ = 100 MHz, far inside T-AECP-RESP.
    parameter int unsigned MEM_TIMEOUT_CYC_P = 4096,
    //! derived — do not override
    localparam int unsigned LANES_C  = (RESP_BYTES_P + 7) / 8,
    localparam int unsigned LANE_W_C = $clog2(LANES_C),
    localparam int unsigned TMO_W_C  = $clog2(MEM_TIMEOUT_CYC_P + 1)
) (
    input  wire         clk_i,            //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,            //! synchronous active-low reset

    //! ---- response lifecycle (driven by KL_aecp_engine) ----
    input  wire         open_i,           //! start a NEW response: drop the open
                                          //!  lane, clear the fault, re-arm
    input  wire         seal_i,           //! µprogram retired: flush, then read
                                          //!  the emitted payload back
    input  wire  [10:0] seal_len_i,       //! payload bytes to stream, counted
                                          //!  from buffer byte 12 (0 = none)

    //! ---- µCPU response-buffer write face (06 §8, byte-strobed) ----
    input  wire         wr_we_i,          //! write presented, HELD until ready
    input  wire   [9:0] wr_addr_i,        //! byte address of the field
    input  wire  [31:0] wr_wdata_i,       //! field value, right-justified
    input  wire   [3:0] wr_wstrb_i,       //! low-contiguous width: 1 / 3 / F
    output logic        wr_ready_o,       //! the whole write is absorbed now

    //! ---- payload read stream (to the frame builder) ----
    output logic        rd_valid_o,       //! `rd_data_o` holds the next byte
    output logic  [7:0] rd_data_o,        //! payload byte, in emission order
    input  wire         rd_take_i,        //! builder consumed the byte

    //! ---- main-memory master, READ + WRITE (vendor-neutral by contract) ----
    //! READ: one outstanding request, responses IN ORDER, `rsp_last` marks the
    //! final beat, a beat carries its lowest byte address in bits [63:56].
    //! `mem_rsp_ready_o` is REAL backpressure here — the buffer accepts a beat
    //! only once the previous one is spent — so a bridge must HOLD a beat until
    //! it is taken.
    output logic        mem_req_valid_o,  //! read request, held until ready
    input  wire         mem_req_ready_i,  //! bridge accepts the request
    output logic [31:0] mem_req_addr_o,   //! byte address, 8-byte aligned
    output logic  [8:0] mem_req_beats_o,  //! 64-bit beats in this burst (>= 1)
    input  wire         mem_rsp_valid_i,  //! response beat present
    output logic        mem_rsp_ready_o,  //! buffer consumes the beat
    input  wire  [63:0] mem_rsp_data_i,   //! beat data (big-endian byte lane)
    input  wire         mem_rsp_last_i,   //! final beat of the burst
    input  wire         mem_rsp_err_i,    //! read failed — abort the burst
    //! WRITE: ONE outstanding single-beat write. `mem_wr_data_o` is a 64-bit
    //! lane in the SAME big-endian byte order as a read beat (byte `addr + n`
    //! is bits [63-8n -: 8]) and `mem_wr_strb_o` bit n enables that byte — a
    //! byte whose strobe is 0 SHALL NOT be modified in memory. `mem_wr_done_i`
    //! is a one-cycle pulse when the write is COMMITTED; the buffer issues no
    //! further request until it arrives, so a bridge may report done in the
    //! same cycle as ready (posted) or any cycle after (acknowledged).
    //! ORDERING: a read request accepted after a write reported done SHALL
    //! observe that write. Nothing else in this processor addresses the
    //! region, so no further ordering rule is needed.
    output logic        mem_wr_valid_o,   //! write presented, held until ready
    input  wire         mem_wr_ready_i,   //! bridge accepts the write
    output logic [31:0] mem_wr_addr_o,    //! byte address, 8-byte aligned
    output logic [63:0] mem_wr_data_o,    //! lane data (big-endian byte lane)
    output logic  [7:0] mem_wr_strb_o,    //! per-byte enable, bit n = byte n
    input  wire         mem_wr_done_i,    //! write committed (one-cycle pulse)
    input  wire         mem_wr_err_i,     //! ... and it failed

    //! ---- observability (07 §2 debug window / suite taps) ----
    output logic        busy_o,           //! a memory transaction is in flight —
                                          //!  `open_i` is only legal while low,
                                          //!  and it is watchdog-bounded
    output logic        err_o,            //! sticky fault: this response is void
    output logic  [2:0] dbg_fault_o,      //! why (FAULT_*_C below)
    output logic [15:0] dbg_lane_wr_o,    //! lane writes committed
    output logic [15:0] dbg_burst_o,      //! read bursts issued
    output logic [15:0] dbg_drop_o        //! bytes dropped (below 12 / past end)
);

  // ---- fault codes (dbg_fault_o) ------------------------------------------
  localparam logic [2:0] FAULT_NONE_C = 3'd0;
  localparam logic [2:0] FAULT_WTMO_C = 3'd1;   // write watchdog
  localparam logic [2:0] FAULT_WERR_C = 3'd2;   // bridge reported a write error
  localparam logic [2:0] FAULT_RTMO_C = 3'd3;   // read watchdog
  localparam logic [2:0] FAULT_RERR_C = 3'd4;   // bridge reported a read error

  //! the µCPU's 12-byte header record (06 §8) has no reader — see the banner
  localparam logic [9:0] HDR_BYTES_C = 10'd12;
  //! byte 12 lives in lane 1, at byte offset 4
  localparam logic [2:0] FIRST_OFF_C = 3'd4;

  // ---- elaboration guards --------------------------------------------------
  if (RESP_BASE_P[2:0] != 3'd0) begin : gen_g_base_align
    $error("RESP_BASE_P=%08h must be 8-byte aligned", RESP_BASE_P);
  end
  if (RESP_BYTES_P <= 16) begin : gen_g_size
    $error("RESP_BYTES_P=%0d leaves no payload above the header record",
           RESP_BYTES_P);
  end
  if (LANES_C > 511) begin : gen_g_beats
    $error("a read burst of %0d beats exceeds the 9-bit mem_req_beats_o field",
           LANES_C);
  end

  // =========================================================================
  // the open lane — the ONLY on-chip state this buffer keeps
  // =========================================================================
  logic [63:0]         lane_d_r;
  logic  [7:0]         lane_s_r;
  logic [LANE_W_C-1:0] lane_ix_r;
  logic                lane_open_r;

  typedef enum logic [2:0] {
    R_FILL, R_FLUSH, R_RREQ, R_STREAM, R_DRAIN, R_DONE, R_ERR
  } r_st_e;
  r_st_e st_r;

  logic        seal_pend_r;    // a seal is waiting for the flush in flight
  logic [10:0] len_r;          // sealed payload length
  logic [10:0] served_r;       // payload bytes handed to the builder
  logic [63:0] rlane_r;        // beat being served
  logic        rvalid_r;
  logic  [2:0] roff_r;         // byte offset inside `rlane_r`
  logic        fault_r;
  logic  [2:0] fcode_r;
  logic [15:0] lanewr_r, burst_r, drop_r;

  // ---- the write skid: ONE captured write, absorbed a byte at a time ------
  logic        sk_valid_r;
  logic  [9:0] sk_addr_r;
  logic [31:0] sk_data_r;
  logic  [3:0] sk_strb_r;
  logic  [1:0] bix_r;          // byte of the captured write being absorbed
  logic        wr_ready_r;

  // ---- memory sequencing ---------------------------------------------------
  logic               wreq_r;   // write request presented
  logic               wbusy_r;  // write accepted, waiting for done
  logic               rreq_r;   // read request presented
  logic               rbusy_r;  // read burst outstanding
  logic [TMO_W_C-1:0] tmo_r;

  logic beat_w, tmo_hit_w, wait_w;
  assign beat_w    = mem_rsp_valid_i && mem_rsp_ready_o && rbusy_r;
  assign tmo_hit_w = (tmo_r == TMO_W_C'(MEM_TIMEOUT_CYC_P));
  //! the watchdog measures the BRIDGE, not us: it only runs while this block
  //! is actually waiting on the far side, so holding `mem_rsp_ready_o` low
  //! while the builder drains a beat can never trip it
  assign wait_w = (wreq_r  && !mem_wr_ready_i)
                  || (wbusy_r && !mem_wr_done_i)
                  || (rreq_r  && !mem_req_ready_i)
                  || (rbusy_r && mem_rsp_ready_o && !mem_rsp_valid_i);

  // =========================================================================
  // the captured write, one byte at a time
  // =========================================================================
  //! the handshake: a write is TAKEN in any cycle both are high, and
  //! `wr_ready_o` is a register (see the banner)
  assign wr_ready_o = wr_ready_r;

  logic accept_w;
  assign accept_w = wr_we_i && wr_ready_r;

  logic [2:0] m_w;                        // strobed width in bytes (0/1/2/4)
  always_comb begin : strobe_width
    if      (sk_strb_r[3]) m_w = 3'd4;
    else if (sk_strb_r[1]) m_w = 3'd2;
    else if (sk_strb_r[0]) m_w = 3'd1;
    else                   m_w = 3'd0;
  end

  logic [10:0] babs_w;                    // byte address being absorbed
  assign babs_w = {1'b0, sk_addr_r} + {9'd0, bix_r};

  //! BIG-ENDIAN placement of the m strobed bytes (see the banner)
  logic [7:0] bval_w;
  always_comb begin : byte_value
    unique case (m_w)
      3'd1: bval_w = sk_data_r[7:0];
      3'd2: bval_w = (bix_r == 2'd0) ? sk_data_r[15:8] : sk_data_r[7:0];
      default: unique case (bix_r)
                 2'd0:    bval_w = sk_data_r[31:24];
                 2'd1:    bval_w = sk_data_r[23:16];
                 2'd2:    bval_w = sk_data_r[15:8];
                 default: bval_w = sk_data_r[7:0];
               endcase
    endcase
  end

  logic keep_w;                           // this byte belongs to the buffer
  assign keep_w = (babs_w >= {1'b0, HDR_BYTES_C})
                  && (babs_w < 11'(RESP_BYTES_P));

  logic [LANE_W_C-1:0] tgt_lane_w;
  logic          [2:0] tgt_off_w;
  assign tgt_lane_w = LANE_W_C'(babs_w >> 3);
  assign tgt_off_w  = babs_w[2:0];

  //! a byte for a DIFFERENT lane closes the open one first — the write-order
  //! rule in the banner is what makes this a ONE-LANE buffer, not a 592-byte one
  logic need_flush_w;
  assign need_flush_w = sk_valid_r && (st_r == R_FILL) && (m_w != 3'd0)
                        && keep_w && lane_open_r
                        && (tgt_lane_w != lane_ix_r);

  logic take_byte_w, last_byte_w;
  assign last_byte_w = ({1'b0, bix_r} + 3'd1) >= m_w;
  assign take_byte_w = sk_valid_r && (st_r == R_FILL) && !need_flush_w;

  // =========================================================================
  // the read stream
  // =========================================================================
  assign rd_valid_o = rvalid_r && (st_r == R_STREAM);

  always_comb begin : read_byte
    rd_data_o = 8'd0;
    for (int unsigned k = 0; k < 8; k++) begin
      if (roff_r == 3'(k)) rd_data_o = rlane_r[63 - 8*k -: 8];
    end
  end

  //! accept a beat only once the current one is spent — the burst paces itself
  //! against the builder's one-byte-per-cycle appetite
  assign mem_rsp_ready_o = (st_r == R_DRAIN)
                           || ((st_r == R_STREAM) && !rvalid_r);

  // ---- the read geometry of a sealed response ------------------------------
  logic [10:0] last_byte_ix_w;
  logic  [8:0] rbeats_w;
  assign last_byte_ix_w = {1'b0, HDR_BYTES_C} + len_r - 11'd1;
  //! lanes 1 .. (last_byte >> 3) inclusive, so the beat count IS that index
  assign rbeats_w = 9'(last_byte_ix_w >> 3);

  // ---- outputs -------------------------------------------------------------
  assign mem_req_valid_o = rreq_r;
  assign mem_req_addr_o  = RESP_BASE_P + 32'd8;
  assign mem_req_beats_o = rbeats_w;
  assign mem_wr_valid_o  = wreq_r;
  assign mem_wr_addr_o   = RESP_BASE_P + (32'(lane_ix_r) << 3);
  assign mem_wr_data_o   = lane_d_r;
  assign mem_wr_strb_o   = lane_s_r;

  assign busy_o        = wreq_r || wbusy_r || rreq_r || rbusy_r;
  assign err_o         = fault_r;
  assign dbg_fault_o   = fcode_r;
  assign dbg_lane_wr_o = lanewr_r;
  assign dbg_burst_o   = burst_r;
  assign dbg_drop_o    = drop_r;

  // =========================================================================
  // the machine
  // =========================================================================
  always_ff @(posedge clk_i) begin : core
    if (!rst_n) begin
      st_r        <= R_FILL;
      lane_d_r    <= 64'd0;
      lane_s_r    <= 8'd0;
      lane_ix_r   <= '0;
      lane_open_r <= 1'b0;
      seal_pend_r <= 1'b0;
      len_r       <= 11'd0;
      served_r    <= 11'd0;
      rlane_r     <= 64'd0;
      rvalid_r    <= 1'b0;
      roff_r      <= FIRST_OFF_C;
      fault_r     <= 1'b0;
      fcode_r     <= FAULT_NONE_C;
      lanewr_r    <= 16'd0;
      burst_r     <= 16'd0;
      drop_r      <= 16'd0;
      sk_valid_r  <= 1'b0;
      sk_addr_r   <= 10'd0;
      sk_data_r   <= 32'd0;
      sk_strb_r   <= 4'd0;
      bix_r       <= 2'd0;
      wr_ready_r  <= 1'b1;
      wreq_r      <= 1'b0;
      wbusy_r     <= 1'b0;
      rreq_r      <= 1'b0;
      rbusy_r     <= 1'b0;
      tmo_r       <= '0;
    end else begin
      // ---------------- no-progress watchdog --------------------------------
      if (!wait_w)          tmo_r <= '0;
      else if (!tmo_hit_w)  tmo_r <= tmo_r + TMO_W_C'(1);

      // ---------------- a new response re-arms everything -------------------
      if (open_i) begin
        st_r        <= R_FILL;
        lane_open_r <= 1'b0;
        lane_s_r    <= 8'd0;
        seal_pend_r <= 1'b0;
        served_r    <= 11'd0;
        rvalid_r    <= 1'b0;
        roff_r      <= FIRST_OFF_C;
        fault_r     <= 1'b0;
        fcode_r     <= FAULT_NONE_C;
        len_r       <= 11'd0;
        sk_valid_r  <= 1'b0;
        bix_r       <= 2'd0;
        wr_ready_r  <= 1'b1;
        tmo_r       <= '0;
      end else begin
        //! capture the presented write; the registered ready is what keeps
        //! this block's address arithmetic out of the µCPU's stall path
        if (accept_w) begin
          sk_valid_r <= 1'b1;
          sk_addr_r  <= wr_addr_i;
          sk_data_r  <= wr_wdata_i;
          sk_strb_r  <= wr_wstrb_i;
          bix_r      <= 2'd0;
          wr_ready_r <= 1'b0;
        end else if (!sk_valid_r) begin
          wr_ready_r <= (st_r == R_FILL) || (st_r == R_ERR);
        end
        unique case (st_r)
          // ---------------- gathering the µCPU's bytes ----------------------
          R_FILL: begin
            if (take_byte_w) begin
              if (keep_w && (m_w != 3'd0)) begin
                if (!lane_open_r) begin
                  lane_open_r <= 1'b1;
                  lane_ix_r   <= tgt_lane_w;
                  lane_d_r    <= 64'd0;
                  lane_s_r    <= 8'd0;
                end
                for (int unsigned k = 0; k < 8; k++) begin
                  if (tgt_off_w == 3'(k)) begin
                    lane_d_r[63 - 8*k -: 8] <= bval_w;
                    lane_s_r[k]             <= 1'b1;
                  end
                end
              end else if ((m_w != 3'd0) && (drop_r != 16'hFFFF)) begin
                drop_r <= drop_r + 16'd1;
              end
              if (last_byte_w) begin
                sk_valid_r <= 1'b0;
                bix_r      <= 2'd0;
                wr_ready_r <= 1'b1;
              end else begin
                bix_r <= bix_r + 2'd1;
              end
            end
            //! a seal is remembered even if a lane flush has to go out first
            if (seal_i) begin
              len_r       <= seal_len_i;
              seal_pend_r <= 1'b1;
            end
            //! the seal only fires once the skid is EMPTY: its last bytes are
            //! part of this response and the lane they open still has to go out
            if (need_flush_w) begin
              wreq_r <= 1'b1;
              st_r   <= R_FLUSH;
            end else if ((seal_pend_r || seal_i) && !sk_valid_r) begin
              if (lane_open_r) begin
                wreq_r <= 1'b1;
                st_r   <= R_FLUSH;
              end else begin
                st_r <= R_RREQ;
              end
            end
          end

          // ---------------- one lane out to main memory ---------------------
          R_FLUSH: begin
            //! a seal landing on top of a mid-response flush is remembered
            if (seal_i) begin
              len_r       <= seal_len_i;
              seal_pend_r <= 1'b1;
            end
            if (wreq_r && mem_wr_ready_i) begin
              wreq_r  <= 1'b0;
              wbusy_r <= 1'b1;
            end
            if (wbusy_r && mem_wr_done_i) begin
              wbusy_r     <= 1'b0;
              lane_open_r <= 1'b0;
              lane_s_r    <= 8'd0;
              if (lanewr_r != 16'hFFFF) lanewr_r <= lanewr_r + 16'd1;
              if (mem_wr_err_i) begin
                fault_r <= 1'b1;
                fcode_r <= FAULT_WERR_C;
                st_r    <= R_ERR;
              end else begin
                //! a seal cannot be honoured while the skid still holds bytes
                //! of this response — go back and absorb them first
                st_r <= (seal_pend_r && !sk_valid_r) ? R_RREQ : R_FILL;
              end
            end else if (tmo_hit_w) begin
              wreq_r  <= 1'b0;
              wbusy_r <= 1'b0;
              fault_r <= 1'b1;
              fcode_r <= FAULT_WTMO_C;
              st_r    <= R_ERR;
            end
          end

          // ---------------- read the emitted payload back -------------------
          R_RREQ: begin
            seal_pend_r <= 1'b0;
            if (len_r == 11'd0) begin
              st_r <= R_DONE;
            end else begin
              rreq_r <= 1'b1;
              if (rreq_r && mem_req_ready_i) begin
                rreq_r  <= 1'b0;
                rbusy_r <= 1'b1;
                roff_r  <= FIRST_OFF_C;
                if (burst_r != 16'hFFFF) burst_r <= burst_r + 16'd1;
                st_r    <= R_STREAM;
              end else if (tmo_hit_w) begin
                rreq_r  <= 1'b0;
                fault_r <= 1'b1;
                fcode_r <= FAULT_RTMO_C;
                st_r    <= R_ERR;
              end
            end
          end

          R_STREAM: begin
            if (beat_w) begin
              rlane_r  <= mem_rsp_data_i;
              rvalid_r <= 1'b1;
              if (mem_rsp_last_i) rbusy_r <= 1'b0;
              if (mem_rsp_err_i) begin
                rvalid_r <= 1'b0;
                rbusy_r  <= 1'b0;
                fault_r  <= 1'b1;
                fcode_r  <= FAULT_RERR_C;
                st_r     <= R_ERR;
              end
            end
            if (rd_take_i && rvalid_r) begin
              served_r <= served_r + 11'd1;
              roff_r   <= roff_r + 3'd1;
              if (roff_r == 3'd7) rvalid_r <= 1'b0;
              if ((served_r + 11'd1) >= len_r) begin
                rvalid_r <= 1'b0;
                st_r     <= rbusy_r ? R_DRAIN : R_DONE;
              end
            end
            if (tmo_hit_w) begin
              rbusy_r  <= 1'b0;
              rvalid_r <= 1'b0;
              fault_r  <= 1'b1;
              fcode_r  <= FAULT_RTMO_C;
              st_r     <= R_ERR;
            end
          end

          //! the builder took every byte it needs; the rest of the burst is
          //! swallowed so the bridge is never left holding a beat
          R_DRAIN: begin
            if (beat_w) begin
              if (mem_rsp_last_i || mem_rsp_err_i) begin
                rbusy_r <= 1'b0;
                st_r    <= R_DONE;
              end
            end else if (tmo_hit_w) begin
              rbusy_r <= 1'b0;
              st_r    <= R_DONE;
            end
          end

          R_DONE: ;   // idle until the next open_i

          //! R_ERR — sticky until the next response. The face is released so a
          //! µCPU parked on a dead buffer still retires its command.
          default: begin
            rvalid_r   <= 1'b0;
            sk_valid_r <= 1'b0;
            wr_ready_r <= 1'b1;
          end
        endcase
      end
    end
  end

endmodule : KL_aecp_resp_buf
`default_nettype wire
