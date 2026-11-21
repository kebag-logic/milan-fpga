/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_aaf_rx_depacketizer.sv
  Author      : Kebag Logic

  Date        : 2026-07-17
  Description : AAF RX payload extractor for the bound listener sink — the
                media half of the Milan Listener fabric path.

                Taps the RX AXI-Stream (never backpressures the datapath),
                buffers every frame through a drop-capable frame FIFO, and
                emits ONLY the AAF sample payload (bytes O+24 .. O+24+
                data_len-1, wire byte order = S32BE interleaved PCM) as one
                AXIS frame per PDU toward the route, render-map and loopback
                consumers.

                The accept verdicts are NOT re-derived here: the paired
                monitor pulses pdu_enq_p when it queues a PDU (bound +
                stream_id match), in the frame's flight, and later
                pdu_done_p with the inputs whose current format the PDU
                matches, the ones it counts in FRAMES_RX. A frame without the
                enqueue pulse is dropped at its tlast. A committed frame is
                read out once for each accepting input, tuser that input,
                from its one stored copy, and not at all when none accepted
                it, so each input receives exactly the PDUs its FRAMES_RX
                counts (#948: one stream may be bound to several inputs, IEEE
                1722.1-2021 8.2).

                Payload realignment: payload starts at frame byte 38
                (untagged, rotate 2) or 42 (C-VLAN, rotate 6); the read side
                re-parses the buffered header (VLAN flag from bytes 12..13,
                data_len from O+20..21) and rotates through a hold register.
                Output beats are always FULL 8-byte words: Milan base-format payloads are
                8-byte multiples (48k: 192 B, 96k: 384 B, 192k: 768 B); a
                non-multiple data_len is zero-padded in the final beat and
                the output advances by the padded length.

                Presentation time (#632): the same header re-parse reads the
                tv bit and avtp_timestamp (IEEE 1722-2016 4.4.4.9, 7.5) and
                pulses hdr_p_o with them on the beat that completes the
                timestamp, before the frame's payload. The payload's first
                beat then waits until PAY_LEAD_CYC_P cycles after that pulse, so
                a consumer can place the PDU by its timestamp before its
                first sample arrives (KL_render_queue). PAY_LEAD_CYC_P = 0 adds
                no wait.

  Company     : Kebag Logic
  Project     : Milan AVTP

  Notes       :
    - The write side drops a frame at its tlast unless the monitor's enqueue
      pulse arrived in its flight; the verdicts may come later, so the read
      side waits for them before it reads the frame.
    - Store overflow (downstream consumer stalled) drops WHOLE frames and counts
      them in drops_o — the tap itself never stalls the RX datapath.
------------------------------------------------------------------------------
*/

//! AAF RX payload extractor (listener media path): taps the RX AXI-Stream
//! without ever backpressuring it, buffers frames through a drop-capable
//! frame FIFO, and emits only the AAF sample payload (wire byte order =
//! S32BE interleaved PCM) as one AXIS frame per PDU toward the fabric
//! consumers. The monitor's enqueue pulse commits a frame and its done pulse
//! names the inputs that accepted it (current-format match); the frame is
//! read out once for each, tuser that input, so each receives exactly the
//! PDUs its FRAMES_RX counts (#948). Payload realignment
//! strips 38 (untagged) or 42 (C-VLAN) header bytes via a hold-register
//! rotation; output beats are always full 8-byte words (Milan base-format
//! payloads are 8-byte multiples), zero-padded on a non-multiple tail.

`default_nettype none

module KL_aaf_rx_depacketizer #(
  parameter int N_STREAMS_P      = 1,     //! listener inputs (verdict mask width)
  parameter int FIFO_DEPTH_BYTES = 2048,  //! frame FIFO depth (BRAM)
  parameter int PAY_LEAD_CYC_P   = 0      //! cycles from hdr_p_o to the
                                          //! frame's first payload beat,
                                          //! at least (0: no wait)
)(
  input  wire         clk_i,              //! Global clock
  input  wire         rst_n,              //! Active-low synchronous reset

  //! --- monitored RX AXI-Stream (observed, never driven) ------------------
  input  wire [63:0]  s_tdata_i,
  input  wire [7:0]   s_tkeep_i,
  input  wire         s_tvalid_i,
  input  wire         s_tready_i,
  input  wire         s_tlast_i,

  //! --- verdicts from the monitor ------------------------------------------
  input  wire         pdu_enq_p_i,        //! pulse: the in-flight frame's PDU
                                          //! was queued (bound + sid match)
  input  wire         pdu_done_p_i,       //! pulse: the oldest queued PDU's
                                          //! verdicts are complete
  input  wire [N_STREAMS_P-1:0] pdu_done_mask_i, //! with done: its accepting
                                          //! inputs (format match, started)

  //! --- PCM payload out (full 8-byte beats, wire byte order = S32BE) ------
  output logic [63:0] m_axis_tdata,
  output logic [7:0]  m_axis_tkeep,
  output logic        m_axis_tvalid,
  output logic        m_axis_tlast,       //! one AXIS frame per AAF PDU
  // spec-fixed 4-bit stream index (upper bits structurally 0 below N=16)
  // verilator coverage_off
  output logic [3:0]  m_axis_tuser,       //! stream index s of this PDU's
                                          //! payload (NXN §1.2: {tuser=s}
                                          //! rides each buffered frame)
  // verilator coverage_on
  input  wire         m_axis_tready,

  //! --- the frame's presentation time (#632) -------------------------------
  output logic        hdr_p_o,            //! one cycle: the frame's tv and
                                          //! avtp_timestamp are on the next
                                          //! two outputs; its payload
                                          //! follows (m_axis_tuser valid)
  output logic [31:0] hdr_ts_o,           //! avtp_timestamp (with hdr_p_o)
  output logic        hdr_tv_o,           //! tv (with hdr_p_o)

  //! --- observability ------------------------------------------------------
  output logic [15:0] pdus_o,             //! payloads emitted to fabric render
  output logic [15:0] drops_o,            //! whole frames lost to FIFO overflow
  //! per-stream attribution pulses (LCTX w11 DEPKT_CNT, NXN §1.4)
  output logic        pdu_out_p_o,        //! pulse per emitted payload PDU
  // spec-fixed 4-bit stream index (upper bits structurally 0 below N=16)
  // verilator coverage_off
  output logic [3:0]  pdu_out_idx_o,      //! its stream index
  // verilator coverage_on
  output logic        drop_p_o,           //! pulse per accepted frame the full
                                          //! store dropped
  output logic [N_STREAMS_P-1:0] drop_mask_o //! its accepting inputs
);

  // ------------------------------------------------------------------ //
  // Write side: every tapped frame enters the frame store and is kept     //
  // only if the monitor queued its PDU (#948)                             //
  // ------------------------------------------------------------------ //
  wire in_acc = s_tvalid_i && s_tready_i;

  //! The monitor's enqueue pulse follows the parser's match, and the parser
  //! matches on a frame's eighth beat (its 56-byte header buffer). The pulse
  //! comes fewer than eight cycles after that beat, and the next frame
  //! cannot reach its own eighth beat sooner, so a pulse is the PDU of the
  //! frame that passed its eighth beat last: the in-flight frame if
  //! p7_r is still set, otherwise a frame that ended first, which is lost.
  logic [3:0] bc_r;                       //! the in-flight frame's beats, to 8
  logic       p7_r;                       //! it passed its eighth beat
  logic       good_r;                     //! its PDU was queued
  wire        enq_mine_w = pdu_enq_p_i && p7_r;
  wire        fw_good_w  = good_r || enq_mine_w;

  always_ff @(posedge clk_i) begin : write_verdict
    if (!rst_n) begin
      bc_r   <= '0;
      p7_r   <= 1'b0;
      good_r <= 1'b0;
    end
    else begin
      if (enq_mine_w) good_r <= 1'b1;
      if (in_acc) begin
        if (bc_r != 4'd8) bc_r <= bc_r + 4'd1;
        if (bc_r == 4'd7) p7_r <= !s_tlast_i;
        if (s_tlast_i) begin
          bc_r   <= '0;
          p7_r   <= 1'b0;
          good_r <= 1'b0;
        end
      end
    end
  end : write_verdict

  // ------------------------------------------------------------------ //
  // The frame store: a frame FIFO whose head frame can be read again     //
  // ------------------------------------------------------------------ //
  //! A committed frame is read once for each input that accepted it, from
  //! its one copy (#948): the head frame's space is freed when its last
  //! input's pass ends, and between passes the read pointer returns to the
  //! frame's start. A frame is dropped whole when the store fills, an
  //! uncommitted one at its tlast; the tap itself never stalls. Words are
  //! {tlast, tdata}: the read side uses no tkeep.
  localparam int FW_C = $clog2(FIFO_DEPTH_BYTES / 8);   //! word address bits
  localparam int FD_C = 1 << FW_C;
  logic [64:0]   fmem_r [FD_C];
  logic [FW_C:0] wp_r;                    //! the next word written
  logic [FW_C:0] wc_r;                    //! the committed frames' end
  logic [FW_C:0] fs_r;                    //! the head frame's start
  logic [FW_C:0] rp_r;                    //! the next word read
  logic [FW_C:0] pn_r;                    //! the head frame's words popped this pass
  logic          drop_r;                  //! the in-flight frame is being dropped
  wire           full_w = (wp_r == {~fs_r[FW_C], fs_r[FW_C-1:0]});
  wire           wdrop_w = full_w || drop_r;
  //! the in-flight frame's end: committed, dropped (store full) or discarded
  wire           tl_w    = in_acc && s_tlast_i;
  wire           ovf_w   = tl_w && wdrop_w;

  always_ff @(posedge clk_i) begin : store_write
    if (in_acc && !wdrop_w) fmem_r[wp_r[FW_C-1:0]] <= {s_tlast_i, s_tdata_i};
  end : store_write

  always_ff @(posedge clk_i) begin : store_write_ptr
    if (!rst_n) begin
      wp_r   <= '0;
      wc_r   <= '0;
      drop_r <= 1'b0;
    end
    else if (in_acc) begin
      if (wdrop_w) begin
        drop_r <= !s_tlast_i;
        if (s_tlast_i) wp_r <= wc_r;
      end
      else begin
        wp_r <= wp_r + 1'b1;
        if (s_tlast_i) begin
          if (fw_good_w) wc_r <= wp_r + 1'b1;
          else           wp_r <= wc_r;
        end
      end
    end
  end : store_write_ptr

  //! read pipeline: the RAM's read register, then the output register
  logic          ff_valid, ff_last, ff_ready;
  logic [63:0]   ff_data;
  logic [64:0]   qa_r, qb_r;
  logic          va_r, vb_r;
  logic          rewind_w, release_w;
  wire           adv_b_w = ff_ready || !vb_r;
  wire           adv_a_w = adv_b_w || !va_r;
  wire           fetch_w = adv_a_w && (rp_r != wc_r);
  assign ff_valid = vb_r;
  assign ff_data  = qb_r[63:0];
  assign ff_last  = qb_r[64];
  wire           pop_w  = ff_valid && ff_ready;

  always_ff @(posedge clk_i) begin : store_read_data
    if (adv_a_w) qa_r <= fmem_r[rp_r[FW_C-1:0]];
    if (adv_b_w) qb_r <= qa_r;
  end : store_read_data

  always_ff @(posedge clk_i) begin : store_read_ptr
    if (!rst_n) begin
      va_r <= 1'b0;
      vb_r <= 1'b0;
      rp_r <= '0;
      fs_r <= '0;
      pn_r <= '0;
    end
    else if (rewind_w) begin
      //! another input owes a pass: back to the frame's start
      va_r <= 1'b0;
      vb_r <= 1'b0;
      rp_r <= fs_r;
      pn_r <= '0;
    end
    else begin
      if (adv_b_w) vb_r <= va_r;
      if (adv_a_w) va_r <= fetch_w;
      if (fetch_w) rp_r <= rp_r + 1'b1;
      if (release_w) begin
        fs_r <= fs_r + pn_r + 1'b1;
        pn_r <= '0;
      end
      else if (pop_w) pn_r <= pn_r + 1'b1;
    end
  end : store_read_ptr

  // ------------------------------------------------------------------ //
  // Verdict queue: each queued PDU, its frame's fate and its accepts     //
  // ------------------------------------------------------------------ //
  //! One entry per enqueue pulse, in queue order, retired once both the
  //! frame's fate and the monitor's done pulse are known. At most three
  //! queued PDUs wait in the monitor (its ring) and one more entry can
  //! wait for its retirement cycle, so four entries hold every case.
  localparam int RQ_LOG2_C = 2;
  logic [RQ_LOG2_C:0]       rq_ap_r, rq_vp_r, rq_rp_r;   //! alloc, done, retire
  logic [(1 << RQ_LOG2_C)-1:0] rq_res_r;                 //! the frame's fate is known
  logic [(1 << RQ_LOG2_C)-1:0] rq_com_r;                 //! ...committed
  logic [(1 << RQ_LOG2_C)-1:0] rq_drp_r;                 //! ...dropped (store full)
  logic [N_STREAMS_P-1:0]   rq_msk_r [1 << RQ_LOG2_C];   //! the accepting inputs
  logic [RQ_LOG2_C:0]       ifl_e_r;                     //! the in-flight frame's entry
  wire [RQ_LOG2_C-1:0]      rq_a_w = rq_ap_r[RQ_LOG2_C-1:0];
  wire [RQ_LOG2_C-1:0]      rq_h_w = rq_rp_r[RQ_LOG2_C-1:0];
  //! the in-flight frame ends with its PDU queued: its entry learns its fate
  wire                      fate_w = tl_w && fw_good_w;
  wire [RQ_LOG2_C-1:0]      fate_e_w = enq_mine_w ? rq_a_w : ifl_e_r[RQ_LOG2_C-1:0];
  wire                      retire_w = (rq_rp_r != rq_vp_r) && rq_res_r[rq_h_w];

  //! the read side's queue: the accepting inputs of each committed frame, in
  //! commit order; depth 64 covers the store's committed frames (a frame
  //! with a queued PDU has at least eight beats, so the 2 KB store holds 32)
  localparam int IDXQ_LOG2_C = 6;
  logic [N_STREAMS_P-1:0]   idxq_r [(1 << IDXQ_LOG2_C)];
  logic [IDXQ_LOG2_C-1:0]   idxq_wp_r, idxq_rp_r;
  logic                     idxq_pop_w;

  always_ff @(posedge clk_i) begin : verdict_queue
    if (!rst_n) begin
      rq_ap_r   <= '0;
      rq_vp_r   <= '0;
      rq_rp_r   <= '0;
      rq_res_r  <= '0;
      rq_com_r  <= '0;
      rq_drp_r  <= '0;
      ifl_e_r   <= '0;
      idxq_wp_r <= '0;
      idxq_rp_r <= '0;
      drop_p_o  <= 1'b0;
      drop_mask_o <= '0;
    end
    else begin
      drop_p_o <= 1'b0;
      //! an enqueue pulse takes the next entry: the in-flight frame's, or a
      //! frame already ended, whose PDU is lost
      if (pdu_enq_p_i) begin
        rq_res_r[rq_a_w] <= !p7_r;
        rq_com_r[rq_a_w] <= 1'b0;
        rq_drp_r[rq_a_w] <= 1'b0;
        rq_ap_r          <= rq_ap_r + 1'b1;
        if (p7_r) ifl_e_r <= rq_ap_r;
      end
      if (fate_w) begin
        rq_res_r[fate_e_w] <= 1'b1;
        rq_com_r[fate_e_w] <= !wdrop_w;
        rq_drp_r[fate_e_w] <= wdrop_w;
      end
      if (pdu_done_p_i) begin
        rq_msk_r[rq_vp_r[RQ_LOG2_C-1:0]] <= pdu_done_mask_i;
        rq_vp_r <= rq_vp_r + 1'b1;
      end
      if (retire_w) begin
        rq_rp_r <= rq_rp_r + 1'b1;
        //! a committed frame's inputs go to the read side, none at all
        //! included: the read side then passes over the frame
        if (rq_com_r[rq_h_w]) begin
          idxq_r[idxq_wp_r] <= rq_msk_r[rq_h_w];
          idxq_wp_r         <= idxq_wp_r + 1'b1;
        end
        //! a frame lost to the full store: its accepting inputs' DEPKT drops
        if (rq_drp_r[rq_h_w] && (rq_msk_r[rq_h_w] != '0)) begin
          drop_p_o    <= 1'b1;
          drop_mask_o <= rq_msk_r[rq_h_w];
        end
      end
      if (idxq_pop_w) idxq_rp_r <= idxq_rp_r + 1'b1;
    end
  end : verdict_queue

  // ------------------------------------------------------------------ //
  // Read side: re-parse the buffered header, strip 38/42 bytes via a     //
  // hold-register rotation, emit exactly ceil(data_len/8) payload beats  //
  // ------------------------------------------------------------------ //
  typedef enum logic [1:0] {
    R_HDR_S,      //! beats 0..4/5: VLAN flag, data_len, prime the hold
    R_PAY_S,      //! rotate + emit payload beats
    R_FLUSH_S     //! swallow padding/tail beats to the frame's tlast
  } rstate_t;

  rstate_t rstate_r;

  logic [2:0]  rbeat_r;       //! header beat index (saturates at 7)
  logic        vlan_r;        //! frame carries a C-VLAN tag
  logic [15:0] remain_r;      //! payload bytes still to emit
  logic [63:0] hold_r;        //! carried tail bytes (2 untagged / 6 tagged;
                              //! 64-bit so the unrolled byte mux never
                              //! part-selects out of range — Vivado 8-524)

  //! rotation k: hold contributes bytes 0..k-1 of every output beat
  wire [2:0] k_w = vlan_r ? 3'd6 : 3'd2;

  //! byte accessor into the little-lane FIFO word
  function automatic [7:0] fbyte(input [63:0] w, input [2:0] j);
    fbyte = w[8*j +: 8];
  endfunction

  //! final beat needs no FIFO word when the tail fits inside the hold
  wire hold_only_w = (rstate_r == R_PAY_S) && (remain_r <= 16'(k_w));
  //! the payload waits out PAY_LEAD_CYC_P cycles from the timestamp's pulse
  logic lead_ok_w;
  wire emit_w      = (rstate_r == R_PAY_S) && lead_ok_w && (hold_only_w || ff_valid);
  wire last_beat_w = (remain_r <= 16'd8);

  //! assemble the output beat: hold bytes then FIFO lanes, zero-padded
  //! past the payload tail
  always_comb begin : out_assemble
    for (int j = 0; j < 8; j++) begin
      logic [7:0] b;
      if (3'(j) < k_w) b = hold_r[8*j +: 8];
      else             b = fbyte(ff_data, 3'(j) - k_w);
      m_axis_tdata[8*j +: 8] = (16'(j) < remain_r) ? b : 8'h00;
    end
  end : out_assemble

  assign m_axis_tvalid = emit_w;
  assign m_axis_tkeep  = 8'hFF;
  assign m_axis_tlast  = emit_w && last_beat_w;

  // ------------------------------------------------------------------ //
  // Passes (#948): the head frame is read once for each input that       //
  // accepted it, lowest first, tuser that input                          //
  // ------------------------------------------------------------------ //
  logic                   pass_r;     //! the head frame's inputs are known
  logic [N_STREAMS_P-1:0] rmask_r;    //! its inputs still owed, this pass's included
  logic [3:0]             rs_r;       //! this pass's input
  function automatic [3:0] lowest(input [N_STREAMS_P-1:0] v);
    lowest = '0;
    for (int k = N_STREAMS_P-1; k >= 0; k--) if (v[k]) lowest = 4'(k);
  endfunction
  wire [N_STREAMS_P-1:0]  sq_head_w = idxq_r[idxq_rp_r];
  wire                    sq_ne_w   = (idxq_wp_r != idxq_rp_r);
  //! a frame's first word, when its inputs are taken from the queue
  wire                    first_w   = (rstate_r == R_HDR_S) && (rbeat_r == '0) && !pass_r;
  wire [N_STREAMS_P-1:0]  rnext_w   = rmask_r & ~(N_STREAMS_P'(1) << rs_r);
  //! the frame's last word: another pass, or the frame's space is freed
  wire                    fend_w    = ff_valid && ff_ready && ff_last;
  assign rewind_w   = fend_w && (rnext_w != '0);
  assign release_w  = fend_w && (rnext_w == '0);
  assign idxq_pop_w = ff_valid && ff_ready && first_w;
  assign m_axis_tuser = rs_r;

  always_ff @(posedge clk_i) begin : pass_ctl
    if (!rst_n) begin
      pass_r  <= 1'b0;
      rmask_r <= '0;
      rs_r    <= '0;
    end
    else if (idxq_pop_w && !fend_w) begin
      pass_r  <= 1'b1;
      rmask_r <= sq_head_w;
      rs_r    <= lowest(sq_head_w);
    end
    else if (fend_w) begin
      pass_r  <= (rnext_w != '0);
      rmask_r <= rnext_w;
      rs_r    <= lowest(rnext_w);
    end
  end : pass_ctl

  //! pop the FIFO word once its lanes are consumed (header beats once the
  //! frame's inputs are known; payload beats when the emit is accepted;
  //! flush beats always)
  assign ff_ready = (rstate_r == R_HDR_S && (pass_r || sq_ne_w)) ||
                    (rstate_r == R_FLUSH_S) ||
                    (rstate_r == R_PAY_S && lead_ok_w && !hold_only_w && m_axis_tready);

  // ------------------------------------------------------------------ //
  // The presentation time (#632): tv and avtp_timestamp from the header //
  // the read side re-parses. Untagged, the AVTP header starts at frame   //
  // byte 14: tv is byte 15 bit 0 (beat 1), the timestamp bytes 26..29    //
  // (beat 3). Tagged it starts at 18: tv byte 19 (beat 2), the timestamp //
  // bytes 30..33 (beat 3 lanes 6..7, beat 4 lanes 0..1).                 //
  // ------------------------------------------------------------------ //
  logic        tv_r;                  //! the frame's tv bit
  logic [15:0] ts_hi_r;               //! a tagged frame's timestamp high half
  //! beat 1's own VLAN test (vlan_r lands on its edge)
  wire vlan_b1_w = (fbyte(ff_data, 3'd4) == 8'h81) && (fbyte(ff_data, 3'd5) == 8'h00);
  wire hdr_beat_w = (rstate_r == R_HDR_S) && pop_w &&
                    (((rbeat_r == 3'd3) && !vlan_r) || ((rbeat_r == 3'd4) && vlan_r));
  always_ff @(posedge clk_i) begin : hdr_fields
    if (!rst_n) begin
      tv_r    <= 1'b0;
      ts_hi_r <= '0;
    end else if ((rstate_r == R_HDR_S) && pop_w) begin
      if (rbeat_r == 3'd1) tv_r <= !vlan_b1_w && ff_data[56];
      if ((rbeat_r == 3'd2) && vlan_r) tv_r <= ff_data[24];
      if (rbeat_r == 3'd3) ts_hi_r <= {fbyte(ff_data, 3'd6), fbyte(ff_data, 3'd7)};
    end
  end : hdr_fields
  assign hdr_p_o  = hdr_beat_w;
  assign hdr_tv_o = tv_r;
  assign hdr_ts_o = vlan_r ? {ts_hi_r, fbyte(ff_data, 3'd0), fbyte(ff_data, 3'd1)}
                           : {fbyte(ff_data, 3'd2), fbyte(ff_data, 3'd3),
                              fbyte(ff_data, 3'd4), fbyte(ff_data, 3'd5)};

  generate if (PAY_LEAD_CYC_P > 0) begin : g_lead
    localparam int LW_C = $clog2(PAY_LEAD_CYC_P + 1);
    logic [LW_C-1:0] lead_r;          //! cycles still to wait
    always_ff @(posedge clk_i) begin : lead_count
      if (!rst_n)            lead_r <= '0;
      else if (hdr_beat_w)   lead_r <= LW_C'(PAY_LEAD_CYC_P - 1);
      else if (lead_r != '0) lead_r <= lead_r - 1'b1;
    end : lead_count
    //! the pulse's own cycle counts as the first of the lead: the header
    //! is still being read on it, so no payload beat can leave then, and
    //! the gate reads the count alone (no path back through the pop)
    assign lead_ok_w = (lead_r == '0);
  end else begin : g_no_lead
    assign lead_ok_w = 1'b1;
  end endgenerate

  always_ff @(posedge clk_i) begin : read_fsm
    if (!rst_n) begin
      rstate_r <= R_HDR_S;
      rbeat_r  <= '0;
      vlan_r   <= 1'b0;
      remain_r <= '0;
      hold_r   <= '0;
      pdus_o   <= '0;
      drops_o  <= '0;
      pdu_out_p_o   <= 1'b0;
      pdu_out_idx_o <= '0;
    end
    else begin
      pdu_out_p_o <= 1'b0;
      if (ovf_w) drops_o <= drops_o + 16'd1;

      case (rstate_r)
        R_HDR_S : begin
          if (pop_w) begin
            rbeat_r <= (rbeat_r == 3'd7) ? 3'd7 : rbeat_r + 3'd1;
            //! a frame no input accepted is passed over (#948)
            if (first_w && (sq_head_w == '0)) rstate_r <= R_FLUSH_S;
            if (rbeat_r == 3'd1)
              vlan_r <= (fbyte(ff_data, 3'd4) == 8'h81) &&
                        (fbyte(ff_data, 3'd5) == 8'h00);
            if (rbeat_r == 3'd4) begin
              if (!vlan_r) begin
                //! untagged: data_len at bytes 34..35, payload from byte 38
                remain_r <= {fbyte(ff_data, 3'd2), fbyte(ff_data, 3'd3)};
                hold_r   <= {48'h0, fbyte(ff_data, 3'd7),
                                    fbyte(ff_data, 3'd6)};
                rstate_r <= R_PAY_S;
              end
              else begin
                //! tagged: data_len at bytes 38..39, payload from byte 42
                remain_r <= {fbyte(ff_data, 3'd6), fbyte(ff_data, 3'd7)};
              end
            end
            if (rbeat_r == 3'd5 && vlan_r) begin
              hold_r   <= {16'h0,
                           fbyte(ff_data, 3'd7), fbyte(ff_data, 3'd6),
                           fbyte(ff_data, 3'd5), fbyte(ff_data, 3'd4),
                           fbyte(ff_data, 3'd3), fbyte(ff_data, 3'd2)};
              rstate_r <= R_PAY_S;
            end
            //! runt safety: a committed frame cannot end inside its header
            //! (commit needs the parse-complete pulse at frame byte 48),
            //! so this arm is defensive-only
            // verilator coverage_off
            if (ff_last) begin
              rstate_r <= R_HDR_S;
              rbeat_r  <= '0;
            end
            // verilator coverage_on
          end
        end

        R_PAY_S : begin
          if (emit_w && m_axis_tready) begin
            //! carry the beat's tail lanes: hold byte j = lane j + (8-k)
            if (!hold_only_w)
              hold_r <= vlan_r
                ? {16'h0,
                   fbyte(ff_data, 3'd7), fbyte(ff_data, 3'd6),
                   fbyte(ff_data, 3'd5), fbyte(ff_data, 3'd4),
                   fbyte(ff_data, 3'd3), fbyte(ff_data, 3'd2)}
                : {48'h0, fbyte(ff_data, 3'd7), fbyte(ff_data, 3'd6)};
            if (last_beat_w) begin
              pdus_o        <= pdus_o + 16'd1;
              pdu_out_p_o   <= 1'b1;
              pdu_out_idx_o <= rs_r;
              remain_r      <= '0;
              rbeat_r       <= '0;
              //! the beat that completed the payload may also close the
              //! frame; otherwise swallow padding/FCS-strip tail beats
              if (hold_only_w || !pop_w || !ff_last) begin
                if (hold_only_w || !ff_last) rstate_r <= R_FLUSH_S;
                // verilator coverage_off
                else                         rstate_r <= R_HDR_S;
                // verilator coverage_on
              end
              else rstate_r <= R_HDR_S;
            end
            else begin
              remain_r <= remain_r - 16'd8;
            end
          end
          //! truncated frame (never for committed AAF PDUs): resync
          if (pop_w && ff_last && !(emit_w && m_axis_tready && last_beat_w)) begin
            rstate_r <= R_HDR_S;
            rbeat_r  <= '0;
            remain_r <= '0;
          end
        end

        R_FLUSH_S : begin
          if (pop_w && ff_last) begin
            rstate_r <= R_HDR_S;
            rbeat_r  <= '0;
          end
        end

        // verilator coverage_off
        default : begin
          rstate_r <= R_HDR_S;
        end
        // verilator coverage_on
      endcase
    end
  end : read_fsm

endmodule

`default_nettype wire
