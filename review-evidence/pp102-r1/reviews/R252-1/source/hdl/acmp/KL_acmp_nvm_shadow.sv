/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_acmp_nvm_shadow.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/05 §5
//                NVM shadow ≈20 B/sink; 07 §5.2 F07.8 record framing,
//                07 §5.3 F07.9 commit/restore flows; 02 §8 F02.8 class-F
//                manager face; 08 §2 T-NVM-DEBOUNCE)
//
//  Description : The per-sink ACMP binding persistence shadow of 05 §5 —
//                the BINDING[i] record source/sink at the class-F seam (the
//                full multi-record NVM manager lands in P4; this block IS
//                the manager for the ACMP binding group). Three faces:
//                (a) CAPTURE — watches the listener executor's record
//                write port (KL_pp_acmp_listener dbg_recwr_*) and projects
//                each written F07.6 record onto the persisted field set
//                {valid=bound, started, streaming_wait, talker_eid,
//                talker_uid, bind_ctlr_eid}; (b) PRELOAD — after boot
//                restore, drives the listener's exact pre_* face
//                (07 §5.3: restored binding enters PRB_W_AVAIL); (c) NVM —
//                initiates on KL_pp_nvm_port's manager face, serializing
//                the F07.8 frame {magic 0x1722, layout_version, record_id
//                = REC_ID_BASE_P + sink, payload_length = 20, crc16
//                CCITT-FALSE over header-sans-crc + payload, 16-bit fields
//                big-endian} around the 20-byte BINDING payload
//                {flags[valid,started,sw], rsv, talker_uid, talker_eid,
//                ctlr_eid — big-endian}. Commits are debounced
//                (T-NVM-DEBOUNCE via tick_i, F07.9 coalescing) and retried
//                RETRY_MAX_P times before the sticky side-port alarm; the
//                shadow store is a RAM-shaped sync-read array, never a
//                flop mirror.
//
//                The one design decision that matters: the shadow is a
//                projection cache with restore-then-replay. Capture
//                compares each record write against the stored projection
//                and only a DIFFERING persisted field marks dirty — so
//                GET_RX_STATE write-backs and probe bookkeeping cost zero
//                NVM wear ("write-through on change") — and boot restore
//                is two-phase: every record is read and validated into the
//                store FIRST, pre_* replay starts only after the whole
//                walk, so a torn stream atomically rejects the image
//                (03 §6 rule (e) spirit: fail whole and loud, never a
//                partial preload).
//
//  Refusals    : (a) a read-back that ends with ZERO record bytes
//                forwarded (empty/unframed region, header refused by the
//                port) is the F07.9 per-record arm — vendor default =
//                no saved binding, the walk continues; a read-back torn
//                MID-STREAM (err or short done after ≥1 byte) aborts the
//                WHOLE restore: restore_fail_o, no preload is ever driven,
//                every un-captured sink stays invalid. (b) a complete
//                record failing crc/layout_version/record_id/length is
//                per-record vendor default (F07.9 crc arm), never an
//                abort. (c) a capture during restore WINS over the
//                restored image for its sink: the NVM value is discarded,
//                the preload is skipped, and the live change is written
//                back after the walk (change-during-restore ordering).
//                (d) a capture hitting a record MID-FLUSH taints the
//                in-flight image: dirty survives the commit and the burst
//                loop re-serializes fresh data (NVM converges to newest).
//                Captures during the post-reset init sweep are dropped
//                (both sweeps write zeros); flushes are gated behind
//                restore completion (07 §5.3 boot-before-enable order).
//
//  Blank arm   : restore_done_o is SEQUENCING, not a verdict. Every path in
//                (a) and (b) above ends the walk with done and no fail, so
//                done alone cannot separate a restore that put bindings back
//                from one that read blank or unframed media and applied
//                vendor defaults to every sink. Milan v1.2 5.3.8.2/5.3.8.3
//                make that difference reportable state (the bound state and
//                the binding parameters either came back or did not), so
//                restore_blank_o carries it: it is done AND no record was
//                ever validated off the media this walk. A record that is
//                framed, crc-clean and carries valid=0 (a saved UNBIND,
//                5.3.8.3's "cleared when the Stream Input gets unbound") is
//                NOT blank - the media answered. A torn walk is not blank
//                either by accident: the atomic reject discards every record
//                it had already taken, so the count it reports is zero.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_acmp_nvm_shadow
  import pp_acmp_pkg::*;
