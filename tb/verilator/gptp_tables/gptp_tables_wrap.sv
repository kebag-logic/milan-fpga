/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : gptp_tables_wrap.sv
//  Project     : Milan AVB end-station -- gPTP plane table lockstep bench
//
//  Description : Issue #640, lane M7, moved six of the fabric gPTP plane's
//                tables into another storage form. This bench runs the real
//                plane (the whole `gptp_shadow` slice: tap, frame FIFOs,
//                engine, egress ledger, launch observer, link guard, PHC)
//                and, beside it, each table in the storage form it had
//                before. Every reference is written by the same conditions
//                the old RTL used, from signals the change did not touch,
//                and is compared every cycle with what the plane's consumer
//                of that table actually receives:
//
//                  rx_fifo  the tap's frame FIFO with eight tkeep bits,
//                           against the plane's lane-number FIFO
//                  tx_fifo  the transmit FIFO with eight tkeep bits, fed by
//                           the old gearbox enables, against the lane count
//                  bank     the engine's message bank as a 64 x 64 array
//                           read through the state port's register, against
//                           the two block RAMs and their output latch
//                  ledger   the egress ledger's type/sequence/tag fields as
//                           reset-cleared registers, against distributed RAM
//                  results  the egress result queue, likewise, at its head
//                           while it offers a result
//                  timer    the engine timer's deadlines, likewise, at the
//                           sweep slot whenever that slot is armed
//
//                Each table counts its mismatches and the coverage that
//                makes a zero count mean something; the harness grades both.
//---------------------------------------------------------------------------//
`default_nettype none

module gptp_tables_wrap #(
    parameter string       UCODE_HEX_P = "gptp_ucode.hex",
    parameter int unsigned CLK_HZ_P    = 2_000_000
) (
    input  wire        clk_i,
    input  wire        rst_n,
    //! clears every count below; the harness raises it once, at boot
    input  wire        cnt_clr_i,

    //! the MAC RX tap face and the plane's transmit lane, as in gptp_shadow
    input  wire [63:0] rx_tdata_i,
    input  wire  [7:0] rx_tkeep_i,
    input  wire        rx_tvalid_i,
    input  wire        rx_tready_i,
    input  wire        rx_tlast_i,
    output wire [63:0] tx_tdata_o,
    output wire  [7:0] tx_tkeep_o,
    output wire        tx_tvalid_o,
    output wire        tx_tlast_o,
    input  wire        tx_tready_i,

    //! test-only record delay, passed to the slice bench
    input  wire        rechold_en_i,
    input  wire  [3:0] rechold_type_i,
    input  wire        rechold_release_i,

    output wire [31:0] pub_flags_o,
    //! what the harness's peer needs: the plane's PHC and the egress result
    //! the engine accepted, so a peer answer can be timed against both
    output wire [63:0] phc_ns_o,
    output wire        dbg_eng_txts_v_o,
    output wire [63:0] dbg_eng_txts_ns_o,
    output wire [15:0] dbg_eng_txts_seq_o,
    output wire  [3:0] dbg_eng_txts_type_o,
    output wire        dbg_eng_txts_ok_o,
    output wire [15:0] dbg_tap_drop_o,
    output wire [15:0] dbg_rx_drop_o,
    output wire [15:0] dbg_ev_drop_o,
    output wire [15:0] dbg_prog_run_o,
    output wire [15:0] dbg_txts_lost_o,
    output wire [15:0] dbg_txts_barr_o,

    //! per-table mismatch counts: each must end at zero
    output logic [31:0] rx_mm_o,
    output logic [31:0] tx_mm_o,
    output logic [31:0] bank_mm_o,
    output logic [31:0] led_mm_o,
    output logic [31:0] res_mm_o,
    output logic [31:0] tmr_mm_o,

    //! per-table coverage: what the comparisons above actually saw
    output logic [31:0] rx_good_o,      //! frames the FIFO committed
    output logic [31:0] rx_ovf_o,       //! frames it dropped full or oversize
    output logic [31:0] rx_bad_o,       //! frames it dropped as bad
    output logic  [7:0] rx_tops_o,      //! highest lanes delivered, as a set
    output logic [31:0] rx_hiwater_o,   //! deepest occupancy, beats
    output logic [31:0] tx_frames_o,    //! frames that left the FIFO
    output logic  [8:0] tx_counts_o,    //! lane counts that left it, as a set
    output logic [31:0] tx_stall_o,     //! cycles a beat waited on ready
    output logic [31:0] tx_hiwater_o,   //! deepest occupancy, beats
    output logic [31:0] bank_reads_o,   //! state-port reads the bank answered
    output logic [31:0] bank_reads1_o,  //! ...of message bank 1
    output logic [31:0] bank_high_o,    //! ...of words 16..31
    output logic [31:0] bank_coll_o,    //! ...in the cycle the parser wrote that word
    output logic [31:0] led_cmp_o,      //! cycles the ledger head was compared
    output logic  [7:0] led_heads_o,    //! head entries compared, as a set
    output logic  [4:0] led_maxn_o,     //! deepest ledger occupancy
    output logic [31:0] res_cmp_o,      //! cycles a result head was compared
    output logic  [7:0] res_heads_o,    //! head entries compared, as a set
    output logic  [4:0] res_maxn_o,     //! deepest result occupancy
    output logic [31:0] tmr_cmp_o,      //! armed sweep reads compared
    output logic  [7:0] tmr_slots_o     //! slots compared, as a set
);

  // ======================================================================= //
  //  The plane, inside the gptp_shadow slice bench                          //
  // ======================================================================= //
  gptp_shadow_wrap #(
      .UCODE_HEX_P   (UCODE_HEX_P),
      .CLK_HZ_P      (CLK_HZ_P),
      .PHC_TICK_NS_P (8)
  ) u_bench (
      .clk_i             (clk_i),
      .rst_n             (rst_n),
      .rx_tdata_i        (rx_tdata_i),
      .rx_tkeep_i        (rx_tkeep_i),
      .rx_tvalid_i       (rx_tvalid_i),
      .rx_tready_i       (rx_tready_i),
      .rx_tlast_i        (rx_tlast_i),
      .tx_tdata_o        (tx_tdata_o),
      .tx_tkeep_o        (tx_tkeep_o),
      .tx_tvalid_o       (tx_tvalid_o),
      .tx_tlast_o        (tx_tlast_o),
      .tx_tready_i       (tx_tready_i),
      .rechold_en_i      (rechold_en_i),
      .rechold_type_i    (rechold_type_i),
      .rechold_release_i (rechold_release_i),
      .recfault_en_i     (1'b0),
      .recfault_mode_i   (2'd0),
      .linkg_dis_i       (1'b0),
      .linkg_freeze_i    (1'b0),
      .cfg_mac_reinit_i  (1'b0),
      .eth_alive_i       (1'b1),
      .obs_rst_i         (1'b0),
      .phc_en_i          (1'b1),
      .phc_incr_i        (32'h0800_0000),
      .phc_adj_ovr_en_i  (1'b0),
      .phc_adj_ovr_i     (32'sd0),
      .phc_load_i        (1'b0),
      .phc_tod_wr_i      (64'd0),
      .pub_flags_o       (pub_flags_o),
      .phc_ns_o          (phc_ns_o),
      .dbg_eng_txts_v_o  (dbg_eng_txts_v_o),
      .dbg_eng_txts_ns_o (dbg_eng_txts_ns_o),
      .dbg_eng_txts_seq_o(dbg_eng_txts_seq_o),
      .dbg_eng_txts_type_o(dbg_eng_txts_type_o),
      .dbg_eng_txts_ok_o (dbg_eng_txts_ok_o),
      .dbg_tap_drop_o    (dbg_tap_drop_o),
      .dbg_rx_drop_o     (dbg_rx_drop_o),
      .dbg_ev_drop_o     (dbg_ev_drop_o),
      .dbg_prog_run_o    (dbg_prog_run_o),
      .dbg_txts_lost_o   (dbg_txts_lost_o),
      .dbg_txts_barr_o   (dbg_txts_barr_o)
  );

  //! the plane's reset: the slice bench resets the plane with its own rst_n
  logic run_w;
  assign run_w = rst_n;

  // ======================================================================= //
  //  rx_fifo: the tap FIFO as it was, with eight tkeep bits                 //
  // ======================================================================= //
  logic [63:0] rr_data_w;
  logic  [7:0] rr_keep_w;
  logic        rr_valid_w, rr_last_w, rr_sready_w;
  logic        rr_ovf_w, rr_bad_w, rr_good_w;
  logic  [8:0] rr_depth_w;

  axis_fifo #(
    .DEPTH               (2048),
    .DATA_WIDTH          (64),
    .KEEP_ENABLE         (1),
    .KEEP_WIDTH          (8),
    .LAST_ENABLE         (1),
    .ID_ENABLE           (0),
    .DEST_ENABLE         (0),
    .USER_ENABLE         (1),
    .USER_WIDTH          (1),
    .FRAME_FIFO          (1),
    .USER_BAD_FRAME_VALUE(1'b1),
    .USER_BAD_FRAME_MASK (1'b1),
    .DROP_BAD_FRAME      (1),
    .DROP_OVERSIZE_FRAME (1),
    .DROP_WHEN_FULL      (1)
  ) u_ref_rx_fifo (
    .clk                (clk_i),
    .rst                (~run_w),
    .s_axis_tdata       (u_bench.u_shadow.fw_data_w),
    .s_axis_tkeep       (rx_tkeep_i),
    .s_axis_tvalid      (u_bench.u_shadow.fw_valid_w),
    .s_axis_tready      (rr_sready_w),
    .s_axis_tlast       (u_bench.u_shadow.fw_last_w),
    .s_axis_tid         ('0),
    .s_axis_tdest       ('0),
    .s_axis_tuser       (u_bench.u_shadow.fw_user_w),
    .m_axis_tdata       (rr_data_w),
    .m_axis_tkeep       (rr_keep_w),
    .m_axis_tvalid      (rr_valid_w),
    .m_axis_tready      (u_bench.u_shadow.ff_ready_w),
    .m_axis_tlast       (rr_last_w),
    .m_axis_tid         (),
    .m_axis_tdest       (),
    .m_axis_tuser       (),
    .status_overflow    (rr_ovf_w),
    .status_bad_frame   (rr_bad_w),
    .status_good_frame  (rr_good_w),
    .status_depth       (),
    .status_depth_commit(),
    .pause_req          (1'b0),
    .pause_ack          ()
  );
  //! occupancy in beats, from the reference's own pointers
  assign rr_depth_w = u_ref_rx_fifo.wr_ptr_reg - u_ref_rx_fifo.rd_ptr_reg;

  //! the serializer's old reading of tkeep: the highest enabled lane
  logic [2:0] rr_top_w;
  always_comb begin : ref_rx_top
    rr_top_w = 3'd0;
    for (int unsigned i = 0; i < 8; i++) if (rr_keep_w[i]) rr_top_w = 3'(i);
  end : ref_rx_top

  logic rx_bad_cyc_w;
  assign rx_bad_cyc_w =
      (rr_sready_w != u_bench.u_shadow.fw_ready_w) ||
      (rr_valid_w  != u_bench.u_shadow.ff_valid_w) ||
      (rr_ovf_w    != u_bench.u_shadow.ff_ovf_w)   ||
      (rr_bad_w    != u_bench.u_shadow.ff_bad_w)   ||
      (rr_good_w   != u_bench.u_shadow.ff_good_w)  ||
      (rr_valid_w && ((rr_data_w != u_bench.u_shadow.ff_data_w) ||
                      (rr_last_w != u_bench.u_shadow.ff_last_w) ||
                      (rr_top_w  != u_bench.u_shadow.ff_top_w)));

  // ======================================================================= //
  //  tx_fifo: the gearbox's old enables into the old eight-bit FIFO         //
  // ======================================================================= //
  logic [7:0] rt_gb_keep_r, rt_st_keep_r;
  always_ff @(posedge clk_i) begin : ref_gearbox_keep
    if (!run_w) begin
      rt_gb_keep_r <= '0;
      rt_st_keep_r <= '0;
    end else if (u_bench.u_shadow.tx_byte_w) begin
      rt_gb_keep_r[u_bench.u_shadow.gb_idx_r] <= 1'b1;
      if ((u_bench.u_shadow.gb_idx_r == 3'd7) || u_bench.u_shadow.eng_tx_eof_w) begin
        rt_st_keep_r <= rt_gb_keep_r | (8'd1 << u_bench.u_shadow.gb_idx_r);
        rt_gb_keep_r <= '0;
      end
    end
  end : ref_gearbox_keep

  logic [63:0] rt_data_w;
  logic  [7:0] rt_keep_w;
  logic        rt_valid_w, rt_last_w, rt_sready_w;

  axis_fifo #(
    .DEPTH               (2048),
    .DATA_WIDTH          (64),
    .KEEP_ENABLE         (1),
    .KEEP_WIDTH          (8),
    .LAST_ENABLE         (1),
    .ID_ENABLE           (0),
    .DEST_ENABLE         (0),
    .USER_ENABLE         (0),
    .FRAME_FIFO          (1),
    .DROP_BAD_FRAME      (0),
    .DROP_OVERSIZE_FRAME (0),
    .DROP_WHEN_FULL      (0)
  ) u_ref_tx_fifo (
    .clk                (clk_i),
    .rst                (~run_w),
    .s_axis_tdata       (u_bench.u_shadow.gbo_data_w),
    .s_axis_tkeep       (rt_st_keep_r),
    .s_axis_tvalid      (u_bench.u_shadow.gbo_valid_w),
    .s_axis_tready      (rt_sready_w),
    .s_axis_tlast       (u_bench.u_shadow.gbo_last_w),
    .s_axis_tid         ('0),
    .s_axis_tdest       ('0),
    .s_axis_tuser       ('0),
    .m_axis_tdata       (rt_data_w),
    .m_axis_tkeep       (rt_keep_w),
    .m_axis_tvalid      (rt_valid_w),
    .m_axis_tready      (u_bench.u_shadow.tx_tready_i),
    .m_axis_tlast       (rt_last_w),
    .m_axis_tid         (),
    .m_axis_tdest       (),
    .m_axis_tuser       (),
    .status_overflow    (),
    .status_bad_frame   (),
    .status_good_frame  (),
    .status_depth       (),
    .status_depth_commit(),
    .pause_req          (1'b0),
    .pause_ack          ()
  );
  logic [8:0] rt_depth_w;
  assign rt_depth_w = u_ref_tx_fifo.wr_ptr_reg - u_ref_tx_fifo.rd_ptr_reg;

  //! The FIFO output is the plane's own lane output, and tkeep and tdata are
  //! visible to the merge downstream in every cycle, so they are compared in
  //! every cycle and not only while valid.
  logic tx_bad_cyc_w;
  assign tx_bad_cyc_w =
      (rt_sready_w != u_bench.u_shadow.gbo_ready_w)     ||
      (rt_valid_w  != u_bench.u_shadow.txf_out_valid_w) ||
      (rt_last_w   != u_bench.u_shadow.txf_out_last_w)  ||
      (rt_data_w   != u_bench.u_shadow.tx_tdata_o)      ||
      (rt_keep_w   != u_bench.u_shadow.tx_tkeep_o);

  // ======================================================================= //
  //  bank: the message bank as the 64 x 64 distributed array it was        //
  // ======================================================================= //
  logic [63:0] rb_mem_r [0:63];
  logic [63:0] rb_rdata_r;
  initial begin : ref_bank_poweron
    for (int i = 0; i < 64; i++) rb_mem_r[i] = '0;
  end : ref_bank_poweron

  //! the old region-0 decode, written independently of the plane's
  //! st_rd_bank_w: a pending Pdelay_Req answers words 0, 2 and 3 from its
  //! snapshot, an Announce answers every word from its frozen context, and
  //! every other read of region 0 is the bank
  logic        rb_rd_w, rb_is_bank_w;
  logic  [5:0] rb_raddr_w, rb_waddr_w;
  logic  [4:0] rb_word_w;
  assign rb_word_w    = u_bench.u_shadow.u_engine.st_addr_w[4:0];
  assign rb_rd_w      = u_bench.u_shadow.u_engine.st_req_w &&
                        !u_bench.u_shadow.u_engine.st_we_w;
  assign rb_is_bank_w = (u_bench.u_shadow.u_engine.st_addr_w[19:16] == 4'd0) &&
                        (u_bench.u_shadow.u_engine.disp_pdreq_r
                           ? !((rb_word_w == 5'd0) || (rb_word_w == 5'd2) ||
                               (rb_word_w == 5'd3))
                           : !u_bench.u_shadow.u_engine.disp_announce_r);
  assign rb_raddr_w   = {u_bench.u_shadow.u_engine.disp_bank_r, rb_word_w};
  assign rb_waddr_w   = {u_bench.u_shadow.u_engine.bank_sel_r,
                         u_bench.u_shadow.u_engine.bank_addr_w};

  always_ff @(posedge clk_i) begin : ref_bank
    if (!run_w) begin
      rb_rdata_r <= '0;
    end else begin
      if (u_bench.u_shadow.u_engine.bank_we_w)
        rb_mem_r[rb_waddr_w] <= u_bench.u_shadow.u_engine.bank_wdata_w;
      if (rb_rd_w)
        rb_rdata_r <= rb_is_bank_w ? rb_mem_r[rb_raddr_w]
                                   : u_bench.u_shadow.u_engine.st_rd_mux_w;
    end
  end : ref_bank

  logic bank_bad_cyc_w;
  assign bank_bad_cyc_w = (rb_rdata_r != u_bench.u_shadow.u_engine.st_rdata_w);

  // ======================================================================= //
  //  ledger and results: the egress ledger's fields as reset registers      //
  // ======================================================================= //
  localparam int unsigned CAP_C = 8;   //! the slice's TXTS_CAP_N_P

  logic  [3:0] rl_type_r [0:CAP_C-1];
  logic [15:0] rl_seq_r  [0:CAP_C-1];
  logic        rl_tag_r  [0:CAP_C-1];
  logic [63:0] rq_ns_r   [0:CAP_C-1];
  logic [15:0] rq_seq_r  [0:CAP_C-1];
  logic  [3:0] rq_type_r [0:CAP_C-1];
  logic        rq_ok_r   [0:CAP_C-1];
  logic  [3:0] rq_gen_r  [0:CAP_C-1];

  logic [2:0] rl_head_w, rl_tail_w, rq_head_w, rq_tail_w;
  logic [4:0] rl_n_w, rq_n_w;
  assign rl_head_w = u_bench.u_shadow.u_txret.led_head_r;
  assign rl_tail_w = u_bench.u_shadow.u_txret.led_tail_w;
  assign rl_n_w    = 5'(u_bench.u_shadow.u_txret.n_led_r);
  assign rq_head_w = u_bench.u_shadow.u_txret.res_head_r;
  assign rq_tail_w = u_bench.u_shadow.u_txret.res_tail_w;
  assign rq_n_w    = 5'(u_bench.u_shadow.u_txret.n_res_r);

  always_ff @(posedge clk_i) begin : ref_ledger
    if (!run_w) begin
      for (int unsigned i = 0; i < CAP_C; i++) begin
        rl_type_r[i] <= 4'd0;
        rl_seq_r [i] <= 16'd0;
        rl_tag_r [i] <= 1'b0;
        rq_ns_r  [i] <= 64'd0;
        rq_seq_r [i] <= 16'd0;
        rq_type_r[i] <= 4'd0;
        rq_ok_r  [i] <= 1'b0;
        rq_gen_r [i] <= 4'd0;
      end
    end else begin
      if (u_bench.u_shadow.u_txret.alloc_i && (rl_n_w != 5'(CAP_C))) begin
        rl_type_r[rl_tail_w] <= u_bench.u_shadow.u_txret.alloc_type_i;
        rl_seq_r [rl_tail_w] <= u_bench.u_shadow.u_txret.alloc_seq_i;
        rl_tag_r [rl_tail_w] <= u_bench.u_shadow.u_txret.alloc_tagged_i;
      end
      if (u_bench.u_shadow.u_txret.push_res_w) begin
        rq_ns_r  [rq_tail_w] <= u_bench.u_shadow.u_txret.res_ns_w;
        rq_seq_r [rq_tail_w] <= rl_seq_r [rl_head_w];
        rq_type_r[rq_tail_w] <= rl_type_r[rl_head_w];
        rq_ok_r  [rq_tail_w] <= u_bench.u_shadow.u_txret.res_ok_w;
        rq_gen_r [rq_tail_w] <= u_bench.u_shadow.u_txret.gen_r;
      end
    end
  end : ref_ledger

  //! the ledger is read at its head while it holds an entry: the tag check,
  //! the measurement verdict and the fields the result queue copies
  logic led_on_w, led_bad_cyc_w;
  assign led_on_w = run_w && (rl_n_w != 5'd0);
  assign led_bad_cyc_w = led_on_w && (
      (u_bench.u_shadow.u_txret.led_type_r[rl_head_w] != rl_type_r[rl_head_w]) ||
      (u_bench.u_shadow.u_txret.led_seq_r [rl_head_w] != rl_seq_r [rl_head_w]) ||
      (u_bench.u_shadow.u_txret.led_tag_r [rl_head_w] != rl_tag_r [rl_head_w]));

  //! the engine takes the queue head only on an accepted valid/ready beat,
  //! so the head is graded whenever it is offered
  logic res_on_w, res_bad_cyc_w;
  assign res_on_w = run_w && u_bench.u_shadow.u_txret.txts_valid_o;
  assign res_bad_cyc_w = res_on_w && (
      (u_bench.u_shadow.u_txret.txts_ns_o   != rq_ns_r  [rq_head_w]) ||
      (u_bench.u_shadow.u_txret.txts_seq_o  != rq_seq_r [rq_head_w]) ||
      (u_bench.u_shadow.u_txret.txts_type_o != rq_type_r[rq_head_w]) ||
      (u_bench.u_shadow.u_txret.txts_ok_o   != rq_ok_r  [rq_head_w]) ||
      (u_bench.u_shadow.u_txret.txts_gen_o  != rq_gen_r [rq_head_w]));

  // ======================================================================= //
  //  timer: the engine timer's deadlines as reset registers                 //
  // ======================================================================= //
  logic [31:0] rd_mem_r [0:7];
  always_ff @(posedge clk_i) begin : ref_deadlines
    if (!run_w) begin
      for (int unsigned i = 0; i < 8; i++) rd_mem_r[i] <= 32'd0;
    end else if (u_bench.u_shadow.u_engine.u_timer.arm_we_i) begin
      rd_mem_r[u_bench.u_shadow.u_engine.u_timer.arm_slot_i] <=
          u_bench.u_shadow.u_engine.u_timer.ms_now_r +
          u_bench.u_shadow.u_engine.u_timer.arm_delta_ms_i;
    end
  end : ref_deadlines

  //! the sweep reads a deadline only through delta_w, and only for an armed
  //! slot; that is the comparison
  logic [2:0]  tm_slot_w;
  logic        tmr_on_w, tmr_bad_cyc_w;
  logic signed [31:0] tm_delta_w;
  assign tm_slot_w  = u_bench.u_shadow.u_engine.u_timer.sweep_r;
  assign tmr_on_w   = run_w && u_bench.u_shadow.u_engine.u_timer.armed_r[tm_slot_w];
  assign tm_delta_w = $signed(rd_mem_r[tm_slot_w] -
                              u_bench.u_shadow.u_engine.u_timer.ms_now_r);
  assign tmr_bad_cyc_w = tmr_on_w &&
      (tm_delta_w != u_bench.u_shadow.u_engine.u_timer.delta_w);

  // ======================================================================= //
  //  Counters                                                               //
  // ======================================================================= //
  //! the bank coverage is counted on the read the reference answered
  logic bank_rd_bank_w;
  assign bank_rd_bank_w = run_w && rb_rd_w && rb_is_bank_w;

  always_ff @(posedge clk_i) begin : counters
    //! the counts survive a warm reset: a run is graded whole
    if (cnt_clr_i) begin
      rx_mm_o <= '0; tx_mm_o <= '0; bank_mm_o <= '0;
      led_mm_o <= '0; res_mm_o <= '0; tmr_mm_o <= '0;
      rx_good_o <= '0; rx_ovf_o <= '0; rx_bad_o <= '0; rx_tops_o <= '0;
      rx_hiwater_o <= '0; tx_frames_o <= '0; tx_counts_o <= '0;
      tx_stall_o <= '0; tx_hiwater_o <= '0; bank_reads_o <= '0;
      bank_reads1_o <= '0; bank_high_o <= '0; bank_coll_o <= '0;
      led_cmp_o <= '0; led_heads_o <= '0; led_maxn_o <= '0;
      res_cmp_o <= '0; res_heads_o <= '0; res_maxn_o <= '0;
      tmr_cmp_o <= '0; tmr_slots_o <= '0;
    end else if (run_w) begin
      if (rx_bad_cyc_w)   rx_mm_o   <= rx_mm_o + 32'd1;
      if (tx_bad_cyc_w)   tx_mm_o   <= tx_mm_o + 32'd1;
      if (bank_bad_cyc_w) bank_mm_o <= bank_mm_o + 32'd1;
      if (led_bad_cyc_w)  led_mm_o  <= led_mm_o + 32'd1;
      if (res_bad_cyc_w)  res_mm_o  <= res_mm_o + 32'd1;
      if (tmr_bad_cyc_w)  tmr_mm_o  <= tmr_mm_o + 32'd1;

      if (rr_good_w) rx_good_o <= rx_good_o + 32'd1;
      if (rr_ovf_w)  rx_ovf_o  <= rx_ovf_o + 32'd1;
      if (rr_bad_w)  rx_bad_o  <= rx_bad_o + 32'd1;
      if (rr_valid_w && u_bench.u_shadow.ff_ready_w)
        rx_tops_o[rr_top_w] <= 1'b1;
      if (32'(rr_depth_w) > rx_hiwater_o) rx_hiwater_o <= 32'(rr_depth_w);

      if (rt_valid_w && u_bench.u_shadow.tx_tready_i) begin
        if (rt_last_w) tx_frames_o <= tx_frames_o + 32'd1;
        tx_counts_o[$countones(rt_keep_w)] <= 1'b1;
      end
      if (rt_valid_w && !u_bench.u_shadow.tx_tready_i)
        tx_stall_o <= tx_stall_o + 32'd1;
      if (32'(rt_depth_w) > tx_hiwater_o) tx_hiwater_o <= 32'(rt_depth_w);

      if (bank_rd_bank_w) begin
        bank_reads_o <= bank_reads_o + 32'd1;
        if (rb_raddr_w[5]) bank_reads1_o <= bank_reads1_o + 32'd1;
        if (rb_raddr_w[4]) bank_high_o   <= bank_high_o + 32'd1;
        if (u_bench.u_shadow.u_engine.bank_we_w && (rb_waddr_w == rb_raddr_w))
          bank_coll_o <= bank_coll_o + 32'd1;
      end

      if (led_on_w) begin
        led_cmp_o <= led_cmp_o + 32'd1;
        led_heads_o[rl_head_w] <= 1'b1;
      end
      if (rl_n_w > led_maxn_o) led_maxn_o <= rl_n_w;
      if (res_on_w) begin
        res_cmp_o <= res_cmp_o + 32'd1;
        res_heads_o[rq_head_w] <= 1'b1;
      end
      if (rq_n_w > res_maxn_o) res_maxn_o <= rq_n_w;
      if (tmr_on_w) begin
        tmr_cmp_o <= tmr_cmp_o + 32'd1;
        tmr_slots_o[tm_slot_w] <= 1'b1;
      end
    end
  end : counters

endmodule : gptp_tables_wrap
`default_nettype wire
