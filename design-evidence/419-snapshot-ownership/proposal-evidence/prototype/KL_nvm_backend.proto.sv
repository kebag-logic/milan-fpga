/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  PROPOSAL PROTOTYPE, issue #419 round 3. NOT SHIPPING RTL. A copy of
//  hdl/milan/KL_nvm_backend.sv with the snapshot-ownership contract of
//  PROPOSAL.md applied; the module keeps its name so the co-simulation can
//  compile either the tracked file or this one behind the same wrapper.
//
//  THE CONTRACT ADDED HERE, in one paragraph. Every allocated record carries
//  an OPEN bit: set when a mutating operation on it is GRANTED, cleared only
//  when a whole-record WRITE on it completes with done and no error. A record
//  whose bit is set is not a completed record, whatever its bytes say. The
//  firmware captures the record area into a private buffer under a bounded
//  grant HOLD (mutating requests are deferred, never refused; reads are never
//  deferred), copies only records whose bit is clear, and CERTIFIES the copy:
//  the certificate is latched in hardware and is false if any mutating grant
//  happened between the arm and the certify. Only a certified capture may be
//  written to flash. The acknowledgement quotes the capture identity and
//  retires only the work captured at the arm; completions after the arm stay
//  owned by dirty_live. Producer-held changes (pend_i, a level) and open
//  records are never retired by an acknowledgement. nvm_dirty keeps its
//  section 9.1 meaning (committable image work no slot holds); accepted work
//  that is NOT yet in any verified slot for any other reason -- held by the
//  producer, or an open record -- is published on its OWN bit, nvm_pend (the
//  owner decision on issue #419, 2026-09-18). The manager alarm and a
//  reported flash failure revoke nvm_backed, as section 9.2 lists.
//
//  THE LOAD (revision b). RELOAD, the firmware's claim that the window now
//  holds a verified container it just loaded, is CHECKED here the way the
//  capture's certificate is: a load flag is armed by a re-base (a write to
//  the image base, length or a channel-map table) only while no mutating
//  operation is in flight, and any mutating grant after it clears the flag.
//  A RELOAD is accepted only with the flag set and only once per reset (the
//  boot load); a refused RELOAD changes nothing but its refusal bit. So an
//  accepted RELOAD never meets an operation that ended without closing its
//  record, and a record is never closed on device idle.
//
//  REVISION C, two bounds by construction. (1) "Once per reset" is no longer
//  keyed to an ACCEPTED load alone: the boot load is also over the first time
//  a device-face operation the load sequence did not bracket is granted on a
//  configured image (win_live_w), which is the restore walk's first read or
//  an enabled producer. So no sequence of boot outcomes and writer restarts
//  can let an accepted RELOAD close records or clear a dirty half once the
//  producer has been able to write the window. (2) An ARM is refused while a
//  mutating request this module already deferred still waits, so a request
//  is deferred by at most ONE capture and T_HOLD_MS_P bounds it across
//  chained captures.
//
//  File        : KL_nvm_backend.sv
//  Project     : Milan FPGA -- saved state and fast connect
//                (docs/design/SAVED_STATE_FASTCONNECT.md sections 4, 8, 9)
//
//  Description : THE DEVICE BEHIND THE PROCESSOR'S NVM PORT. KL_pp_nvm_port
//                (protocol-processor) frames one F07.8 record per operation
//                and streams it one byte per handshake toward a device face;
//                this module is that device. It keeps the persisted record
//                image in the reserved main-memory window (section 8.1), so a
//                record READ fetches bytes from the image, a WRITE stores them
//                and an ERASE fills the record's span with 0xFF. Nothing here
//                touches flash: the media is owned by firmware through the
//                LiteSPI master that already exists (section 3), and what
//                crosses the CSR face is the control tuple of section 8.2 --
//                the image base and length, the sequence number, the verdict
//                of the last slot the firmware validated, the heartbeat and
//                the commit bracket -- never record data.
//
//                WHERE A RECORD IS. record_id is decoded to an image byte
//                offset by the section 4.2 allocation: fixed blocks for the
//                fixed-length groups, and for the two channel-map groups a
//                per-port, per-direction {prefix, length} table the firmware
//                loads from the same overlay the descriptor image came from
//                (an input port and an output port of one ordinal carry
//                different cluster counts on the shipped 8x8 overlay, 8 and
//                17, so the two directions never share a table). Every group
//                after the channel maps sits at the SUM of the actual
//                preceding lengths, because KLJ2 section 6.1 concatenates
//                records with no padding.
//
//                WHAT IT DOES BEFORE FIRMWARE ARRIVES. Until the firmware has
//                written a non-zero image length, this module answers exactly
//                as the blank-flash responder it replaces did: reads return
//                0xFF, writes are accepted and discarded, erase completes. So
//                a build whose firmware has no writer yet behaves as today,
//                and PP_STAT keeps telling the truth about it (nvm_backed
//                stays 0). Once configured, a READ still answers 0xFF until
//                the firmware has marked the image VALID -- the section 6.2
//                acceptance order runs in firmware over the slot it copied
//                into the window, and a record must never be restored out of
//                an image nobody validated -- while WRITE and ERASE always
//                reach the image, because the processor commits records at
//                runtime and the firmware wraps them into a container later.
//
//                WHAT IT MAY CLAIM. nvm_backed_o is fabric-derived evidence
//                and never a knob: it sets on a firmware heartbeat or a
//                completed transaction, re-arms T-NVM-WRITER-ALIVE on each,
//                and is revoked when that deadline or T-NVM-COMMIT-TIMEOUT
//                expires. nvm_dirty_o says the image holds changes no slot
//                holds; nvm_stale_o says a loss has not been made good. The
//                three follow the next-state function of section 9.2 with
//                its two priorities written out, and section 9.3's
//                (backed=1, dirty=0, stale=1) row is unreachable in the state.
//
//                THE MEMORY FACE is the same contract as the response-buffer
//                master beside it (protocol_processor_top's banner): one
//                outstanding read burst of 64-bit beats carrying their lowest
//                byte address in bits [63:56] (big-endian lanes), and one
//                outstanding single-beat write, 8-byte aligned, strobe bit n
//                enabling byte n, committed by a one-cycle wr_done pulse
//                that may follow wr_ready in the same cycle (a posted bridge)
//                or any later one (an acknowledged bridge). A read fetches
//                the word that holds the byte and keeps it until the byte
//                stream leaves the word or anything writes, so consecutive
//                bytes of one record cost one bus read per eight.
//
//  Refusals    : an unallocated record_id, a span past the record, a span
//                past the configured image and a bus error each end the
//                operation with one dev_err pulse and no further traffic.
//                The port never range-checks record_id against its region
//                (design page section 13), so this module does.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_nvm_backend #(
    //! core clock frequency in Hz; the millisecond tick the deadlines
    //! count in is derived from it
    parameter int unsigned CLK_HZ_P       = 125_000_000,
    //! shape: the section 4.2 allocation's per-group occupancy, defaulted
    //! to the ax7101_8x8 header's values (KL_pp_shadow passes the live ones)
    parameter int unsigned N_STREAM_IN_P  = 9,
    parameter int unsigned N_STREAM_OUT_P = 9,
    parameter int unsigned N_SPORT_IN_P   = 8,
    parameter int unsigned N_SPORT_OUT_P  = 8,
    parameter int unsigned N_AUDIO_UNIT_P = 1,
    parameter int unsigned N_CLK_DOM_P    = 1,
    parameter int unsigned N_NAME_P       = 99,
    //! design page section 9.4 deadlines, in milliseconds
    parameter int unsigned T_ALIVE_MS_P   = 2000,
    parameter int unsigned T_COMMIT_MS_P  = 8000,
    //! the capture hold bound: the longest a mutating producer request is
    //! deferred by one capture, in milliseconds (PROPOSAL.md section 5)
    parameter int unsigned T_HOLD_MS_P    = 50,
    //! width of the capture identity an acknowledgement quotes
    parameter int unsigned CAP_ID_W_P     = 16
) (
    input  wire         clk_i,          //! core clock
    input  wire         rst_n,          //! synchronous active-low reset

    //! ---- device face: target of KL_pp_nvm_port's initiator ----
    input  wire         dev_req_i,      //! command request, held until dev_gnt_o
    output logic        dev_gnt_o,      //! command accepted (one cycle)
    input  wire  [1:0]  dev_op_i,       //! READ / WRITE / ERASE_REGION
    input  wire  [7:0]  dev_region_i,   //! region id = F07.8 record_id
    input  wire  [15:0] dev_offset_i,   //! byte offset inside the record
    input  wire  [15:0] dev_len_i,      //! byte count (ERASE: 0 = whole record)
    input  wire         dev_wvalid_i,   //! write byte present
    output logic        dev_wready_o,   //! this module accepts the write byte
    input  wire  [7:0]  dev_wdata_i,    //! write byte
    output logic        dev_rvalid_o,   //! read byte present
    output logic [7:0]  dev_rdata_o,    //! read byte
    input  wire         dev_rready_i,   //! initiator accepts the read byte
    output logic        dev_busy_o,     //! command in flight
    output logic        dev_done_o,     //! one-cycle pulse: complete
    output logic        dev_err_o,      //! one-cycle pulse: failed

    //! ---- main-memory master into the reserved ppmem window (section 8.1) --
    //! Same contract as the response-buffer master: see the banner.
    output logic        mem_req_valid_o,  //! read request, held until ready
    input  wire         mem_req_ready_i,  //! bridge accepts the request
    output logic [31:0] mem_req_addr_o,   //! byte address, 8-byte aligned
    output logic [8:0]  mem_req_beats_o,  //! 64-bit beats in the burst (1)
    input  wire         mem_rsp_valid_i,  //! response beat present
    output logic        mem_rsp_ready_o,  //! this module takes the beat
    input  wire  [63:0] mem_rsp_data_i,   //! beat data, big-endian byte lane
    input  wire         mem_rsp_last_i,   //! final beat of the burst
    input  wire         mem_rsp_err_i,    //! read failed -- abort the op
    output logic        mem_wr_valid_o,   //! write presented, held until ready
    input  wire         mem_wr_ready_i,   //! bridge accepts the write
    output logic [31:0] mem_wr_addr_o,    //! byte address, 8-byte aligned
    output logic [63:0] mem_wr_data_o,    //! lane data (byte replicated)
    output logic [7:0]  mem_wr_strb_o,    //! per-byte enable, bit n = byte n
    input  wire         mem_wr_done_i,    //! write committed (one-cycle pulse)
    input  wire         mem_wr_err_i,     //! ... and it failed

    //! ---- control CSRs (section 8.2: a control tuple, never a data window) -
    //! [5] selects the channel-map tables, [4] the DIRECTION inside them
    //! (0 = input group 0x60, 1 = output group 0x70) and [3:0] the port.
    //! With [5] clear, [4:0] is the register index (R_* below).
    input  wire         csr_sel_i,      //! CSR access
    input  wire         csr_we_i,       //! 1 = write
    input  wire  [5:0]  csr_addr_i,     //! see above
    input  wire  [31:0] csr_wdata_i,    //! write data
    output logic [31:0] csr_rdata_o,    //! read data

    //! ---- fabric evidence ----
    //! A LEVEL, not an event: 1 while the producer holds an accepted change
    //! it has not yet written through the device face (the AECP store's
    //! sticky level today; plus the binding manager's unflushed state once
    //! donor scope D1 exports it). No acknowledgement retires it.
    input  wire         pend_i,
    //! the producer's bounded-retry exhaustion alarm (sticky in the donor
    //! until reset): section 9.2 lists it as a revocation cause
    input  wire         alarm_i,

    //! ---- published status (section 9.1) ----
    output logic        nvm_backed_o,   //! live: a writer answered in time
    output logic        nvm_dirty_o,    //! committable image work no slot holds
    output logic        nvm_stale_o,    //! a loss that has not been made good
    output logic [3:0]  nvm_verdict_o,  //! section 6.2 verdict of the last image
    output logic        img_valid_o,    //! firmware validated the image in the window
    //! THE PENDING BIT: accepted work that no verified slot represents and
    //! nvm_dirty does not report -- producer-held changes, or an open record
    output logic        nvm_pend_o,
    output logic        nvm_unres_o     //! diagnostic: at least one record is open
);

  // ---- device-face op codes (2'b11 reserved) -----------------------------
  localparam logic [1:0] OP_READ_C  = 2'd0;
  localparam logic [1:0] OP_WRITE_C = 2'd1;
  localparam logic [1:0] OP_ERASE_C = 2'd2;

  localparam int unsigned REC_HDR_C = 8;     // F07.8 framing bytes
  localparam int unsigned NAME_C    = 64;    // one AEM string, section 4.2

  // ---- the section 4.2 id blocks -----------------------------------------
  localparam int unsigned ID_CFG_C   = 'h00;
  localparam int unsigned ID_SUID_C  = 'h01;
  localparam int unsigned ID_RATE_C  = 'h02;
  localparam int unsigned ID_CLKS_C  = 'h0A;
  localparam int unsigned ID_MCR_C   = 'h12;
  localparam int unsigned ID_BIND_C  = 'h20;
  localparam int unsigned ID_FMTI_C  = 'h30;
  localparam int unsigned ID_FMTO_C  = 'h40;
  localparam int unsigned ID_PTOF_C  = 'h50;
  localparam int unsigned ID_MAPI_C  = 'h60;
  localparam int unsigned ID_MAPO_C  = 'h70;
  localparam int unsigned ID_NAME_C  = 'h80;

  // ---- per-group record size, header included ----------------------------
  //! The two channel-map groups are absent from this list ON PURPOSE: their
  //! record length is per port, not per group, and lives in the tables below.
  localparam int unsigned SZ_CFG_C  = REC_HDR_C + 2;
  localparam int unsigned SZ_SUID_C = REC_HDR_C + 8;
  localparam int unsigned SZ_RATE_C = REC_HDR_C + 4;
  localparam int unsigned SZ_CLKS_C = REC_HDR_C + 2;
  localparam int unsigned SZ_MCR_C  = REC_HDR_C + 66;
  localparam int unsigned SZ_BIND_C = REC_HDR_C + 20;
  localparam int unsigned SZ_FMT_C  = REC_HDR_C + 8;
  localparam int unsigned SZ_PTOF_C = REC_HDR_C + 4;
  localparam int unsigned SZ_NAME_C = REC_HDR_C + NAME_C;

  // ---- image byte bases: records are concatenated in ascending record_id --
  //! Constant up to the first channel-map group, because every group before it
  //! is fixed-length. Everything after it is derived at run time from the
  //! loaded lengths (b_mapo_w, b_name_w below).
  localparam int unsigned B_CFG_C  = 0;
  localparam int unsigned B_SUID_C = B_CFG_C  + SZ_CFG_C;
  localparam int unsigned B_RATE_C = B_SUID_C + SZ_SUID_C;
  localparam int unsigned B_CLKS_C = B_RATE_C + N_AUDIO_UNIT_P * SZ_RATE_C;
  localparam int unsigned B_MCR_C  = B_CLKS_C + N_CLK_DOM_P    * SZ_CLKS_C;
  localparam int unsigned B_BIND_C = B_MCR_C  + N_CLK_DOM_P    * SZ_MCR_C;
  localparam int unsigned B_FMTI_C = B_BIND_C + N_STREAM_IN_P  * SZ_BIND_C;
  localparam int unsigned B_FMTO_C = B_FMTI_C + N_STREAM_IN_P  * SZ_FMT_C;
  localparam int unsigned B_PTOF_C = B_FMTO_C + N_STREAM_OUT_P * SZ_FMT_C;
  localparam int unsigned B_MAPI_C = B_PTOF_C + N_STREAM_OUT_P * SZ_PTOF_C;

  //! The id comparisons run in 9 bits: a block that ends exactly at 0x100
  //! (128 names) must not wrap to 0 and vanish, which an 8-bit sum would do.
  // ---- elaboration contract: what this shape refuses ---------------------
  //! Every bound is an id-block capacity of the section 4.2 allocation or a
  //! counter width below, so a shape that cannot be addressed is refused when
  //! the parameters bind rather than aliased into a neighbouring block.
  //! ONE format string per $error: later arguments print as values.
  if (N_STREAM_IN_P < 1 || N_STREAM_IN_P > 16 || N_STREAM_OUT_P < 1 || N_STREAM_OUT_P > 16) begin : g_refuse_streams
    $error("KL_nvm_backend: N_STREAM_IN_P=%0d / N_STREAM_OUT_P=%0d outside 1..16: the BINDING, FORMAT and OFFSET blocks hold sixteen ids each (0x20, 0x30, 0x40, 0x50).",
           N_STREAM_IN_P, N_STREAM_OUT_P);
  end else if (N_SPORT_IN_P < 1 || N_SPORT_IN_P > 16 || N_SPORT_OUT_P < 1 || N_SPORT_OUT_P > 16) begin : g_refuse_sports
    $error("KL_nvm_backend: N_SPORT_IN_P=%0d / N_SPORT_OUT_P=%0d outside 1..16: the channel-map blocks hold sixteen ids each (0x60, 0x70) and the tables are indexed by csr_addr_i[3:0].",
           N_SPORT_IN_P, N_SPORT_OUT_P);
  end else if (N_AUDIO_UNIT_P < 1 || N_AUDIO_UNIT_P > 8 || N_CLK_DOM_P < 1 || N_CLK_DOM_P > 8) begin : g_refuse_units
    $error("KL_nvm_backend: N_AUDIO_UNIT_P=%0d / N_CLK_DOM_P=%0d outside 1..8: the RATE block (0x02) and the CLOCK_SOURCE block (0x0A) hold eight ids each.",
           N_AUDIO_UNIT_P, N_CLK_DOM_P);
  end else if (N_NAME_P < 1 || N_NAME_P > 128) begin : g_refuse_names
    $error("KL_nvm_backend: N_NAME_P=%0d outside 1..128: the NAME block is 0x80..0xFF.",
           N_NAME_P);
  end else if (CLK_HZ_P < 1000) begin : g_refuse_clock
    $error("KL_nvm_backend: CLK_HZ_P=%0d is below 1 kHz, so no millisecond tick can be derived for the section 9.4 deadlines.",
           CLK_HZ_P);
  end else if (T_ALIVE_MS_P < 1 || T_ALIVE_MS_P > 65535 || T_COMMIT_MS_P < 1 || T_COMMIT_MS_P > 65535) begin : g_refuse_deadlines
    $error("KL_nvm_backend: T_ALIVE_MS_P=%0d / T_COMMIT_MS_P=%0d outside 1..65535: the deadline down-counters are sixteen bits wide.",
           T_ALIVE_MS_P, T_COMMIT_MS_P);
  end else if (T_HOLD_MS_P < 1 || T_HOLD_MS_P >= T_COMMIT_MS_P) begin : g_refuse_hold
    $error("KL_nvm_backend: T_HOLD_MS_P=%0d must be at least 1 and below T_COMMIT_MS_P=%0d: the hold bounds a copy, never a flash transaction.",
           T_HOLD_MS_P, T_COMMIT_MS_P);
  end else if (CAP_ID_W_P < 2 || CAP_ID_W_P > 16) begin : g_refuse_capid
    $error("KL_nvm_backend: CAP_ID_W_P=%0d outside 2..16: the identity rides the acknowledgement word's upper half.",
           CAP_ID_W_P);
  end

  localparam int unsigned IDW_C = 9;

  // =======================================================================
  //  Region decode: record_id -> {image byte base, record byte length}
  // =======================================================================
  //! Per-port channel-map prefix and length, loaded by firmware, DIRECTION
  //! DISTINCT (see the banner). The prefix is the running sum of the
  //! preceding lengths INSIDE the group.
  logic [15:0] mapi_pref_r [0:N_SPORT_IN_P-1];
  logic [15:0] mapi_len_r  [0:N_SPORT_IN_P-1];
  logic [15:0] mapo_pref_r [0:N_SPORT_OUT_P-1];
  logic [15:0] mapo_len_r  [0:N_SPORT_OUT_P-1];

  localparam int unsigned MAPI_IW_C = (N_SPORT_IN_P  > 1)
                                    ? $clog2(N_SPORT_IN_P)  : 1;
  localparam int unsigned MAPO_IW_C = (N_SPORT_OUT_P > 1)
                                    ? $clog2(N_SPORT_OUT_P) : 1;

  logic [17:0] rec_base_w;
  logic [11:0] rec_len_w;
  logic        rec_hit_w;
  logic [MAPI_IW_C-1:0] mapi_idx_w;
  logic [MAPO_IW_C-1:0] mapo_idx_w;
  logic [17:0] b_mapo_w, b_name_w;
  logic [IDW_C-1:0] region_w;

  assign region_w = {1'b0, dev_region_i};

  //! Only ever consumed inside the guarded branch that proves the id is in
  //! the group, so a truncated value outside it cannot reach an output.
  assign mapi_idx_w = MAPI_IW_C'(dev_region_i - 8'(ID_MAPI_C));
  assign mapo_idx_w = MAPO_IW_C'(dev_region_i - 8'(ID_MAPO_C));

  //! A group base is the SUM of the preceding group's actual record lengths.
  //! The running prefix already carries that sum, so the span of a group is
  //! its last port's prefix plus that port's length: one adder, and it cannot
  //! disagree with the table the decode reads.
  assign b_mapo_w = 18'(B_MAPI_C)
                  + 18'(mapi_pref_r[MAPI_IW_C'(N_SPORT_IN_P  - 1)])
                  + 18'(mapi_len_r [MAPI_IW_C'(N_SPORT_IN_P  - 1)]);
  assign b_name_w = b_mapo_w
                  + 18'(mapo_pref_r[MAPO_IW_C'(N_SPORT_OUT_P - 1)])
                  + 18'(mapo_len_r [MAPO_IW_C'(N_SPORT_OUT_P - 1)]);

  always_comb begin
    rec_base_w = 18'd0;
    rec_len_w  = 12'd0;
    rec_hit_w  = 1'b0;
    if (region_w == IDW_C'(ID_CFG_C)) begin
      rec_base_w = 18'(B_CFG_C);
      rec_len_w  = 12'(SZ_CFG_C);
      rec_hit_w  = 1'b1;
    end else if (region_w == IDW_C'(ID_SUID_C)) begin
      rec_base_w = 18'(B_SUID_C);
      rec_len_w  = 12'(SZ_SUID_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_RATE_C)
              && region_w <  IDW_C'(ID_RATE_C + N_AUDIO_UNIT_P)) begin
      rec_base_w = 18'(B_RATE_C) + 18'(dev_region_i - 8'(ID_RATE_C)) * 18'(SZ_RATE_C);
      rec_len_w  = 12'(SZ_RATE_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_CLKS_C)
              && region_w <  IDW_C'(ID_CLKS_C + N_CLK_DOM_P)) begin
      rec_base_w = 18'(B_CLKS_C) + 18'(dev_region_i - 8'(ID_CLKS_C)) * 18'(SZ_CLKS_C);
      rec_len_w  = 12'(SZ_CLKS_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_MCR_C)
              && region_w <  IDW_C'(ID_MCR_C + N_CLK_DOM_P)) begin
      rec_base_w = 18'(B_MCR_C) + 18'(dev_region_i - 8'(ID_MCR_C)) * 18'(SZ_MCR_C);
      rec_len_w  = 12'(SZ_MCR_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_BIND_C)
              && region_w <  IDW_C'(ID_BIND_C + N_STREAM_IN_P)) begin
      rec_base_w = 18'(B_BIND_C) + 18'(dev_region_i - 8'(ID_BIND_C)) * 18'(SZ_BIND_C);
      rec_len_w  = 12'(SZ_BIND_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_FMTI_C)
              && region_w <  IDW_C'(ID_FMTI_C + N_STREAM_IN_P)) begin
      rec_base_w = 18'(B_FMTI_C) + 18'(dev_region_i - 8'(ID_FMTI_C)) * 18'(SZ_FMT_C);
      rec_len_w  = 12'(SZ_FMT_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_FMTO_C)
              && region_w <  IDW_C'(ID_FMTO_C + N_STREAM_OUT_P)) begin
      rec_base_w = 18'(B_FMTO_C) + 18'(dev_region_i - 8'(ID_FMTO_C)) * 18'(SZ_FMT_C);
      rec_len_w  = 12'(SZ_FMT_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_PTOF_C)
              && region_w <  IDW_C'(ID_PTOF_C + N_STREAM_OUT_P)) begin
      rec_base_w = 18'(B_PTOF_C) + 18'(dev_region_i - 8'(ID_PTOF_C)) * 18'(SZ_PTOF_C);
      rec_len_w  = 12'(SZ_PTOF_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_MAPI_C)
              && region_w <  IDW_C'(ID_MAPI_C + N_SPORT_IN_P)) begin
      rec_base_w = 18'(B_MAPI_C) + 18'(mapi_pref_r[mapi_idx_w]);
      rec_len_w  = 12'(mapi_len_r[mapi_idx_w]);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_MAPO_C)
              && region_w <  IDW_C'(ID_MAPO_C + N_SPORT_OUT_P)) begin
      rec_base_w = b_mapo_w + 18'(mapo_pref_r[mapo_idx_w]);
      rec_len_w  = 12'(mapo_len_r[mapo_idx_w]);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_NAME_C)
              && region_w <  IDW_C'(ID_NAME_C + N_NAME_P)) begin
      rec_base_w = b_name_w + 18'(dev_region_i - 8'(ID_NAME_C)) * 18'(SZ_NAME_C);
      rec_len_w  = 12'(SZ_NAME_C);
      rec_hit_w  = 1'b1;
    end
  end

  // =======================================================================
  //  Control CSRs
  // =======================================================================
  localparam logic [4:0] R_IMG_BASE_C = 5'd0;
  localparam logic [4:0] R_IMG_LEN_C  = 5'd1;
  localparam logic [4:0] R_SEQ_C      = 5'd2;
  localparam logic [4:0] R_STAT_C     = 5'd3;
  localparam logic [4:0] R_ACK_C      = 5'd4;
  //! PROTOTYPE: the identity of the capture an acknowledgement must quote
  localparam logic [4:0] R_CAPID_C    = 5'd5;
  //! PROTOTYPE: the ownership vector, 32 record ids per word, words 8..15
  localparam logic [4:0] R_OWN0_C     = 5'd8;
  //! PROTOTYPE: the status word's feature tag, [31:24]
  localparam logic [7:0] CAP_TAG_C    = 8'hC3;
  //! the writer's own transaction verdicts (design page section 6.2)
  localparam logic [3:0] VD_ERASE_C   = 4'd11;
  localparam logic [3:0] VD_VERIFY_C  = 4'd13;

  logic [31:0] img_base_r;
  logic [31:0] img_len_r;
  logic [31:0] seq_r;
  logic [3:0]  verdict_r;
  logic        img_valid_r;
  logic        backed_r, stale_r, ever_backed_r;
  logic        reg_we_w, hb_kick_w, commit_ack_w, commit_start_w;
  logic        img_cfg_w, img_live_w;
  //! PROTOTYPE strobes and events
  logic        arm_w, cert_w, release_w, reload_w, reconf_w, map_we_w, fail_rep_w;
  //! PROTOTYPE (revision b): the RELOAD strobe after the backend's check
  logic        reload_ok_w;
  logic [CAP_ID_W_P-1:0] ack_id_w;

  assign reg_we_w       = csr_sel_i & csr_we_i & ~csr_addr_i[5];
  assign map_we_w       = csr_sel_i & csr_we_i &  csr_addr_i[5];
  assign hb_kick_w      = reg_we_w & (csr_addr_i[4:0] == R_ACK_C) & csr_wdata_i[0];
  assign commit_ack_w   = reg_we_w & (csr_addr_i[4:0] == R_ACK_C) & csr_wdata_i[1];
  assign commit_start_w = reg_we_w & (csr_addr_i[4:0] == R_ACK_C) & csr_wdata_i[2];
  assign arm_w          = reg_we_w & (csr_addr_i[4:0] == R_ACK_C) & csr_wdata_i[3];
  assign cert_w         = reg_we_w & (csr_addr_i[4:0] == R_ACK_C) & csr_wdata_i[4];
  assign release_w      = reg_we_w & (csr_addr_i[4:0] == R_ACK_C) & csr_wdata_i[5];
  assign reload_w       = reg_we_w & (csr_addr_i[4:0] == R_ACK_C) & csr_wdata_i[6];
  assign ack_id_w       = csr_wdata_i[16 +: CAP_ID_W_P];
  //! the image moved or changed shape: every record is unknown again
  assign reconf_w       = (reg_we_w & ((csr_addr_i[4:0] == R_IMG_BASE_C)
                                     | (csr_addr_i[4:0] == R_IMG_LEN_C)))
                        | map_we_w;
  //! a transaction verdict the writer reports (VD_ERASE, VD_PROGRAM,
  //! VD_VERIFY): section 9.2 lists it as a revocation cause of its own
  assign fail_rep_w     = reg_we_w & (csr_addr_i[4:0] == R_STAT_C)
                        & (csr_wdata_i[3:0] >= VD_ERASE_C)
                        & (csr_wdata_i[3:0] <= VD_VERIFY_C);
  //! Configured: the firmware has told this module where the image is. Live:
  //! configured AND validated, the only state in which a READ may serve image
  //! bytes rather than blank flash.
  assign img_cfg_w  = (img_len_r != 32'd0);
  assign img_live_w = img_cfg_w & img_valid_r;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      img_base_r  <= 32'd0;
      img_len_r   <= 32'd0;
      seq_r       <= 32'd0;
      verdict_r   <= 4'd0;
      img_valid_r <= 1'b0;
    end else if (reg_we_w) begin
      case (csr_addr_i[4:0])
        //! moving the image invalidates whatever validation the old one had
        R_IMG_BASE_C: begin img_base_r <= csr_wdata_i; img_valid_r <= 1'b0; end
        R_IMG_LEN_C:  begin img_len_r  <= csr_wdata_i; img_valid_r <= 1'b0; end
        R_SEQ_C:      seq_r <= csr_wdata_i;
        //! [3:0] the section 6.2 verdict of the image the firmware last
        //! offered, [4] whether that image is the one in the window and it
        //! passed: the firmware's statement, published as evidence only
        R_STAT_C:     begin verdict_r <= csr_wdata_i[3:0]; img_valid_r <= csr_wdata_i[4]; end
        default:      ;
      endcase
    end
  end

  //! The two channel-map tables: {length, prefix} per port and per direction,
  //! firmware-loaded. csr_addr_i[4] picks the direction.
  always_ff @(posedge clk_i) begin
    if (csr_sel_i && csr_we_i && csr_addr_i[5]) begin
      if (!csr_addr_i[4]) begin
        if (32'(csr_addr_i[3:0]) < 32'(N_SPORT_IN_P)) begin
          mapi_pref_r[MAPI_IW_C'(csr_addr_i[3:0])] <= csr_wdata_i[15:0];
          mapi_len_r [MAPI_IW_C'(csr_addr_i[3:0])] <= csr_wdata_i[31:16];
        end
      end else begin
        if (32'(csr_addr_i[3:0]) < 32'(N_SPORT_OUT_P)) begin
          mapo_pref_r[MAPO_IW_C'(csr_addr_i[3:0])] <= csr_wdata_i[15:0];
          mapo_len_r [MAPO_IW_C'(csr_addr_i[3:0])] <= csr_wdata_i[31:16];
        end
      end
    end
  end

  logic commit_busy_r;
  logic dev_busy_w;

  // -----------------------------------------------------------------------
  //  PROTOTYPE: capture state, ownership vector and the dirty halves
  // -----------------------------------------------------------------------
  logic                  cap_open_r, cap_hold_r, cap_valid_r, cap_cert_r;
  logic                  ack_ref_r, arm_ref_r;
  logic [CAP_ID_W_P-1:0] cap_id_r;
  localparam int unsigned HOLD_W_C = $clog2(T_HOLD_MS_P + 1);
  logic [HOLD_W_C-1:0]   hold_r;
  logic                  dirty_live_r, dirty_cap_r, pend_r;
  logic [255:0]          open_r;
  logic                  unres_w, dirty_img_w;
  logic                  arm_ok_w, cert_ok_w, ack_ok_w, close_w, drop_w;
  logic                  hold_exp_w, void_grant_w, gnt_opmut_w, rec_close_w;
  //! latched at the grant: which record the operation owns, whether it will
  //! present memory writes, and whether it rewrites the WHOLE record
  logic [7:0]            op_region_r;
  logic                  op_mut_r, op_full_r;
  //! the grant's set, applied from op_region_r one cycle later so that one
  //! comparator per record serves the set and the close. Exact from the first
  //! cycle after an arm: the arm's own edge defers every mutating request
  //! (gnt_now_w below), so the last grant an arm can follow is on the edge
  //! before it, and that grant's set lands on the arm edge
  logic                  set_q_r;
  //! the load (revision b): ld_ok_r, armed by a re-base with no mutating
  //! operation in flight and cleared by every mutating grant after it;
  //! ld_pend_r, A BOOT WINDOW LOAD MAY STILL BE ACCEPTED (revision c: it
  //! falls on an accepted RELOAD and the first time the window goes live);
  //! rl_ref_r, the last RELOAD strobe was refused
  logic                  ld_ok_r, ld_pend_r, rl_ref_r;
  //! REVISION D: a RELOAD HAS BEEN ACCEPTED since reset. Set by an accepted
  //! RELOAD, cleared only by reset, published at PP_NVM_STAT[2]. No capture
  //! is armed while it is 0, so a boot whose window load was never accepted
  //! can write no slot and retire nothing
  logic                  ld_acc_r;
  logic                  inflight_w, win_live_w;
  //! revision c: a mutating request a capture DEFERRED, registered. It may
  //! not be deferred a second time by a later capture, so an arm is refused
  //! while it waits and the bound of one hold holds per request
  logic                  mut_wait_w, mut_defer_r;
  //! THE PENDING BIT, one wire for the port and the status word's [22]
  logic                  pend_w;

  assign unres_w     = |open_r;
  assign dirty_img_w = dirty_live_r | dirty_cap_r;

  always_comb begin
    if (csr_addr_i[5]) begin
      if (!csr_addr_i[4]) begin
        csr_rdata_o = {mapi_len_r [MAPI_IW_C'(csr_addr_i[3:0])],
                       mapi_pref_r[MAPI_IW_C'(csr_addr_i[3:0])]};
      end else begin
        csr_rdata_o = {mapo_len_r [MAPO_IW_C'(csr_addr_i[3:0])],
                       mapo_pref_r[MAPO_IW_C'(csr_addr_i[3:0])]};
      end
    end else if (csr_addr_i[4:3] == R_OWN0_C[4:3]) begin
      //! the ownership vector: word 8 + k holds record ids 32k .. 32k + 31
      csr_rdata_o = open_r[32 * csr_addr_i[2:0] +: 32];
    end else begin
      case (csr_addr_i[4:0])
        R_IMG_BASE_C: csr_rdata_o = img_base_r;
        R_IMG_LEN_C:  csr_rdata_o = img_len_r;
        R_SEQ_C:      csr_rdata_o = seq_r;
        //! the status word: [31:24] the capture-contract tag, [23] unres,
        //! [22] nvm_pend (the pending bit, the same wire as the port),
        //! [21] arm refused, [20] ack refused, [19] certified, [18] valid,
        //! [17] hold, [16] open, then the tracked layout below with [8] now
        //! the COMMITTABLE image work that drives a commit, and three load
        //! bits in positions the tracked layout keeps zero: [11] the last
        //! RELOAD was refused, [3] load pending (a boot window load may
        //! still be accepted), [2] load accepted (a RELOAD has been
        //! accepted since reset; without it no capture is armed)
        R_STAT_C:     csr_rdata_o = {CAP_TAG_C, unres_w, pend_w, arm_ref_r,
                                     ack_ref_r, cap_cert_r, cap_valid_r,
                                     cap_hold_r, cap_open_r,
                                     verdict_r, rl_ref_r, commit_busy_r,
                                     nvm_stale_o, dirty_img_w, img_valid_r,
                                     backed_r, img_cfg_w, dev_busy_w,
                                     ld_pend_r, ld_acc_r, 2'd0};
        R_CAPID_C:    csr_rdata_o = 32'(cap_id_r);
        default:      csr_rdata_o = 32'd0;
      endcase
    end
  end

  // =======================================================================
  //  Deadlines (section 9.4): a millisecond tick and two down-counters
  // =======================================================================
  localparam int unsigned MS_DIV_C = (CLK_HZ_P >= 1000) ? CLK_HZ_P / 1000 : 1;
  localparam int unsigned MS_W_C   = (MS_DIV_C > 1) ? $clog2(MS_DIV_C) : 1;

  logic [MS_W_C-1:0] ms_div_r;
  logic              ms_tick_w;
  logic [15:0]       alive_r;
  logic [15:0]       commit_r;

  assign ms_tick_w = (ms_div_r == '0);

  always_ff @(posedge clk_i) begin
    if (!rst_n) ms_div_r <= MS_W_C'(MS_DIV_C - 1);
    else        ms_div_r <= ms_tick_w ? MS_W_C'(MS_DIV_C - 1) : ms_div_r - 1'b1;
  end

  // -----------------------------------------------------------------------
  //  Section 9.2, as ONE next-state function with the priorities written out.
  //  PROTOTYPE: the loss set gains the two causes the page lists and the
  //  tracked module lacked (a reported flash failure and the manager alarm),
  //  and the recovery arm reads the COMPOSITE next dirty.
  // -----------------------------------------------------------------------
  logic alive_exp_w, commit_exp_w, loss_ev_w, loss_w;
  logic backed_n_w, stale_n_w, comp_n_w;
  logic dirty_live_n_w, dirty_cap_n_w;

  //! A deadline expires on the tick that would take it from 1 to 0. A
  //! heartbeat re-arms the liveness deadline instead of letting it expire;
  //! a start, an acknowledgement or a release preempts the commit deadline.
  assign alive_exp_w  = ms_tick_w & (alive_r == 16'd1) & ~hb_kick_w;
  assign commit_exp_w = commit_busy_r & ms_tick_w & (commit_r == 16'd1)
                        & ~commit_start_w & ~ack_ok_w & ~release_w;

  //! A LOSS is a deadline expiring, a reported flash transaction failure or
  //! the manager alarm, after a writer had once been live. The alarm is a
  //! LEVEL (sticky in the donor until reset), so it holds backed at 0 until
  //! reset: it is the only evidence of a producer change abandoned before
  //! any record was granted.
  assign loss_ev_w = alive_exp_w | commit_exp_w | fail_rep_w | alarm_i;
  assign loss_w    = loss_ev_w & ever_backed_r;

  //! PRIORITY: a loss in the same cycle as a heartbeat wins.
  assign backed_n_w = loss_ev_w ? 1'b0
                    : hb_kick_w ? 1'b1
                                : backed_r;

  //! RECOVERY on the NEXT nvm_dirty, exactly section 9.2's rule: writer
  //! live again AND no committable image work outstanding. Work the pending
  //! bit reports does not hold stale (the owner decision keeps the two
  //! reports separate); a reader of durability reads nvm_pend beside it.
  assign comp_n_w  = dirty_live_n_w | dirty_cap_n_w;
  assign stale_n_w = loss_w                   ? 1'b1
                   : (backed_n_w & ~comp_n_w) ? 1'b0
                                              : stale_r;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      alive_r       <= 16'd0;
      commit_r      <= 16'd0;
      commit_busy_r <= 1'b0;
      backed_r      <= 1'b0;
      stale_r       <= 1'b0;
      ever_backed_r <= 1'b0;
    end else begin
      // liveness: the heartbeat re-arms the alive deadline
      if (hb_kick_w) begin
        alive_r       <= 16'(T_ALIVE_MS_P);
        ever_backed_r <= 1'b1;
      end else if (ms_tick_w && (alive_r != 16'd0)) begin
        alive_r <= alive_r - 16'd1;
      end

      // the commit deadline: armed at start, disarmed by the acknowledgement,
      // by a release, or by anything that re-bases the image
      if (commit_start_w) begin
        commit_r      <= 16'(T_COMMIT_MS_P);
        commit_busy_r <= 1'b1;
      end else if (ack_ok_w || release_w || reload_ok_w || reconf_w) begin
        commit_busy_r <= 1'b0;
      end else if (commit_busy_r && ms_tick_w && (commit_r != 16'd0)) begin
        commit_r <= commit_r - 16'd1;
        if (commit_r == 16'd1) commit_busy_r <= 1'b0;
      end

      backed_r <= backed_n_w;
      stale_r  <= stale_n_w;
    end
  end

  // -----------------------------------------------------------------------
  //  PROTOTYPE: the capture machine. ONE capture at a time; its identity
  //  advances only on an accepted arm, so it names captures, not attempts.
  // -----------------------------------------------------------------------
  //! an ACCEPTED reload and reconf end any capture; a refused reload changes
  //! nothing; a lapsed commit deadline does NOT (design page section 16: a
  //! late-but-valid completion is accepted as data and does not by itself
  //! resurrect nvm_backed)
  logic void_hard_w;
  assign void_hard_w = reload_ok_w | reconf_w;
  //! REVISION C: an ARM is REFUSED while a mutating request this module
  //! already deferred is still waiting for its grant. The request takes the
  //! cycle the hold drops instead, and the writer re-arms at its next
  //! service call, so one request is deferred by AT MOST ONE capture and
  //! the T_HOLD_MS_P bound holds by construction across chained captures,
  //! not by a property of the writer's timing.
  //! REVISION D: and only once a RELOAD HAS BEEN ACCEPTED since reset
  //! (ld_acc_r). img_valid_r is the writer's claim about the window; this
  //! term is the backend's own record of having validated one, so a boot
  //! whose window load was never accepted captures nothing however the
  //! writer behaves, and no acknowledgement in it can retire anything.
  assign arm_ok_w    = arm_w & img_cfg_w & img_valid_r & ~cap_open_r & ~void_hard_w
                     & ~mut_defer_r & ld_acc_r;
  assign hold_exp_w  = cap_hold_r & ms_tick_w & (hold_r == HOLD_W_C'(1));
  //! a mutating grant between the arm and the certificate: only reachable
  //! after the hold lapsed, and it makes every copy taken so far suspect
  assign void_grant_w = gnt_opmut_w & cap_open_r & ~cap_cert_r;
  assign cert_ok_w   = cert_w & cap_open_r & ~cap_cert_r & cap_valid_r
                     & ~void_grant_w & ~void_hard_w;
  assign ack_ok_w    = commit_ack_w & cap_open_r & cap_cert_r & cap_valid_r
                     & (ack_id_w == cap_id_r) & ~void_hard_w;
  //! an acknowledgement that quotes ANOTHER capture's identity names nothing
  //! this module holds: it is refused and changes nothing else. One that
  //! quotes this capture ends it, accepted or not.
  assign close_w     = cap_open_r & ((commit_ack_w & (ack_id_w == cap_id_r))
                                     | release_w | void_hard_w);
  //! closing without an accepted acknowledgement hands the captured work
  //! back to dirty_live: nothing a failed attempt covered is forgotten
  assign drop_w      = close_w & ~ack_ok_w;

  //! the dirty halves. dirty_live is every record COMPLETION the current
  //! capture does not hold; dirty_cap is what the open capture holds. An
  //! acknowledgement reaches only dirty_cap, so work completing before, on
  //! or after its edge is never retired by it. A completion on the arm edge
  //! stays live (it may or may not be in the copy; one extra commit).
  assign dirty_live_n_w = rec_close_w ? 1'b1
                        : reload_ok_w ? 1'b0
                        : arm_ok_w    ? 1'b0
                        : drop_w      ? (dirty_live_r | dirty_cap_r)
                                      : dirty_live_r;
  assign dirty_cap_n_w  = reload_ok_w        ? 1'b0
                        : arm_ok_w           ? dirty_live_r
                        : (ack_ok_w | drop_w) ? 1'b0
                                             : dirty_cap_r;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      cap_open_r   <= 1'b0;
      cap_hold_r   <= 1'b0;
      cap_valid_r  <= 1'b0;
      cap_cert_r   <= 1'b0;
      cap_id_r     <= '0;
      hold_r       <= '0;
      ack_ref_r    <= 1'b0;
      arm_ref_r    <= 1'b0;
      dirty_live_r <= 1'b0;
      dirty_cap_r  <= 1'b0;
      pend_r       <= 1'b0;
    end else begin
      cap_open_r  <= arm_ok_w ? 1'b1 : close_w ? 1'b0 : cap_open_r;
      cap_hold_r  <= arm_ok_w ? 1'b1
                   : (close_w | cert_w | hold_exp_w) ? 1'b0 : cap_hold_r;
      cap_valid_r <= arm_ok_w ? 1'b1
                   : (close_w | void_grant_w) ? 1'b0 : cap_valid_r;
      cap_cert_r  <= arm_ok_w ? 1'b0
                   : close_w ? 1'b0 : cert_ok_w ? 1'b1 : cap_cert_r;
      if (arm_ok_w) cap_id_r <= cap_id_r + 1'b1;
      if (arm_ok_w)
        hold_r <= HOLD_W_C'(T_HOLD_MS_P);
      else if (cap_hold_r && ms_tick_w && (hold_r != '0))
        hold_r <= hold_r - 1'b1;
      if (commit_ack_w) ack_ref_r <= ~ack_ok_w;
      else if (arm_ok_w) ack_ref_r <= 1'b0;
      if (arm_w) arm_ref_r <= ~arm_ok_w;
      dirty_live_r <= dirty_live_n_w;
      dirty_cap_r  <= dirty_cap_n_w;
      pend_r       <= pend_i;
    end
  end

  assign pend_w        = pend_r | unres_w;
  assign nvm_backed_o  = backed_r;
  assign nvm_dirty_o   = dirty_img_w;
  assign nvm_stale_o   = stale_r;
  assign nvm_verdict_o = verdict_r;
  assign img_valid_o   = img_valid_r;
  assign nvm_pend_o    = pend_w;
  assign nvm_unres_o   = unres_w;

  // =======================================================================
  //  The byte pump: device face <-> main memory
  // =======================================================================
  typedef enum logic [3:0] {
    S_IDLE,     // wait for a command
    S_RDBLANK,  // READ with no live image: stream 0xFF, no memory traffic
    S_RDFETCH,  // READ: request the word that holds the byte
    S_RDWAIT,   // READ: wait for the beat
    S_RDHOLD,   // READ: present the byte until the initiator takes it
    S_WTAKE,    // WRITE: wait for the initiator's byte
    S_WREQ,     // WRITE: present the single-beat write until accepted
    S_WDONE,    // WRITE: wait for the commit pulse
    S_WDISCARD, // WRITE with no configured image: accept and discard
    S_EREQ,     // ERASE: present one 0xFF byte write
    S_EDONE,    // ERASE: wait for its commit pulse
    S_FIN,      // pulse done
    S_ERR       // pulse err
  } state_e;

  state_e      st_r;
  logic [31:0] addr_r;
  logic [15:0] cnt_r;
  logic [7:0]  byte_r;
  logic        gnt_r, done_r, err_r, was_write_r;
  logic [15:0] eff_len_w;
  logic [31:0] span_end_w;
  logic        span_ok_w;
  //! the word cache: one fetched 64-bit beat and the address it came from
  logic        wc_valid_r;
  logic [28:0] wc_addr_r;
  logic [63:0] wc_data_r;
  logic        wc_hit_w;

  //! ERASE with len 0 means the whole record
  assign eff_len_w = (dev_op_i == OP_ERASE_C && dev_len_i == 16'd0)
                   ? 16'(rec_len_w) : dev_len_i;
  //! the span must fit the record AND the configured image
  assign span_end_w = 32'(rec_base_w) + 32'(dev_offset_i) + 32'(eff_len_w);
  assign span_ok_w  = rec_hit_w
                    && ({16'd0, dev_offset_i} + {16'd0, eff_len_w} <= 32'(rec_len_w))
                    && (span_end_w <= img_len_r);
  assign wc_hit_w   = wc_valid_r && (wc_addr_r == addr_r[31:3]);

  //! PROTOTYPE: a WRITE or ERASE request is DEFERRED (no grant, the port
  //! holds its request) while a capture holds the image; a READ never is.
  //! The hold starts ON the arm edge: a request in the arm's own cycle is
  //! deferred like any later one, so no mutating operation starts inside a
  //! capture before its record reads open (revision b). The hold is bounded
  //! by T_HOLD_MS_P, after which the request is granted and the capture it
  //! overlaps can no longer be certified.
  logic mut_req_w, gnt_now_w;
  assign mut_req_w   = (dev_op_i == OP_WRITE_C) || (dev_op_i == OP_ERASE_C);
  assign gnt_now_w   = (st_r == S_IDLE) && dev_req_i
                     && !((cap_hold_r | arm_ok_w) && mut_req_w);
  //! the grant of an operation that WILL present memory writes to its record
  assign gnt_opmut_w = gnt_now_w && mut_req_w && img_cfg_w && span_ok_w
                     && (eff_len_w != 16'd0);
  //! a whole-record WRITE that completed without error closes its record
  assign rec_close_w = done_r & was_write_r & op_mut_r & op_full_r;

  //! revision c: a mutating request the device could serve NOW and only the
  //! capture is holding back. Registered, it refuses the next arm (arm_ok_w
  //! above), so the request cannot be handed from one hold to the next.
  assign mut_wait_w  = dev_req_i & mut_req_w & (st_r == S_IDLE) & ~gnt_now_w;

  always_ff @(posedge clk_i) begin
    if (!rst_n) mut_defer_r <= 1'b0;
    else        mut_defer_r <= mut_wait_w;
  end

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      st_r        <= S_IDLE;
      addr_r      <= 32'd0;
      cnt_r       <= 16'd0;
      byte_r      <= 8'd0;
      gnt_r       <= 1'b0;
      done_r      <= 1'b0;
      err_r       <= 1'b0;
      was_write_r <= 1'b0;
      wc_valid_r  <= 1'b0;
      wc_addr_r   <= 29'd0;
      wc_data_r   <= 64'd0;
      op_region_r <= 8'd0;
      op_mut_r    <= 1'b0;
      op_full_r   <= 1'b0;
      set_q_r     <= 1'b0;
    end else begin
      gnt_r  <= 1'b0;
      done_r <= 1'b0;
      err_r  <= 1'b0;
      set_q_r <= gnt_opmut_w;
      //! a moved image makes every cached word a word of another image
      if (reg_we_w && (csr_addr_i[4:0] == R_IMG_BASE_C)) wc_valid_r <= 1'b0;
      case (st_r)
        S_IDLE: begin
          if (gnt_now_w) begin
            gnt_r       <= 1'b1;
            op_region_r <= dev_region_i;
            op_mut_r    <= gnt_opmut_w;
            op_full_r   <= (dev_op_i == OP_WRITE_C) && (dev_offset_i == 16'd0)
                        && (eff_len_w == 16'(rec_len_w));
            addr_r      <= img_base_r + 32'(rec_base_w) + 32'(dev_offset_i);
            cnt_r       <= eff_len_w;
            was_write_r <= (dev_op_i == OP_WRITE_C);
            if (!img_cfg_w) begin
              //! no image yet: the blank-flash responder's exact behaviour
              if (dev_op_i == OP_READ_C && dev_len_i != 16'd0)       st_r <= S_RDBLANK;
              else if (dev_op_i == OP_WRITE_C && dev_len_i != 16'd0) st_r <= S_WDISCARD;
              else                                                    st_r <= S_FIN;
            end else if (!span_ok_w) begin
              //! the port never range-checks record_id; this module must
              st_r <= S_ERR;
            end else if (eff_len_w == 16'd0) begin
              st_r <= S_FIN;
            end else begin
              case (dev_op_i)
                OP_READ_C:  st_r <= img_live_w ? S_RDFETCH : S_RDBLANK;
                OP_WRITE_C: begin st_r <= S_WTAKE; wc_valid_r <= 1'b0; end
                default:    begin st_r <= S_EREQ;  wc_valid_r <= 1'b0; end
              endcase
            end
          end
        end
        S_RDBLANK: begin
          if (dev_rready_i) begin
            if (cnt_r <= 16'd1) st_r <= S_FIN;
            else                cnt_r <= cnt_r - 16'd1;
          end
        end
        S_RDFETCH: begin
          if (wc_hit_w) begin
            byte_r <= wc_data_r[63 - 8 * addr_r[2:0] -: 8];
            st_r   <= S_RDHOLD;
          end else if (mem_req_ready_i) begin
            st_r <= S_RDWAIT;
          end
        end
        S_RDWAIT: begin
          if (mem_rsp_valid_i) begin
            if (mem_rsp_err_i) begin
              wc_valid_r <= 1'b0;
              st_r       <= S_ERR;
            end else if (mem_rsp_last_i) begin
              //! the single beat of the burst: cache it and serve the byte
              wc_valid_r <= 1'b1;
              wc_addr_r  <= addr_r[31:3];
              wc_data_r  <= mem_rsp_data_i;
              byte_r     <= mem_rsp_data_i[63 - 8 * addr_r[2:0] -: 8];
              st_r       <= S_RDHOLD;
            end
          end
        end
        S_RDHOLD: begin
          if (dev_rready_i) begin
            addr_r <= addr_r + 32'd1;
            if (cnt_r <= 16'd1) st_r <= S_FIN;
            else begin
              cnt_r <= cnt_r - 16'd1;
              st_r  <= S_RDFETCH;
            end
          end
        end
        S_WTAKE: begin
          if (dev_wvalid_i) begin
            byte_r <= dev_wdata_i;
            st_r   <= S_WREQ;
          end
        end
        S_WREQ: begin
          if (mem_wr_ready_i) begin
            //! a posted bridge commits in the same cycle it accepts
            if (mem_wr_done_i) begin
              if (mem_wr_err_i) st_r <= S_ERR;
              else begin
                addr_r <= addr_r + 32'd1;
                if (cnt_r <= 16'd1) st_r <= S_FIN;
                else begin cnt_r <= cnt_r - 16'd1; st_r <= S_WTAKE; end
              end
            end else begin
              st_r <= S_WDONE;
            end
          end
        end
        S_WDONE: begin
          if (mem_wr_done_i) begin
            if (mem_wr_err_i) st_r <= S_ERR;
            else begin
              addr_r <= addr_r + 32'd1;
              if (cnt_r <= 16'd1) st_r <= S_FIN;
              else begin cnt_r <= cnt_r - 16'd1; st_r <= S_WTAKE; end
            end
          end
        end
        S_WDISCARD: begin
          if (dev_wvalid_i) begin
            if (cnt_r <= 16'd1) st_r <= S_FIN;
            else                cnt_r <= cnt_r - 16'd1;
          end
        end
        S_EREQ: begin
          if (mem_wr_ready_i) begin
            if (mem_wr_done_i) begin
              if (mem_wr_err_i) st_r <= S_ERR;
              else begin
                addr_r <= addr_r + 32'd1;
                if (cnt_r <= 16'd1) st_r <= S_FIN;
                else                cnt_r <= cnt_r - 16'd1;
              end
            end else begin
              st_r <= S_EDONE;
            end
          end
        end
        S_EDONE: begin
          if (mem_wr_done_i) begin
            if (mem_wr_err_i) st_r <= S_ERR;
            else begin
              addr_r <= addr_r + 32'd1;
              if (cnt_r <= 16'd1) st_r <= S_FIN;
              else begin cnt_r <= cnt_r - 16'd1; st_r <= S_EREQ; end
            end
          end
        end
        S_FIN: begin
          done_r <= 1'b1;
          st_r   <= S_IDLE;
        end
        default: begin        // S_ERR
          err_r <= 1'b1;
          st_r  <= S_IDLE;
        end
      endcase
    end
  end

  //! the memory face, driven from the state alone
  assign mem_req_valid_o = (st_r == S_RDFETCH) && !wc_hit_w;
  assign mem_req_addr_o  = {addr_r[31:3], 3'b000};
  assign mem_req_beats_o = 9'd1;
  assign mem_rsp_ready_o = (st_r == S_RDWAIT);
  assign mem_wr_valid_o  = (st_r == S_WREQ) || (st_r == S_EREQ);
  assign mem_wr_addr_o   = {addr_r[31:3], 3'b000};
  assign mem_wr_data_o   = (st_r == S_EREQ) ? {64{1'b1}} : {8{byte_r}};
  assign mem_wr_strb_o   = 8'd1 << addr_r[2:0];

  //! the device face
  assign dev_busy_w   = (st_r != S_IDLE);
  assign dev_gnt_o    = gnt_r;
  assign dev_wready_o = (st_r == S_WTAKE) || (st_r == S_WDISCARD);
  assign dev_rvalid_o = (st_r == S_RDHOLD) || (st_r == S_RDBLANK);
  assign dev_rdata_o  = (st_r == S_RDBLANK) ? 8'hFF : byte_r;
  assign dev_busy_o   = dev_busy_w;
  assign dev_done_o   = done_r;
  assign dev_err_o    = err_r;

  // =======================================================================
  //  PROTOTYPE: record ownership (declared after the byte pump it observes)
  // =======================================================================
  //! the ownership vector, one bit per ALLOCATED record id (the section 4.2
  //! blocks at this shape); an unallocated id is a constant 0
  function automatic logic alloc_f(input int unsigned id);
    return (id == ID_CFG_C) || (id == ID_SUID_C)
        || (id >= ID_RATE_C && id < ID_RATE_C + N_AUDIO_UNIT_P)
        || (id >= ID_CLKS_C && id < ID_CLKS_C + N_CLK_DOM_P)
        || (id >= ID_MCR_C  && id < ID_MCR_C  + N_CLK_DOM_P)
        || (id >= ID_BIND_C && id < ID_BIND_C + N_STREAM_IN_P)
        || (id >= ID_FMTI_C && id < ID_FMTI_C + N_STREAM_IN_P)
        || (id >= ID_FMTO_C && id < ID_FMTO_C + N_STREAM_OUT_P)
        || (id >= ID_PTOF_C && id < ID_PTOF_C + N_STREAM_OUT_P)
        || (id >= ID_MAPI_C && id < ID_MAPI_C + N_SPORT_IN_P)
        || (id >= ID_MAPO_C && id < ID_MAPO_C + N_SPORT_OUT_P)
        || (id >= ID_NAME_C && id < ID_NAME_C + N_NAME_P);
  endfunction

  //! an operation is still in flight and will keep writing its own record
  assign inflight_w = (st_r != S_IDLE) & op_mut_r;

  // -----------------------------------------------------------------------
  //  PROTOTYPE (revision b): the load check, the capture's valid flag in
  //  reverse. The firmware re-bases, loads the window from a verified slot
  //  and strobes RELOAD; nothing but the load may have written the window in
  //  between, and the backend, not the firmware, decides whether that held.
  // -----------------------------------------------------------------------
  //! accepted only while the load flag is set AND the boot load is still
  //! pending: once per reset, so a RELOAD can never replace a window the
  //! producer has been writing since
  assign reload_ok_w = reload_w & ld_ok_r & ld_pend_r;

  //! REVISION C: THE WINDOW HAS GONE LIVE. A device-face operation that the
  //! load sequence did not bracket was granted on a configured image: the
  //! restore walk's reads, or a producer face that has been enabled. From
  //! that grant the boot load is OVER, accepted or not, so no later RELOAD
  //! is ever accepted -- whatever outcome a restarted writer finds, it can
  //! no longer close records or clear a dirty half over a live window. A
  //! load the writer REPEATS is not this: inside one bracket the flag is
  //! still set when the first grant after the re-base arrives.
  assign win_live_w = gnt_now_w & img_cfg_w & ~ld_ok_r;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      ld_ok_r   <= 1'b0;
      ld_pend_r <= 1'b1;
      ld_acc_r  <= 1'b0;
      rl_ref_r  <= 1'b0;
    end else begin
      //! PRIORITY: a mutating grant clears the flag, even on a re-base
      //! edge; a re-base arms it only with no mutating operation in flight,
      //! because such an operation keeps writing its record after the load
      ld_ok_r <= gnt_opmut_w ? 1'b0
               : reconf_w    ? ~inflight_w
                             : ld_ok_r;
      if (reload_ok_w | win_live_w) ld_pend_r <= 1'b0;
      //! revision d: set by an accepted RELOAD, cleared only by reset
      if (reload_ok_w) ld_acc_r <= 1'b1;
      if (reload_w)    rl_ref_r  <= ~reload_ok_w;
    end
  end

  for (genvar gi = 0; gi < 256; gi++) begin : g_own
    if (alloc_f(gi)) begin : g_alloc
      logic hit_w, open_n_w;
      assign hit_w = (op_region_r == 8'(gi));
      //! PRIORITY, highest first: a re-based image makes every record
      //! unknown; a grant opens its record, one cycle after the grant (it
      //! wins a same-edge close or reload, because the operation is still to
      //! come); an ACCEPTED reload makes every record a completed one (it
      //! meets no operation in flight: see reload_ok_w); a whole-record
      //! completion closes its record. Nothing closes a record on idle.
      assign open_n_w = reconf_w
                          | (set_q_r & hit_w)
                          | (~reload_ok_w & open_r[gi] & ~(rec_close_w & hit_w));
      always_ff @(posedge clk_i) begin
        if (!rst_n) open_r[gi] <= 1'b1;   // unknown until the writer reloads
        else        open_r[gi] <= open_n_w;
      end
    end else begin : g_none
      assign open_r[gi]   = 1'b0;
    end
  end


endmodule

`default_nettype wire