#(
    //! P-N-STREAM-IN (F01.5): one shadow row per sink
    parameter int unsigned N_SINKS_P     = 8,
    //! BINDING[i] record id base (07 §5.2 allocation — not doc-pinned)
    parameter logic [7:0]  REC_ID_BASE_P = 8'h20,
    //! F07.8 layout_version this shadow writes and accepts
    //! 0x02 (issue #78): the record's BYTES did not change, but the meaning
    //! of `started` did. Until #78 nothing ever set it, so every record any
    //! shipped firmware persisted carries started = 0 - and started = 0 now
    //! gates the media path. Accepting those records on upgrade would fast-
    //! connect a binding that reports bound, reserves bandwidth, answers
    //! GET_STREAM_INFO with STREAMING_WAIT set, and plays nothing until a
    //! controller happens to send START_STREAMING. Refusing them costs one
    //! re-bind and cannot be silent.
    parameter logic [7:0]  LAYOUT_VER_P  = 8'h02,
    //! T-NVM-DEBOUNCE in tick_i units (F08.1: ≈500 ms at a 1 ms tick)
    parameter int unsigned DEB_TICKS_P   = 500,
    //! bounded commit retries before the side-port alarm (F07.9)
    parameter int unsigned RETRY_MAX_P   = 2,
    //! derived — do not override
    localparam int unsigned SINK_W_C = (N_SINKS_P > 1) ? $clog2(N_SINKS_P) : 1
) (
    input  wire                        clk_i,          //! core clock (P-CLK-HZ)
    input  wire                        rst_n,          //! sync active-low reset

    //! ---- boot/debounce control ------------------------------------------
    input  wire                        tick_i,         //! debounce timebase tick
    input  wire                        restore_go_i,   //! start boot restore (07 §5.3)
    output logic                       restore_busy_o, //! restore walk/replay running
    output logic                       restore_done_o, //! level: restore sequencing complete
    output logic                       restore_fail_o, //! level: torn read-back aborted the WHOLE restore
    output logic                       restore_blank_o,//! level: the completed walk validated ZERO records (blank or invalid media)
    output logic                       alarm_o,        //! sticky: commit retries exhausted (side-port alarm)

    //! ---- (a) capture face (KL_pp_acmp_listener dbg_recwr_* shadow) ---------
    input  wire                        cap_wr_i,       //! record write this cycle
    input  wire  [SINK_W_C-1:0]        cap_sink_i,     //! written sink
    input  wire  [ACMP_REC_W_C-1:0]    cap_rec_i,      //! written F07.6 record image

    //! ---- (b) preload face out (KL_pp_acmp_listener pre_* exact) ------------
    output logic                       pre_valid_o,    //! preload request (boot restore)
    output logic [15:0]                pre_sink_o,     //! sink index
    output logic [63:0]                pre_talker_eid_o,//! restored talker EID
    output logic [15:0]                pre_talker_uid_o,//! restored talker unique_id
    output logic [63:0]                pre_ctlr_eid_o, //! restored controller EID
    output logic                       pre_sw_o,       //! restored STREAMING_WAIT
    output logic                       pre_started_o,  //! restored started flag
    input  wire                        pre_ready_i,    //! accept on valid AND ready

    //! ---- (c) class-F manager face (KL_pp_nvm_port initiator, F02.8) -----
    output logic                       nvm_req_o,      //! start an op (port idle only)
    output logic                       nvm_we_o,       //! 1 = commit, 0 = restore
    output logic [7:0]                 nvm_record_id_o,//! REC_ID_BASE_P + sink
    output logic                       nvm_wvalid_o,   //! commit byte present
    input  wire                        nvm_wready_i,   //! port accepts the commit byte
    output logic [7:0]                 nvm_wdata_o,    //! commit byte (framed, header first)
    input  wire                        nvm_rvalid_i,   //! restore byte present
    output logic                       nvm_rready_o,   //! accept the restore byte
    input  wire  [7:0]                 nvm_rdata_i,    //! restore byte (framed, header first)
    input  wire                        nvm_busy_i,     //! op in flight
    input  wire                        nvm_done_i,     //! one-cycle pulse: op complete
    input  wire                        nvm_err_i,      //! one-cycle pulse: op failed

    //! ---- observability (suite taps; never drive anything) ---------------
    output logic [N_SINKS_P-1:0]       dbg_dirty_o,    //! per-sink dirty (unflushed change)
    output logic [N_SINKS_P-1:0]       dbg_valid_o,    //! per-sink saved-binding valid
    output logic [N_SINKS_P-1:0]       dbg_touched_o   //! per-sink captured-during-restore
);

  // ---- F07.8 framing constants (07 §5.2) ---------------------------------
  localparam logic [7:0]  MAGIC_HI_C = 8'h17;
  localparam logic [7:0]  MAGIC_LO_C = 8'h22;
  localparam int unsigned PL_BYTES_C = 20;             // 05 §5: ≈20 B/sink, exact here
  localparam logic [15:0] PLEN_C     = 16'(PL_BYTES_C);

  // ---- the persisted projection (05 §5 NVM shadow field set) -------------
  typedef struct packed {
    logic        started;      // Milan §5.3.8.7
    logic        sw;           // saved STREAMING_WAIT (restored via pre_sw)
    logic [15:0] talker_uid;   // Milan §5.3.8.2/.3
    logic [63:0] talker_eid;
    logic [63:0] ctlr_eid;
  } shw_t;

  localparam int unsigned SHW_W_C = $bits(shw_t);      // 146

  // ---- top FSM -----------------------------------------------------------
  typedef enum logic [3:0] {
    H_INIT,      // zero-sweep the shadow RAM after reset (captures dropped)
    H_WAIT,      // wait restore_go_i (captures live)
    H_RS_REQ,    // restore: request record read for sink rs_k_r
    H_RS_STREAM, // restore: receive + validate the framed record
    H_RS_STORE,  // restore: write the validated projection (capture wins)
    H_RP_RD,     // replay: shadow read issue for sink rp_k_r
    H_RP_LATCH,  // replay: read data -> preload latch
    H_RP_DRIVE,  // replay: hold pre_* until accept (or withdraw on touch)
    H_FIN,       // restore sequencing complete -> done level
    H_RUN,       // steady state: debounced write-through
    H_FL_RD,     // flush: shadow read issue for sink fl_sink_r
    H_FL_LATCH,  // flush: read data -> serializer latch
    H_FL_CRC,    // flush: 26-byte crc16 accumulate (header-sans-crc + payload)
    H_FL_REQ,    // flush: request the commit op (port idle)
    H_FL_STREAM, // flush: pump the 28 framed bytes
    H_FL_WAIT    // flush: wait done (clear dirty) / err (retry then alarm)
  } hstate_e;

  hstate_e             hs_r;
  logic [SINK_W_C:0]   init_cnt_r;
  logic                go_pend_r;      // restore_go_i seen during H_INIT

  // ---- RAM: the shadow store (RAM-shaped, sync read, no reset) -----------
  logic [SHW_W_C-1:0]  shw_ram_r [0:N_SINKS_P-1];
  logic [SHW_W_C-1:0]  shw_rdata_r;

  logic                rd_en_w;
  logic [SINK_W_C-1:0] rd_addr_w;
  logic                wr_en_w;
  logic [SINK_W_C-1:0] wr_addr_w;
  logic [SHW_W_C-1:0]  wr_data_w;

  always_ff @(posedge clk_i) begin : shw_ram_wr
    if (wr_en_w) begin
      shw_ram_r[wr_addr_w] <= wr_data_w;
    end
  end

  always_ff @(posedge clk_i) begin : shw_ram_rd
    if (rd_en_w) begin
      shw_rdata_r <= shw_ram_r[rd_addr_w];
    end
  end

  // one-cycle write bypass: a write coincident with a read issue is not in
  // the sync-read data, so the capture compare forwards it
  logic                byp_v_r;
  logic [SINK_W_C-1:0] byp_sink_r;
  logic [SHW_W_C-1:0]  byp_data_r;

  always_ff @(posedge clk_i) begin : byp_ff
    if (!rst_n) begin
      byp_v_r    <= 1'b0;
      byp_sink_r <= '0;
      byp_data_r <= '0;
    end else begin
      byp_v_r    <= wr_en_w;
      byp_sink_r <= wr_addr_w;
      byp_data_r <= wr_data_w;
    end
  end

  // ---- per-sink flag files -----------------------------------------------
  logic [N_SINKS_P-1:0] valid_r;    // saved-binding valid (projection 'valid')
  logic [N_SINKS_P-1:0] dirty_r;    // unflushed change
  logic [N_SINKS_P-1:0] touched_r;  // captured during the restore span

  // ---- (a) capture pipeline ----------------------------------------------
  acmp_rec_t cap_rec_w;
  shw_t      cap_proj_w;
  logic      cap_vld_w;
  logic      cap_active_w;

  assign cap_rec_w    = acmp_rec_t'(cap_rec_i);
  assign cap_vld_w    = cap_rec_w.f_bound;
  assign cap_active_w = cap_wr_i && (hs_r != H_INIT);

  always_comb begin : cap_proj
    cap_proj_w.started    = cap_rec_w.f_started;
    cap_proj_w.sw         = cap_rec_w.f_sw;
    cap_proj_w.talker_uid = cap_rec_w.talker_uid;
    cap_proj_w.talker_eid = cap_rec_w.talker_eid;
    cap_proj_w.ctlr_eid   = cap_rec_w.bind_ctlr_eid;
  end

  logic                c1_v_r;
  logic [SINK_W_C-1:0] c1_sink_r;
  shw_t                c1_proj_r;
  logic                c1_vld_r;

  always_ff @(posedge clk_i) begin : cap_stage
    if (!rst_n) begin
      c1_v_r    <= 1'b0;
      c1_sink_r <= '0;
      c1_proj_r <= '0;
      c1_vld_r  <= 1'b0;
    end else begin
      c1_v_r    <= cap_active_w;
      c1_sink_r <= cap_sink_i;
      c1_proj_r <= cap_proj_w;
      c1_vld_r  <= cap_vld_w;
    end
  end

  logic [SHW_W_C-1:0] cmp_data_w;
  logic               c1_diff_w;
  logic               c1_wr_w;

  assign cmp_data_w = (byp_v_r && (byp_sink_r == c1_sink_r)) ? byp_data_r
                                                             : shw_rdata_r;
  assign c1_diff_w  = (SHW_W_C'(c1_proj_r) != cmp_data_w)
                    || (c1_vld_r != valid_r[c1_sink_r]);
  assign c1_wr_w    = c1_v_r && c1_diff_w;

  // ---- restore span / sequencing helpers ---------------------------------
  logic go_take_w;
  logic rest_span_w;

  assign go_take_w   = (hs_r == H_WAIT) && (restore_go_i || go_pend_r);
  assign rest_span_w = go_take_w
                     || (hs_r == H_RS_REQ) || (hs_r == H_RS_STREAM)
                     || (hs_r == H_RS_STORE) || (hs_r == H_RP_RD)
                     || (hs_r == H_RP_LATCH) || (hs_r == H_RP_DRIVE);

  // ---- restore walk state -------------------------------------------------
  logic [SINK_W_C-1:0] rs_k_r;
  logic [16:0]         rbcnt_r;       // received record bytes this op
  logic [7:0]          rver_r, rrid_r;
  logic [15:0]         rplen_r;
  logic [15:0]         rcrc_rx_r;     // stored crc16 (header bytes 6..7)
  logic [15:0]         rcrc_acc_r;    // running crc16 (header-sans-crc + payload)
  logic                rvld_q_r, rstarted_q_r, rsw_q_r;
  logic [15:0]         ruid_q_r;
  logic [63:0]         rtk_q_r, rctlr_q_r;

  logic [16:0]         rexp_total_w;
  logic                rrec_ok_w;

  assign rexp_total_w = 17'd8 + 17'(rplen_r);
  assign rrec_ok_w    = (rver_r == LAYOUT_VER_P)
                      && (rrid_r == nvm_record_id_o)
                      && (rplen_r == PLEN_C)
                      && (rcrc_acc_r == rcrc_rx_r);

  // ---- replay state -------------------------------------------------------
  logic [SINK_W_C-1:0] rp_k_r;
  shw_t                rp_fields_r;

  // ---- flush state --------------------------------------------------------
  logic [SINK_W_C-1:0] fl_sink_r;
  shw_t                fl_fields_r;
  logic                fl_vld_r;
  logic [15:0]         fl_crc_r;
  logic [4:0]          fl_cidx_r;     // crc byte cursor 0..25
  logic [4:0]          fl_sidx_r;     // stream byte cursor 0..27
  logic [31:0]         fl_retry_r;
  logic                fl_taint_r;    // capture hit fl_sink mid-flush: the
                                      // serialized image is stale, keep dirty

  logic                fl_any_w;
  logic [SINK_W_C-1:0] fl_pick_w;

  always_comb begin : dirty_pick
    fl_any_w  = 1'b0;
    fl_pick_w = '0;
    for (int unsigned i = 0; i < N_SINKS_P; i++) begin
      if (!fl_any_w && dirty_r[i]) begin
        fl_any_w  = 1'b1;
        fl_pick_w = SINK_W_C'(i);
      end
    end
  end

  // ---- debounce (T-NVM-DEBOUNCE, F07.9 coalescing) ------------------------
  logic        deb_open_r;
  logic [31:0] deb_cnt_r;
  logic        fl_arm_r;

  always_ff @(posedge clk_i) begin : debounce_ff
    if (!rst_n) begin
      deb_open_r <= 1'b0;
      deb_cnt_r  <= 32'd0;
      fl_arm_r   <= 1'b0;
    end else begin
      if (c1_wr_w && !deb_open_r) begin
        deb_open_r <= 1'b1;
        deb_cnt_r  <= DEB_TICKS_P;
      end else if (deb_open_r && tick_i) begin
        if (deb_cnt_r <= 32'd1) begin
          deb_open_r <= 1'b0;
          fl_arm_r   <= 1'b1;          // window closed: release one burst
        end else begin
          deb_cnt_r <= deb_cnt_r - 32'd1;
        end
      end
      if ((hs_r == H_RUN) && fl_arm_r && !fl_any_w) begin
        fl_arm_r <= 1'b0;              // burst drained
      end
    end
  end

  // ---- crc16 CCITT-FALSE byte step (07 §5.2 in-band integrity) -----------
  function automatic logic [15:0] crc16_f(input logic [15:0] c,
                                          input logic [7:0]  d);
    logic [15:0] x;
    x = c ^ {d, 8'h00};
    for (int unsigned i = 0; i < 8; i++) begin
      x = x[15] ? ((x << 1) ^ 16'h1021) : (x << 1);
    end
    return x;
  endfunction

  // ---- framed-record byte generator (packed args only — sv2v rule) -------
  function automatic logic [7:0] fr_byte_f(input logic [SHW_W_C-1:0] fields,
                                           input logic               vld,
                                           input logic [7:0]         rid,
                                           input logic [15:0]        crc,
                                           input logic [4:0]         idx);
    shw_t       f;
    logic [7:0] b;
    f = shw_t'(fields);
    unique case (idx)
      5'd0:    b = MAGIC_HI_C;
      5'd1:    b = MAGIC_LO_C;
      5'd2:    b = LAYOUT_VER_P;
      5'd3:    b = rid;
      5'd4:    b = PLEN_C[15:8];
      5'd5:    b = PLEN_C[7:0];
      5'd6:    b = crc[15:8];
      5'd7:    b = crc[7:0];
      5'd8:    b = {5'd0, f.sw, f.started, vld};
      5'd9:    b = 8'd0;                               // reserved
      5'd10:   b = f.talker_uid[15:8];
      5'd11:   b = f.talker_uid[7:0];
      default: begin
        if (idx < 5'd20) b = f.talker_eid[8*(32'd19 - 32'(idx)) +: 8];
        else             b = f.ctlr_eid[8*(32'd27 - 32'(idx)) +: 8];
      end
    endcase
    return b;
  endfunction

  // crc pass skips the crc field itself: cursor 0..25 -> byte 0..5, 8..27
  logic [4:0] fl_cbyte_w;
  assign fl_cbyte_w = (fl_cidx_r < 5'd6) ? fl_cidx_r : (fl_cidx_r + 5'd2);

  // ---- RAM port arbitration (capture always wins) ------------------------
  logic fsm_rd_req_w;
  logic [SINK_W_C-1:0] fsm_rd_addr_w;
  logic fsm_rd_gnt_w;

  assign fsm_rd_req_w = (hs_r == H_RP_RD) || (hs_r == H_FL_RD);
  assign fsm_rd_addr_w = (hs_r == H_RP_RD) ? rp_k_r : fl_sink_r;
  assign fsm_rd_gnt_w = fsm_rd_req_w && !cap_active_w;

  assign rd_en_w   = cap_active_w || fsm_rd_req_w;
  assign rd_addr_w = cap_active_w ? cap_sink_i : fsm_rd_addr_w;

  logic fsm_wr_req_w;
  logic [SINK_W_C-1:0] fsm_wr_addr_w;
  logic [SHW_W_C-1:0]  fsm_wr_data_w;
  logic fsm_wr_gnt_w;

  shw_t rs_store_w;
  always_comb begin : rs_store
    rs_store_w.started    = rstarted_q_r;
    rs_store_w.sw         = rsw_q_r;
    rs_store_w.talker_uid = ruid_q_r;
    rs_store_w.talker_eid = rtk_q_r;
    rs_store_w.ctlr_eid   = rctlr_q_r;
  end

  assign fsm_wr_req_w  = ((hs_r == H_INIT) && (init_cnt_r < (SINK_W_C+1)'(N_SINKS_P)))
                       || ((hs_r == H_RS_STORE) && !touched_r[rs_k_r]);
  assign fsm_wr_addr_w = (hs_r == H_INIT) ? init_cnt_r[SINK_W_C-1:0] : rs_k_r;
  assign fsm_wr_data_w = (hs_r == H_INIT) ? '0 : SHW_W_C'(rs_store_w);
  assign fsm_wr_gnt_w  = fsm_wr_req_w && !c1_wr_w;

  assign wr_en_w   = c1_wr_w || fsm_wr_req_w;
  assign wr_addr_w = c1_wr_w ? c1_sink_r : fsm_wr_addr_w;
  assign wr_data_w = c1_wr_w ? SHW_W_C'(c1_proj_r) : fsm_wr_data_w;

  // ---- restore stream terminal events ------------------------------------
  logic rs_torn_w;      // ended mid-record: abort the WHOLE restore
  logic rs_empty_w;     // ended with zero bytes: per-record vendor default
  logic rs_complete_w;  // full frame delivered

  assign rs_torn_w = (hs_r == H_RS_STREAM)
                   && ((nvm_err_i && (rbcnt_r != 17'd0))
                       || (nvm_done_i && (rbcnt_r != 17'd0)
                           && ((rbcnt_r < 17'd8) || (rbcnt_r != rexp_total_w))));
  assign rs_empty_w = (hs_r == H_RS_STREAM)
                    && ((nvm_err_i && (rbcnt_r == 17'd0))
                        || (nvm_done_i && (rbcnt_r == 17'd0)));
  assign rs_complete_w = (hs_r == H_RS_STREAM) && nvm_done_i
                       && (rbcnt_r >= 17'd8) && (rbcnt_r == rexp_total_w);

  // ---- flush terminal events ----------------------------------------------
  // err can land mid-stream (device abort) or in the wait state; both are
  // the same bounded-retry path
  logic fl_done_w, fl_err_w, fl_giveup_w, fl_active_w;

  assign fl_done_w   = (hs_r == H_FL_WAIT) && nvm_done_i;
  assign fl_err_w    = ((hs_r == H_FL_WAIT) || (hs_r == H_FL_STREAM))
                     && nvm_err_i;
  assign fl_giveup_w = fl_err_w && (fl_retry_r >= RETRY_MAX_P);
  assign fl_active_w = (hs_r == H_FL_RD) || (hs_r == H_FL_LATCH)
                     || (hs_r == H_FL_CRC) || (hs_r == H_FL_REQ)
                     || (hs_r == H_FL_STREAM) || (hs_r == H_FL_WAIT);

  always_ff @(posedge clk_i) begin : fl_taint_ff
    if (!rst_n) begin
      fl_taint_r <= 1'b0;
    end else if ((hs_r == H_RUN) && fl_arm_r && fl_any_w) begin
      fl_taint_r <= 1'b0;                        // fresh pick, fresh image
    end else if (c1_wr_w && fl_active_w && (c1_sink_r == fl_sink_r)) begin
      fl_taint_r <= 1'b1;                        // the in-flight image is stale
    end
  end

  // ---- flag files ---------------------------------------------------------
  // Ordering inside the block is the priority: abort clears, restore
  // stores, flush clears — and a same-cycle capture wins them all.
  always_ff @(posedge clk_i) begin : flags_ff
    if (!rst_n) begin
      valid_r   <= '0;
      dirty_r   <= '0;
      touched_r <= '0;
    end else begin
      if (go_take_w) begin
        touched_r <= '0;
      end
      if (rs_torn_w) begin
        for (int unsigned i = 0; i < N_SINKS_P; i++) begin
          if (!touched_r[i]) valid_r[i] <= 1'b0;   // atomic reject
        end
      end
      if ((hs_r == H_RS_STORE) && fsm_wr_gnt_w) begin
        valid_r[rs_k_r] <= rvld_q_r;
      end
      if (rs_complete_w && !rrec_ok_w && !touched_r[rs_k_r]) begin
        valid_r[rs_k_r] <= 1'b0;                   // F07.9 per-record default
      end
      if (rs_empty_w && !touched_r[rs_k_r]) begin
        valid_r[rs_k_r] <= 1'b0;                   // no saved binding
      end
      if ((fl_done_w && !fl_taint_r) || fl_giveup_w) begin
        dirty_r[fl_sink_r] <= 1'b0;   // a tainted commit keeps dirty: the
      end                             // burst loop re-serializes fresh data
      if (c1_wr_w) begin                           // capture wins
        valid_r[c1_sink_r] <= c1_vld_r;
        dirty_r[c1_sink_r] <= 1'b1;
        if (rest_span_w) touched_r[c1_sink_r] <= 1'b1;
      end
    end
  end

  // ---- alarm --------------------------------------------------------------
  logic alarm_r;

  always_ff @(posedge clk_i) begin : alarm_ff
    if (!rst_n) begin
      alarm_r <= 1'b0;
    end else if (fl_giveup_w) begin
      alarm_r <= 1'b1;                             // sticky until reset
    end
  end

  // ---- restore result levels ----------------------------------------------
  logic done_r, fail_r;
  //! set by the ONE event that proves the media answered: a fully framed
  //! record that passed crc, layout_version, record_id and length. Cleared
  //! when a walk starts and again by the atomic reject, so it is never a
  //! leftover from the previous walk.
  logic any_rec_r;

  // ---- the engine ---------------------------------------------------------
  always_ff @(posedge clk_i) begin : engine
    if (!rst_n) begin
      hs_r         <= H_INIT;
      init_cnt_r   <= '0;
      go_pend_r    <= 1'b0;
      rs_k_r       <= '0;
      rbcnt_r      <= 17'd0;
      rver_r       <= 8'd0;
      rrid_r       <= 8'd0;
      rplen_r      <= 16'd0;
      rcrc_rx_r    <= 16'd0;
      rcrc_acc_r   <= 16'd0;
      rvld_q_r     <= 1'b0;
      rstarted_q_r <= 1'b0;
      rsw_q_r      <= 1'b0;
      ruid_q_r     <= 16'd0;
      rtk_q_r      <= 64'd0;
      rctlr_q_r    <= 64'd0;
      rp_k_r       <= '0;
      rp_fields_r  <= '0;
      fl_sink_r    <= '0;
      fl_fields_r  <= '0;
      fl_vld_r     <= 1'b0;
      fl_crc_r     <= 16'd0;
      fl_cidx_r    <= 5'd0;
      fl_sidx_r    <= 5'd0;
      fl_retry_r   <= 32'd0;
      done_r       <= 1'b0;
      fail_r       <= 1'b0;
      any_rec_r    <= 1'b0;
      nvm_req_o       <= 1'b0;
      nvm_we_o        <= 1'b0;
      nvm_record_id_o <= 8'd0;
    end else begin
      nvm_req_o <= 1'b0;                       // one-cycle strobe

      if (restore_go_i && (hs_r == H_INIT)) begin
        go_pend_r <= 1'b1;                     // don't lose an early go
      end

      unique case (hs_r)
        // ---------------------------------------------------------- H_INIT
        H_INIT: begin
          if (init_cnt_r < (SINK_W_C+1)'(N_SINKS_P)) begin
            init_cnt_r <= init_cnt_r + (SINK_W_C+1)'(1);
          end else begin
            hs_r <= H_WAIT;
          end
        end

        // ---------------------------------------------------------- H_WAIT
        H_WAIT: begin
          if (go_take_w) begin
            go_pend_r <= 1'b0;
            rs_k_r    <= '0;
            any_rec_r <= 1'b0;
            hs_r      <= H_RS_REQ;
          end
        end

        // -------------------------------------------------------- H_RS_REQ
        H_RS_REQ: begin
          if (!nvm_busy_i && !nvm_done_i && !nvm_err_i) begin
            nvm_req_o       <= 1'b1;
            nvm_we_o        <= 1'b0;
            nvm_record_id_o <= REC_ID_BASE_P + 8'(rs_k_r);
            rbcnt_r         <= 17'd0;
            rcrc_acc_r      <= 16'hFFFF;
            hs_r            <= H_RS_STREAM;
          end
        end

        // ----------------------------------------------------- H_RS_STREAM
        H_RS_STREAM: begin
          if (nvm_rvalid_i) begin              // rready held high here
            if ((rbcnt_r != 17'd6) && (rbcnt_r != 17'd7)) begin
              rcrc_acc_r <= crc16_f(rcrc_acc_r, nvm_rdata_i);
            end
            if      (rbcnt_r == 17'd2)  rver_r    <= nvm_rdata_i;
            else if (rbcnt_r == 17'd3)  rrid_r    <= nvm_rdata_i;
            else if (rbcnt_r == 17'd4)  rplen_r   <= {nvm_rdata_i, rplen_r[7:0]};
            else if (rbcnt_r == 17'd5)  rplen_r   <= {rplen_r[15:8], nvm_rdata_i};
            else if (rbcnt_r == 17'd6)  rcrc_rx_r <= {nvm_rdata_i, rcrc_rx_r[7:0]};
            else if (rbcnt_r == 17'd7)  rcrc_rx_r <= {rcrc_rx_r[15:8], nvm_rdata_i};
            else if (rbcnt_r == 17'd8) begin
              rvld_q_r     <= nvm_rdata_i[0];
              rstarted_q_r <= nvm_rdata_i[1];
              rsw_q_r      <= nvm_rdata_i[2];
            end
            else if ((rbcnt_r == 17'd10) || (rbcnt_r == 17'd11)) begin
              ruid_q_r <= {ruid_q_r[7:0], nvm_rdata_i};
            end
            else if ((rbcnt_r >= 17'd12) && (rbcnt_r < 17'd20)) begin
              rtk_q_r <= {rtk_q_r[55:0], nvm_rdata_i};
            end
            else if ((rbcnt_r >= 17'd20) && (rbcnt_r < 17'd28)) begin
              rctlr_q_r <= {rctlr_q_r[55:0], nvm_rdata_i};
            end
            rbcnt_r <= rbcnt_r + 17'd1;
          end
          if (rs_torn_w) begin
            fail_r    <= 1'b1;                 // atomic reject, no preload
            done_r    <= 1'b1;
            any_rec_r <= 1'b0;                 // nothing taken survives it
            hs_r      <= H_RUN;
          end else if (rs_empty_w || (rs_complete_w && !rrec_ok_w)) begin
            // per-record vendor default (valid cleared in flags_ff)
            if (rs_k_r == SINK_W_C'(N_SINKS_P - 1)) begin
              rp_k_r <= '0;
              hs_r   <= H_RP_RD;
            end else begin
              rs_k_r <= rs_k_r + SINK_W_C'(1);
              hs_r   <= H_RS_REQ;
            end
          end else if (rs_complete_w) begin
            any_rec_r <= 1'b1;                 // the media answered
            hs_r      <= H_RS_STORE;
          end
        end

        // ------------------------------------------------------ H_RS_STORE
        H_RS_STORE: begin
          if (fsm_wr_gnt_w || touched_r[rs_k_r]) begin
            if (rs_k_r == SINK_W_C'(N_SINKS_P - 1)) begin
              rp_k_r <= '0;
              hs_r   <= H_RP_RD;
            end else begin
              rs_k_r <= rs_k_r + SINK_W_C'(1);
              hs_r   <= H_RS_REQ;
            end
          end
        end

        // -------------------------------------------------------- H_RP_RD
        H_RP_RD: begin
          if (!valid_r[rp_k_r] || touched_r[rp_k_r]) begin
            if (rp_k_r == SINK_W_C'(N_SINKS_P - 1)) hs_r <= H_FIN;
            else                                    rp_k_r <= rp_k_r + SINK_W_C'(1);
          end else if (fsm_rd_gnt_w) begin
            hs_r <= H_RP_LATCH;
          end
        end

        // ----------------------------------------------------- H_RP_LATCH
        H_RP_LATCH: begin
          rp_fields_r <= shw_t'(shw_rdata_r);
          hs_r        <= H_RP_DRIVE;
        end

        // ----------------------------------------------------- H_RP_DRIVE
        H_RP_DRIVE: begin
          if (pre_ready_i || touched_r[rp_k_r]) begin
            // accepted — or withdrawn: a live capture outranks the image
            if (rp_k_r == SINK_W_C'(N_SINKS_P - 1)) hs_r <= H_FIN;
            else begin
              rp_k_r <= rp_k_r + SINK_W_C'(1);
              hs_r   <= H_RP_RD;
            end
          end
        end

        // ----------------------------------------------------------- H_FIN
        H_FIN: begin
          done_r <= 1'b1;
          hs_r   <= H_RUN;
        end

        // ----------------------------------------------------------- H_RUN
        H_RUN: begin
          if (fl_arm_r && fl_any_w) begin
            fl_sink_r  <= fl_pick_w;
            fl_retry_r <= 32'd0;
            hs_r       <= H_FL_RD;
          end
        end

        // --------------------------------------------------------- H_FL_RD
        H_FL_RD: begin
          if (fsm_rd_gnt_w) begin
            hs_r <= H_FL_LATCH;
          end
        end

        // ------------------------------------------------------ H_FL_LATCH
        H_FL_LATCH: begin
          fl_fields_r <= shw_t'(shw_rdata_r);
          fl_vld_r    <= valid_r[fl_sink_r];
          fl_crc_r    <= 16'hFFFF;
          fl_cidx_r   <= 5'd0;
          hs_r        <= H_FL_CRC;
        end

        // -------------------------------------------------------- H_FL_CRC
        H_FL_CRC: begin
          fl_crc_r <= crc16_f(fl_crc_r,
                              fr_byte_f(SHW_W_C'(fl_fields_r), fl_vld_r,
                                        REC_ID_BASE_P + 8'(fl_sink_r),
                                        16'h0000, fl_cbyte_w));
          if (fl_cidx_r == 5'd25) begin
            fl_sidx_r <= 5'd0;
            hs_r      <= H_FL_REQ;
          end else begin
            fl_cidx_r <= fl_cidx_r + 5'd1;
          end
        end

        // -------------------------------------------------------- H_FL_REQ
        H_FL_REQ: begin
          if (!nvm_busy_i && !nvm_done_i && !nvm_err_i) begin
            nvm_req_o       <= 1'b1;
            nvm_we_o        <= 1'b1;
            nvm_record_id_o <= REC_ID_BASE_P + 8'(fl_sink_r);
            hs_r            <= H_FL_STREAM;
          end
        end

        // ----------------------------------------------------- H_FL_STREAM
        H_FL_STREAM: begin
          if (nvm_err_i) begin
            if (fl_retry_r >= RETRY_MAX_P) begin
              hs_r <= H_RUN;                   // give up: alarm + dirty drop
            end else begin
              fl_retry_r <= fl_retry_r + 32'd1;
              hs_r       <= H_FL_RD;           // bounded retry, fresh read
            end
          end else if (nvm_wready_i) begin
            if (fl_sidx_r == 5'd27) begin
              hs_r <= H_FL_WAIT;
            end else begin
              fl_sidx_r <= fl_sidx_r + 5'd1;
            end
          end
        end

        // ------------------------------------------------------- H_FL_WAIT
        H_FL_WAIT: begin
          if (nvm_done_i) begin
            hs_r <= H_RUN;                     // dirty cleared in flags_ff
          end else if (nvm_err_i) begin
            if (fl_retry_r >= RETRY_MAX_P) begin
              hs_r <= H_RUN;                   // give up: alarm + dirty drop
            end else begin
              fl_retry_r <= fl_retry_r + 32'd1;
              hs_r       <= H_FL_RD;           // bounded retry, fresh read
            end
          end
        end

        default: hs_r <= H_RUN;
      endcase
    end
  end

  // ---- manager-face data paths --------------------------------------------
  assign nvm_wvalid_o = (hs_r == H_FL_STREAM);
  assign nvm_wdata_o  = fr_byte_f(SHW_W_C'(fl_fields_r), fl_vld_r,
                                  nvm_record_id_o, fl_crc_r, fl_sidx_r);
  assign nvm_rready_o = (hs_r == H_RS_STREAM);

  // ---- preload face --------------------------------------------------------
  assign pre_valid_o      = (hs_r == H_RP_DRIVE) && !touched_r[rp_k_r];
  assign pre_sink_o       = 16'(32'(rp_k_r));
  assign pre_talker_eid_o = rp_fields_r.talker_eid;
  assign pre_talker_uid_o = rp_fields_r.talker_uid;
  assign pre_ctlr_eid_o   = rp_fields_r.ctlr_eid;
  assign pre_sw_o         = rp_fields_r.sw;
  assign pre_started_o    = rp_fields_r.started;

  // ---- levels / observability ---------------------------------------------
  assign restore_busy_o = (hs_r == H_RS_REQ) || (hs_r == H_RS_STREAM)
                        || (hs_r == H_RS_STORE) || (hs_r == H_RP_RD)
                        || (hs_r == H_RP_LATCH) || (hs_r == H_RP_DRIVE)
                        || (hs_r == H_FIN);
  assign restore_done_o  = done_r;
  assign restore_fail_o  = fail_r;
  assign restore_blank_o = done_r && !any_rec_r;
  assign alarm_o        = alarm_r;
  assign dbg_dirty_o    = dirty_r;
  assign dbg_valid_o    = valid_r;
  assign dbg_touched_o  = touched_r;

endmodule

`default_nettype wire
