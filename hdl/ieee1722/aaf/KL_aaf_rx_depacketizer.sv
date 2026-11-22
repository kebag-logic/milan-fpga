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
                stream_id match), three cycles after the frame's eighth beat
                on the tap, and later pdu_done_p with the inputs whose
                current format the PDU matches, the ones it counts in
                FRAMES_RX. The store takes the tap three cycles late, so even
                a frame that ends on its eighth beat has its enqueue pulse in
                time; a frame without one is dropped at its tlast. A
                committed frame is read out once for each accepting input,
                tuser that input, from its one stored copy, and not at all
                when none accepted it, so each input receives exactly the
                PDUs its FRAMES_RX counts (#948: one stream may be bound to
                several inputs, IEEE 1722.1-2021 8.2).

                Payload realignment: payload starts at frame byte 38
                (untagged, rotate 2) or 42 (C-VLAN, rotate 6); the read side
                re-parses the buffered header (VLAN flag from bytes 12..13,
                data_len from O+20..21) and rotates through a hold register.
                Output beats are always FULL 8-byte words: each PDU's output
                frame is ceil(data_len/8) beats with tlast on the last, a
                non-multiple data_len zero-padded in that beat. When the
                payload's tail lies wholly in the hold register, the frame's
                last stored word is popped with that final beat, so the pass
                ends on the beat that carries tlast (#948). A frame that ends
                short of its data_len is dropped whole at its tlast and
                counted, never read out in part. (Milan base-format payloads
                are 8-byte multiples: 48k 192 B, 96k 384 B, 192k 768 B.)

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
    - The write side runs three cycles behind the tap, the enqueue pulse's
      latency after a frame's eighth beat, so every frame's queueing is known
      by its tlast there, however short the frame; a frame whose PDU was not
      queued is dropped at its tlast. The verdicts may come later, so the
      read side waits for them before it reads the frame.
    - Store overflow (downstream consumer stalled) drops WHOLE frames and counts
      them in drops_o — the tap itself never stalls the RX datapath. A queued
      PDU's frame short of its payload is dropped and counted the same way.
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
//! rotation; output beats are always full 8-byte words, ceil(data_len/8) of
//! them per PDU with tlast on the last, zero-padded on a non-multiple tail.

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
  input  wire         pdu_enq_p_i,        //! pulse: the PDU of the frame whose
                                          //! eighth beat the tap carried three
                                          //! cycles before was queued (bound +
                                          //! sid match)
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
  output logic [15:0] drops_o,            //! whole frames lost: FIFO overflow,
                                          //! or a queued PDU's frame short of
                                          //! its payload
  //! per-stream attribution pulses (LCTX w11 DEPKT_CNT, NXN §1.4)
  output logic        pdu_out_p_o,        //! pulse per emitted payload PDU
  // spec-fixed 4-bit stream index (upper bits structurally 0 below N=16)
  // verilator coverage_off
  output logic [3:0]  pdu_out_idx_o,      //! its stream index
  // verilator coverage_on
  output logic        drop_p_o,           //! pulse per accepted frame the full
                                          //! store dropped, or that ended
                                          //! short of its payload
  output logic [N_STREAMS_P-1:0] drop_mask_o //! its accepting inputs
);

  // ------------------------------------------------------------------ //
  // Write side: every tapped frame enters the frame store and is kept     //
  // only if the monitor queued its PDU (#948)                             //
  // ------------------------------------------------------------------ //
  //! The tap as it comes: the verdicts' attribution counts its beats.
  wire tap_acc_w = s_tvalid_i && s_tready_i;

  //! The monitor's enqueue pulse follows the parser's match, and the parser
  //! matches on a frame's eighth beat (its 56-byte header buffer). The
  //! parser's input register, its registered match and the monitor's
  //! registered pulse put the pulse ENQ_LAT_C = 3 cycles after the tap
  //! carries that beat, or nowhere (no bound entry holds the stream_id, or
  //! the monitor's ring is full). A frame may end on that very beat: eight
  //! beats are 57 to 64 octets, and one channel of 48 kHz Base AAF is 62
  //! (Milan v1.2 Table 6.1, IEEE 1722-2016 7.3). So the tap's own beat count
  //! names the pulse's frame, the one that passed its eighth beat last (the
  //! next cannot reach its own eighth beat sooner than eight cycles on), and
  //! the store's write side runs ENQ_LAT_C cycles behind the tap: each
  //! frame's verdict is known when its eighth beat reaches the write side,
  //! on or before its tlast, however short the frame (#948).
  localparam int ENQ_LAT_C = 3;
  logic [3:0] tbc_r;                      //! the tap frame's beats, to 8
  logic       taw_r;                      //! its PDU may still be queued
  logic       tq_r;                       //! its PDU was queued
  //! the tap's eighth beat, and a pulse for the frame that passed it
  wire        tp7_w     = tap_acc_w && (tbc_r == 4'd7);
  wire        enq_tap_w = pdu_enq_p_i && taw_r;

  always_ff @(posedge clk_i) begin : tap_attrib
    if (!rst_n) begin
      tbc_r <= '0;
      taw_r <= 1'b0;
      tq_r  <= 1'b0;
    end
    else begin
      if (enq_tap_w) begin
        taw_r <= 1'b0;
        tq_r  <= 1'b1;
      end
      if (tap_acc_w) begin
        if (tbc_r != 4'd8) tbc_r <= tbc_r + 4'd1;
        if (s_tlast_i)     tbc_r <= '0;
      end
      if (tp7_w) begin
        taw_r <= 1'b1;
        tq_r  <= 1'b0;
      end
    end
  end : tap_attrib

  //! the tap ENQ_LAT_C cycles late, as the store's write side takes it. The
  //! valid stages are reset; the data stages carry no reset ON PURPOSE (a
  //! shift register): each is read only with its valid.
  logic [ENQ_LAT_C-1:0] dv_r;
  logic [ENQ_LAT_C-1:0] dl_r;
  logic [63:0]          dd_r [ENQ_LAT_C];
  logic [7:0]           dk_r [ENQ_LAT_C];
  always_ff @(posedge clk_i) begin : tap_delay_valid
    if (!rst_n) dv_r <= '0;
    else        dv_r <= {dv_r[ENQ_LAT_C-2:0], tap_acc_w};
  end : tap_delay_valid
  always_ff @(posedge clk_i) begin : tap_delay_data
    dl_r    <= {dl_r[ENQ_LAT_C-2:0], s_tlast_i};
    dd_r[0] <= s_tdata_i;
    dk_r[0] <= s_tkeep_i;
    for (int i = 1; i < ENQ_LAT_C; i++) begin
      dd_r[i] <= dd_r[i-1];
      dk_r[i] <= dk_r[i-1];
    end
  end : tap_delay_data
  wire        in_acc    = dv_r[ENQ_LAT_C-1];
  wire [63:0] w_tdata_w = dd_r[ENQ_LAT_C-1];
  wire [7:0]  w_tkeep_w = dk_r[ENQ_LAT_C-1];
  wire        w_tlast_w = dl_r[ENQ_LAT_C-1];

  logic [3:0] bc_r;                       //! the stored frame's beats, to 8
  logic       good_r;                     //! its PDU was queued
  //! the stored frame's eighth beat, and its verdict: the pulse came by now,
  //! in this very cycle at the latency ENQ_LAT_C
  wire        m7_w      = in_acc && (bc_r == 4'd7);
  wire        q7_w      = tq_r || enq_tap_w;
  wire        fw_good_w = good_r || (m7_w && q7_w);

  //! A frame is kept only with its whole payload (#948): data_len octets
  //! after the 24-octet AAF header, which starts at frame byte 14, or 18
  //! behind a C-VLAN tag (IEEE 1722-2016 4.4.4.10). The VLAN flag is on
  //! beat 1 and data_len on beat 4, so from beat 4 on wowe_r holds the
  //! payload octets still to come; a frame whose last beat brings fewer is
  //! dropped whole at its tlast, as the full store drops one, and the read
  //! side only ever reads complete payloads. A frame with a queued PDU is
  //! at least eight beats long, so its tlast is never before beat 4.
  logic        wvlan_r;                   //! the in-flight frame is tagged
  logic [16:0] wowe_r;                    //! its payload octets after these beats
  wire  [3:0]  wkeep_n_w = 4'(w_tkeep_w[0]) + 4'(w_tkeep_w[1]) +
                           4'(w_tkeep_w[2]) + 4'(w_tkeep_w[3]) +
                           4'(w_tkeep_w[4]) + 4'(w_tkeep_w[5]) +
                           4'(w_tkeep_w[6]) + 4'(w_tkeep_w[7]);
  wire  [15:0] wlen_w    = wvlan_r ? {w_tdata_w[55:48], w_tdata_w[63:56]}
                                   : {w_tdata_w[23:16], w_tdata_w[31:24]};
  wire         wshort_w  = (wowe_r > 17'(wkeep_n_w));

  always_ff @(posedge clk_i) begin : write_verdict
    if (!rst_n) begin
      bc_r    <= '0;
      good_r  <= 1'b0;
      wvlan_r <= 1'b0;
      wowe_r  <= '0;
    end
    else begin
      if (m7_w) good_r <= q7_w;
      if (in_acc) begin
        if (bc_r != 4'd8) bc_r <= bc_r + 4'd1;
        if (bc_r == 4'd1)
          wvlan_r <= (w_tdata_w[39:32] == 8'h81) && (w_tdata_w[47:40] == 8'h00);
        //! beat 4 holds frame bytes 32..39: an untagged payload ends at
        //! 38 + data_len, a tagged one at 42 + data_len
        if (bc_r == 4'd4)
          wowe_r <= wvlan_r ? 17'(wlen_w) + 17'd2
                            : ((wlen_w > 16'd2) ? 17'(wlen_w) - 17'd2 : 17'd0);
        else if (bc_r > 4'd4)
          wowe_r <= (wowe_r > 17'd8) ? wowe_r - 17'd8 : 17'd0;
        if (w_tlast_w) begin
          bc_r    <= '0;
          good_r  <= 1'b0;
          wvlan_r <= 1'b0;
          wowe_r  <= '0;
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
  //! uncommitted one or one short of its payload at its tlast; the tap
  //! itself never stalls. Words are {tlast, tdata}: the read side uses no
  //! tkeep. The store, its read registers qa_r/qb_r and the two small queues
  //! (rq_msk_r, idxq_r) carry no reset ON PURPOSE (RAM): a word or entry is
  //! read only where a reset pointer or valid flag (wc_r, va_r/vb_r, rq_vp_r,
  //! idxq_wp_r) says it was written since the reset.
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
  wire           tl_w    = in_acc && w_tlast_w;
  //! a frame with a queued PDU that ends short of its payload (#948)
  wire           trunc_w = tl_w && fw_good_w && !wdrop_w && wshort_w;
  wire           ovf_w   = tl_w && (wdrop_w || trunc_w);

  always_ff @(posedge clk_i) begin : store_write
    if (in_acc && !wdrop_w) fmem_r[wp_r[FW_C-1:0]] <= {w_tlast_w, w_tdata_w};
  end : store_write

  always_ff @(posedge clk_i) begin : store_write_ptr
    if (!rst_n) begin
      wp_r   <= '0;
      wc_r   <= '0;
      drop_r <= 1'b0;
    end
    else if (in_acc) begin
      if (wdrop_w) begin
        drop_r <= !w_tlast_w;
        if (w_tlast_w) wp_r <= wc_r;
      end
      else begin
        wp_r <= wp_r + 1'b1;
        if (w_tlast_w) begin
          if (fw_good_w && !wshort_w) wc_r <= wp_r + 1'b1;
          else                        wp_r <= wc_r;
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
  logic [RQ_LOG2_C:0]       te_r;                        //! the pulse's frame's entry
  wire [RQ_LOG2_C-1:0]      rq_a_w = rq_ap_r[RQ_LOG2_C-1:0];
  wire [RQ_LOG2_C-1:0]      rq_h_w = rq_rp_r[RQ_LOG2_C-1:0];
  //! the stored frame ends with its PDU queued: its entry learns its fate
  wire                      fate_w = tl_w && fw_good_w;
  wire [RQ_LOG2_C-1:0]      fate_e_w = enq_tap_w ? rq_a_w : te_r[RQ_LOG2_C-1:0];
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
      te_r      <= '0;
      idxq_wp_r <= '0;
      idxq_rp_r <= '0;
      drop_p_o  <= 1'b0;
      drop_mask_o <= '0;
    end
    else begin
      drop_p_o <= 1'b0;
      //! an enqueue pulse takes the next entry, the frame's that passed its
      //! eighth beat last on the tap; its fate comes at that frame's tlast on
      //! the write side. A pulse no frame awaits is defensive only: its PDU
      //! is lost and its entry has its fate at once
      if (pdu_enq_p_i) begin
        rq_res_r[rq_a_w] <= !taw_r;
        rq_com_r[rq_a_w] <= 1'b0;
        rq_drp_r[rq_a_w] <= 1'b0;
        rq_ap_r          <= rq_ap_r + 1'b1;
        if (taw_r) te_r <= rq_ap_r;
      end
      if (fate_w) begin
        rq_res_r[fate_e_w] <= 1'b1;
        rq_com_r[fate_e_w] <= !wdrop_w && !wshort_w;
        rq_drp_r[fate_e_w] <= wdrop_w || wshort_w;
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
        //! a frame lost to the full store, or short of its payload: its
        //! accepting inputs' DEPKT drops
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
  //! the frame's last word leaves the payload's tail in the hold: it is not
  //! popped with this beat but with the final, hold-only one, so the frame's
  //! end, and the pass's (rewind or release), falls on the beat that carries
  //! tlast (#948)
  wire keep_w      = ff_last && (remain_r > 16'd8) &&
                     (remain_r <= 16'd8 + 16'(k_w));
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
  //! frame's inputs are known; payload beats when the emit is accepted, the
  //! kept last word with the hold-only beat; flush beats always)
  assign ff_ready = (rstate_r == R_HDR_S && (pass_r || sq_ne_w)) ||
                    (rstate_r == R_FLUSH_S) ||
                    (rstate_r == R_PAY_S && lead_ok_w && m_axis_tready &&
                     (hold_only_w ? ff_last : !keep_w));

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
              //! frame (its last word popped with it, a hold-only beat's
              //! kept word too); otherwise swallow padding/FCS-strip tail
              //! beats
              rstate_r <= (pop_w && ff_last) ? R_HDR_S : R_FLUSH_S;
            end
            else begin
              remain_r <= remain_r - 16'd8;
            end
          end
          //! truncated frame: defensive only, the write side commits a
          //! frame only with its whole payload (#948), so its last word is
          //! popped with the beat that carries tlast
          // verilator coverage_off
          if (pop_w && ff_last && !(emit_w && m_axis_tready && last_beat_w)) begin
            rstate_r <= R_HDR_S;
            rbeat_r  <= '0;
            remain_r <= '0;
          end
          // verilator coverage_on
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
