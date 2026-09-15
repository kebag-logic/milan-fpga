/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : gptp_shadow_wrap.sv
//  Project     : Milan AVB end-station -- gPTP fabric-slice bench
//
//  Description : Testbench wrap of the WHOLE fabric slice the splice
//                instantiates: KL_gptp_shadow (tap + engine + lane + the
//                egress ledger), the real timestamp_counter it steers, and
//                the REAL KL_gptp_gmii_launch observing an octet stream this
//                wrapper frames out of the plane's own transmit lane. NO
//                timestamp enters from the harness: ingress stamps come from
//                the tap's commit-FIFO transport, egress results from the
//                observer and the ledger -- the loop closes entirely in
//                fabric.
//
//                WHAT THE FRAMER IS, AND WHAT IT IS NOT. `bench_framer`
//                below turns the plane's 64-bit lane into a contiguous
//                octet stream with a preamble, a start-of-frame delimiter
//                and an inter-frame gap, store-and-forward so a frame never
//                starts until it is whole. That is enough to drive the real
//                observer and to give this bench an INDEPENDENT launch
//                reference (`dbg_launch_*`, the PHC sampled at the edge the
//                framer presents frame octet 0). It is NOT the product MAC:
//                it has no width converter, no FCS, no padding, no
//                clock-domain crossing and no queueing behind other
//                traffic, so it proves NOTHING about launch latency through
//                the shipping transmit chain. The causal proof over the
//                generated production MAC is tb/verilator/gptp_txts; this
//                bench proves the plane's own ownership, ordering and
//                reconstruction arithmetic.
//---------------------------------------------------------------------------//
`default_nettype none

module gptp_shadow_wrap #(
    parameter string       UCODE_HEX_P = "gptp_ucode.hex",
    parameter int unsigned CLK_HZ_P    = 2_000_000,
    //! the PHC in this bench runs the 125 MHz shape (8.0 ns per tick) while
    //! the bench clock is CLK_HZ_P, so the plane is TOLD the shape rather
    //! than deriving a tick from a clock that does not carry it
    parameter int unsigned PHC_TICK_NS_P = 8
) (
    input  wire clk_i,
    input  wire rst_n,

    //! the MAC RX tap face (wide)
    input  wire [63:0] rx_tdata_i,
    input  wire [7:0]  rx_tkeep_i,
    input  wire        rx_tvalid_i,
    input  wire        rx_tready_i,
    input  wire        rx_tlast_i,

    //! the TX lane out (wide), observed by the harness; the bench framer
    //! below is its consumer, gated by this ready so a phase can still stall
    //! the lane between frames
    output wire [63:0] tx_tdata_o,
    output wire [7:0]  tx_tkeep_o,
    output wire        tx_tvalid_o,
    output wire        tx_tlast_o,
    input  wire        tx_tready_i,

    //! Test-only RECORD delay. The launch record of one selected
    //! messageType can be held back and released later, which is what a
    //! record that arrives late looks like to the ledger. Nothing is
    //! fabricated: the held record is the observer's own.
    input  wire        rechold_en_i,
    input  wire [3:0]  rechold_type_i,
    input  wire        rechold_release_i,

    //! THE REAL LINK GUARD runs inside this wrapper, at a scaled settle so
    //! a bench can afford a whole episode. Its FSM, its trigger set, its
    //! sequenced eth-then-sys release and its disable behaviour are the
    //! product's; only `SETTLE_CYC_C` is smaller. The harness drives its
    //! controls, not its outputs, so the plane's recovery demand is graded
    //! against a guard that can refuse it.
    input  wire        linkg_dis_i,      //! LINK_CTRL[2]
    input  wire        linkg_freeze_i,   //! LINK_CTRL[3]
    input  wire        cfg_mac_reinit_i, //! LINK_CTRL[1], the firmware hand
    input  wire        eth_alive_i,      //! 0 stops both eth clocks
    //! hold the observer in reset without touching the plane: the
    //! independent-observer-reset arm
    input  wire        obs_rst_i,

    //! THE PHC's OWN CONTROLS, driven into the real counter. A phase that
    //! wants to prove the reconstruction refuses a trajectory outside the
    //! model moves the counter itself, not a status bit the plane reads.
    input  wire        phc_en_i,        //! 0 holds the counter
    input  wire [31:0] phc_incr_i,      //! Q8.24 nominal step, ns
    input  wire        phc_adj_ovr_en_i,//! 1 = force the addend below
    input  wire signed [31:0] phc_adj_ovr_i,
    input  wire        phc_load_i,      //! settime strobe
    input  wire [63:0] phc_tod_wr_i,

    //! the steered clock, observable
    output wire [63:0] phc_ns_o,

    //! publish bank
    output wire [63:0] pub_gm_id_o,
    output wire [63:0] pub_parent_id_o,
    output wire [31:0] pub_flags_o,
    output wire [31:0] pub_pdelay_ns_o,
    output wire [31:0] pub_offset_o,
    output wire [63:0] pub_annq_o,
    output wire  [3:0] pub_path_count_o,
    output wire [63:0] pub_path_tail0_o,
    output wire [63:0] pub_path_tail1_o,
    output wire [63:0] pub_path_tail6_o,
    output wire  [3:0] pub_path_gen_o,
    output wire        pub_commit_o,
    output wire        pub_disc_o,

    //! Consumer-equivalent registers sample tu on the publication edge.
    output logic        aaf_launch_tu_o,
    output logic        crf_launch_tu_o,
    output logic [15:0] disc_launch_count_o,
    output wire         ts_uncertain_o,

    //! diagnostics
    output wire [15:0] dbg_tap_drop_o,
    output wire [15:0] dbg_rx_drop_o,
    output wire [63:0] dbg_rx_ts_o,
    output wire        dbg_tspush_v_o,
    output wire [63:0] dbg_tspush_o,
    output wire        dbg_tspop_v_o,
    //! how many times the engine's uCPU has STARTED a program
    output wire [15:0] dbg_prog_run_o,
    output wire [15:0] dbg_ev_drop_o,

    //! THE INDEPENDENT LAUNCH REFERENCE: the PHC sampled at the edge the
    //! framer presents frame octet 0, the octet the standard's message
    //! timestamp point names. It is taken at the framer, not inside the
    //! observer, so the reconstruction under test is compared against
    //! something it did not produce.
    output logic        dbg_launch_v_o,
    output logic [63:0] dbg_launch_phc_o,
    output logic  [3:0] dbg_launch_type_o,
    output logic [15:0] dbg_launch_seq_o,

    //! the observer's own records, before the test-only delay
    output wire        dbg_rec_v_o,
    output wire        dbg_rec_kind_o,
    output wire [11:0] dbg_rec_oidx_o,
    output wire  [3:0] dbg_rec_gen_o,
    output wire  [3:0] dbg_rec_type_o,
    output wire [15:0] dbg_rec_seq_o,
    output wire  [7:0] dbg_rec_delta_o,
    output wire        dbg_rec_abort_o,
    output wire [15:0] dbg_rec_ovr_o,
    //! the held record, if any
    output wire         dbg_rec_held_o,
    output wire   [3:0] dbg_rec_held_type_o,
    output wire  [15:0] dbg_rec_held_seq_o,
    //! the record as the plane finally receives it, and whether the
    //! test-only queue delayed it. A delayed record is captured against a
    //! LATER PHC value, which is a fixture artefact and not a behaviour the
    //! wire can produce, so the reconstruction law excludes exactly these.
    output wire         dbg_dut_rec_v_o,
    output wire         dbg_dut_rec_kind_o,
    output wire         dbg_dut_rec_delayed_o,

    //! the tuple the engine ACCEPTED, sampled at its accepted beat
    output wire        dbg_eng_txts_v_o,
    output wire [63:0] dbg_eng_txts_ns_o,
    output wire [15:0] dbg_eng_txts_seq_o,
    output wire  [3:0] dbg_eng_txts_type_o,
    output wire        dbg_eng_txts_ok_o,
    output wire  [3:0] dbg_eng_txts_gen_o,

    //! the guard, observed
    output wire        dbg_linkg_reinit_o,
    output wire        dbg_linkg_eth_rst_o,
    output wire        dbg_linkg_epi_start_o,
    output wire        dbg_linkg_epi_done_o,
    output wire        dbg_linkg_epi_busy_o,
    output wire        dbg_recov_req_o,
    output logic [15:0] dbg_recov_req_cnt_o,
    output logic [15:0] dbg_epi_done_cnt_o,

    //! ledger diagnostics
    output wire [15:0] dbg_txts_lost_o,
    output wire [15:0] dbg_txts_disc_o,
    output wire [15:0] dbg_txts_barr_o,
    output wire [15:0] dbg_txts_stall_o,
    output wire [15:0] dbg_txts_phcl_o,
    output wire  [7:0] dbg_phc_dirtcyc_o,
    output wire signed [31:0] dbg_phc_adj_o,
    output wire [15:0] dbg_txts_state_o,
    output wire [15:0] dbg_txts_torn_o
);

  localparam int unsigned FO_DEPTH_C = 512;
  localparam int unsigned FO_AW_C    = 9;    //! $clog2(FO_DEPTH_C)
  localparam int unsigned IFG_C      = 12;
  localparam logic [7:0]  PREAMBLE_C = 8'h55;
  localparam logic [7:0]  SFD_C      = 8'hD5;

  logic               busy_w;
  logic signed [31:0] adj_w;
  logic               step_we_w;
  logic [63:0]        step_w;
  logic               pub_disc_w;
  logic [7*64-1:0]    pub_path_w;
  logic               obs_rst_n_w;

  logic        rec_v_w, rec_kind_w, rec_abort_w;
  logic [11:0] rec_oidx_w;
  logic  [3:0] rec_gen_w, rec_type_w;
  logic [15:0] rec_seq_w;
  logic  [7:0] rec_delta_w;
  logic        seal_req_w, seal_ack_w;
  logic  [3:0] seal_gen_w;

  logic        dut_rec_v_w, dut_rec_kind_w, dut_rec_abort_w;
  logic [11:0] dut_rec_oidx_w;
  logic  [3:0] dut_rec_gen_w, dut_rec_type_w;
  logic [15:0] dut_rec_seq_w;
  logic  [7:0] dut_rec_delta_w;

  logic        gmii_v_r;
  logic  [7:0] gmii_d_r;
  logic        lane_ready_w, lane_beat_w;
  logic        linkg_reinit_w, linkg_eth_rst_w;
  logic        epi_start_w, epi_done_w, epi_busy_w;
  logic        recov_req_w;
  logic        eth_tgl_r;
  logic        mac_rst_n_w;

  //! the addend the counter really sees: the plane's servo, or the
  //! phase's override when it is proving the envelope
  logic signed [31:0] adj_eff_w;
  assign adj_eff_w = phc_adj_ovr_en_i ? phc_adj_ovr_i : adj_w;

  timestamp_counter #(
      .COUNTER_WIDTH (64),
      .INCR_WIDTH    (32),
      .FRAC_WIDTH    (24)
  ) u_phc (
      .clk                  (clk_i),
      .resetn               (rst_n),
      .enable_i             (phc_en_i),
      .incr_i               (phc_incr_i),
      .adj_i                (adj_eff_w),
      .tod_wr_i             (phc_tod_wr_i),
      .cmd_load_i           (phc_load_i),
      .offset_i             ($signed(step_w)),
      .cmd_adjust_i         (step_we_w),
      .cmd_snapshot_i       (1'b0),
      .timestamp_out        (phc_ns_o),
      .tod_snapshot_o       (),
      .tod_snapshot_valid_o ()
  );

  KL_gptp_shadow #(
      .TDATA_WIDTH_P (64),
      .CLK_HZ_P      (CLK_HZ_P),
      .UCODE_HEX_P   (UCODE_HEX_P),
      .PHC_TICK_NS_P (PHC_TICK_NS_P),
      .ETH_TICK_NS_P (PHC_TICK_NS_P)
  ) u_shadow (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .rx_tdata_i      (rx_tdata_i),
      .rx_tkeep_i      (rx_tkeep_i),
      .rx_tvalid_i     (rx_tvalid_i),
      .rx_tready_i     (rx_tready_i),
      .rx_tlast_i      (rx_tlast_i),
      .phc_ns_i        (phc_ns_o),
      //! the SAME nets the counter is driven with, which is the point
      .phc_en_eff_i    (phc_en_i),
      .phc_incr_eff_ns_i(phc_incr_i),
      .phc_adj_eff_ns_i(adj_eff_w),
      .phc_load_eff_i  (phc_load_i),
      .phc_adjust_eff_i(step_we_w),
      .phc_adj_o       (adj_w),
      .phc_step_we_o   (step_we_w),
      .phc_step_o      (step_w),
      .tx_tdata_o      (tx_tdata_o),
      .tx_tkeep_o      (tx_tkeep_o),
      .tx_tvalid_o     (tx_tvalid_o),
      .tx_tlast_o      (tx_tlast_o),
      .tx_tready_i     (lane_ready_w),
      .rec_valid_i     (dut_rec_v_w),
      .rec_kind_i      (dut_rec_kind_w),
      .rec_oidx_i      (dut_rec_oidx_w),
      .rec_gen_i       (dut_rec_gen_w),
      .rec_type_i      (dut_rec_type_w),
      .rec_seq_i       (dut_rec_seq_w),
      .rec_delta_i     (dut_rec_delta_w),
      .rec_abort_i     (dut_rec_abort_w),
      .seal_req_o      (seal_req_w),
      .seal_gen_o      (seal_gen_w),
      .seal_ack_i      (seal_ack_w),
      .mac_reinit_i    (linkg_reinit_w),
      .mac_eth_rst_i   (linkg_eth_rst_w),
      .epi_start_i     (epi_start_w),
      .epi_done_i      (epi_done_w),
      .epi_busy_i      (epi_busy_w),
      .epi_dis_i       (linkg_dis_i),
      .recov_req_o     (recov_req_w),
      .pub_gm_id_o     (pub_gm_id_o),
      .pub_parent_id_o (pub_parent_id_o),
      .pub_flags_o     (pub_flags_o),
      .pub_pdelay_ns_o (pub_pdelay_ns_o),
      .pub_offset_o    (pub_offset_o),
      .pub_annq_o      (pub_annq_o),
      .pub_path_count_o(pub_path_count_o),
      .pub_path_o      (pub_path_w),
      .pub_path_gen_o  (pub_path_gen_o),
      .pub_commit_o    (pub_commit_o),
      .pub_disc_o      (pub_disc_w),
      .dbg_tap_drop_o  (dbg_tap_drop_o),
      .dbg_rx_drop_o   (dbg_rx_drop_o),
      .dbg_ev_drop_o   (dbg_ev_drop_o),
      .dbg_busy_o      (busy_w),
      .dbg_rx_ts_o     (dbg_rx_ts_o),
      .dbg_tspush_v_o  (dbg_tspush_v_o),
      .dbg_tspush_o    (dbg_tspush_o),
      .dbg_tspop_v_o   (dbg_tspop_v_o),
      .dbg_txts_lost_o (dbg_txts_lost_o),
      .dbg_txts_disc_o (dbg_txts_disc_o),
      .dbg_txts_barr_o (dbg_txts_barr_o),
      .dbg_txts_stall_o(dbg_txts_stall_o),
      .dbg_txts_phcl_o (dbg_txts_phcl_o),
      .dbg_txts_dirt_cyc_o(dbg_phc_dirtcyc_o),
      .dbg_txts_state_o(dbg_txts_state_o),
      .dbg_txts_torn_o (dbg_txts_torn_o)
  );

  // ======================================================================= //
  //  The real link guard, at a bench-scaled settle                          //
  // ======================================================================= //
  //! One divide-by-2 toggle per eth clock, exactly as the SoC builds them,
  //! so `eth_alive_i` low is a stopped clock and not a poked status bit.
  always_ff @(posedge clk_i) begin : eth_toggles
    if (!rst_n)          eth_tgl_r <= 1'b0;
    else if (eth_alive_i) eth_tgl_r <= ~eth_tgl_r;
  end : eth_toggles

  KL_link_guard #(
      .DEAD_CYC_C   (64),
      .SETTLE_CYC_C (1024)
  ) u_guard (
      .clk_i        (clk_i),
      .rst_n        (rst_n),
      .rx_tgl_i     (eth_tgl_r),
      .tx_tgl_i     (eth_tgl_r),
      .act_tgl_i    (1'b0),
      .dis_i        (linkg_dis_i),
      .freeze_i     (linkg_freeze_i),
      .man_reinit_i (cfg_mac_reinit_i | recov_req_w),
      .reinit_o     (linkg_reinit_w),
      .eth_rst_o    (linkg_eth_rst_w),
      .link_est_o   (),
      .stat_o       (),
      .epi_start_o  (epi_start_w),
      .epi_done_o   (epi_done_w),
      .epi_busy_o   (epi_busy_w)
  );

  assign dbg_linkg_reinit_o    = linkg_reinit_w;
  assign dbg_linkg_eth_rst_o   = linkg_eth_rst_w;
  assign dbg_linkg_epi_start_o = epi_start_w;
  assign dbg_linkg_epi_done_o  = epi_done_w;
  assign dbg_linkg_epi_busy_o  = epi_busy_w;
  assign dbg_recov_req_o       = recov_req_w;

  always_ff @(posedge clk_i) begin : guard_counts
    if (!rst_n) begin
      dbg_recov_req_cnt_o <= 16'd0;
      dbg_epi_done_cnt_o  <= 16'd0;
    end else begin
      if (recov_req_w) dbg_recov_req_cnt_o <= dbg_recov_req_cnt_o + 16'd1;
      if (epi_done_w)  dbg_epi_done_cnt_o  <= dbg_epi_done_cnt_o + 16'd1;
    end
  end : guard_counts

  //! The MAC side this wrapper stands in for: the framer and the observer
  //! are cleared by the guard's eth-side reset, which is exactly what
  //! `eth_rst` does to the LiteEth transmit side, the PHY transmit stage
  //! and the real observer in the product.
  assign mac_rst_n_w = rst_n & ~linkg_eth_rst_w;

  assign dbg_phc_adj_o = adj_eff_w;
  assign pub_disc_o = pub_disc_w;
  assign pub_path_tail0_o = pub_path_w[0*64 +: 64];
  assign pub_path_tail1_o = pub_path_w[1*64 +: 64];
  assign pub_path_tail6_o = pub_path_w[6*64 +: 64];

  // ======================================================================= //
  //  Bench framer: the plane's 64-bit lane -> a contiguous octet stream     //
  // ======================================================================= //
  //! Store and forward, like the boundary it stands in for: a frame starts
  //! only once it is whole, so the observer never sees a fragment this
  //! wrapper created rather than one a phase asked for.
  logic [8:0]        fo_mem_r [0:FO_DEPTH_C-1];
  logic [FO_AW_C-1:0] fo_wp_r, fo_rp_r;
  logic [7:0]        fo_frames_r;

  //! the framer takes a beat whenever it has room; a phase can still stall
  //! the lane through `tx_tready_i`, which parks whole frames in the plane's
  //! own transmit FIFO exactly as downstream backpressure does
  assign lane_ready_w = tx_tready_i;
  assign lane_beat_w  = tx_tvalid_o & lane_ready_w;

  logic [2:0] lane_top_w;
  always_comb begin : lane_top
    lane_top_w = 3'd0;
    for (int unsigned i = 0; i < 8; i++) if (tx_tkeep_o[i]) lane_top_w = 3'(i);
  end : lane_top

  typedef enum logic [1:0] {FR_IDLE, FR_PRE, FR_DATA, FR_GAP} fr_state_e;
  fr_state_e  fr_S;
  logic [3:0] fr_cnt_r;
  logic [8:0] fo_rd_w;
  assign fo_rd_w = fo_mem_r[fo_rp_r];

  logic fo_pop_w;
  assign fo_pop_w = (fr_S == FR_DATA);

  logic push_frame_w, pop_frame_w;
  assign push_frame_w = lane_beat_w & tx_tlast_o;
  assign pop_frame_w  = fo_pop_w & fo_rd_w[8];

  always_ff @(posedge clk_i) begin : framer_push
    if (!mac_rst_n_w) begin
      fo_wp_r     <= '0;
      fo_frames_r <= 8'd0;
    end else begin
      if (lane_beat_w) begin
        int unsigned n;
        n = 0;
        for (int unsigned k = 0; k < 8; k++) begin
          if (tx_tkeep_o[k]) begin
            fo_mem_r[FO_AW_C'(fo_wp_r + FO_AW_C'(n))] <=
                {tx_tlast_o & (3'(k) == lane_top_w), tx_tdata_o[8*k +: 8]};
            n = n + 1;
          end
        end
        fo_wp_r <= FO_AW_C'(fo_wp_r + FO_AW_C'(n));
      end
      //! a whole frame arrives and a whole frame leaves in the same cycle:
      //! the count is unchanged, which is why these are netted rather than
      //! written one after the other
      if (push_frame_w & ~pop_frame_w)      fo_frames_r <= fo_frames_r + 8'd1;
      else if (~push_frame_w & pop_frame_w) fo_frames_r <= fo_frames_r - 8'd1;
    end
  end : framer_push

  always_ff @(posedge clk_i) begin : framer_emit
    if (!mac_rst_n_w) begin
      fr_S       <= FR_IDLE;
      fr_cnt_r   <= 4'd0;
      fo_rp_r    <= '0;
      gmii_v_r   <= 1'b0;
      gmii_d_r   <= 8'd0;
    end else begin
      gmii_v_r <= 1'b0;
      unique case (fr_S)
        FR_IDLE: begin
          if (|fo_frames_r) begin
            fr_S     <= FR_PRE;
            fr_cnt_r <= 4'd0;
            gmii_v_r <= 1'b1;
            gmii_d_r <= PREAMBLE_C;
          end
        end
        FR_PRE: begin
          gmii_v_r <= 1'b1;
          gmii_d_r <= (fr_cnt_r == 4'd6) ? SFD_C : PREAMBLE_C;
          if (fr_cnt_r == 4'd6) fr_S <= FR_DATA;
          fr_cnt_r <= fr_cnt_r + 4'd1;
        end
        FR_DATA: begin
          gmii_v_r <= 1'b1;
          gmii_d_r <= fo_rd_w[7:0];
          fo_rp_r  <= FO_AW_C'(fo_rp_r + FO_AW_C'(1));
          if (fo_rd_w[8]) begin
            fr_S     <= FR_GAP;
            fr_cnt_r <= 4'd0;
          end else if (fr_cnt_r != 4'd15) begin
            fr_cnt_r <= fr_cnt_r + 4'd1;
          end
        end
        default: begin   //! FR_GAP
          if (fr_cnt_r == 4'(IFG_C - 1)) begin
            fr_S     <= FR_IDLE;
            fr_cnt_r <= 4'd0;
          end else begin
            fr_cnt_r <= fr_cnt_r + 4'd1;
          end
        end
      endcase
    end
  end : framer_emit

  //! THE INDEPENDENT LAUNCH REFERENCE. Counted over the octets the framer
  //! PRESENTS, so it shares no state with the observer's own pipeline. The
  //! PHC is sampled one edge after the reference octet, because the
  //! accumulator value present over an interval is the one written at its
  //! start: sampling at the reference edge itself would report the tick
  //! before the launch.
  logic [7:0] lo_idx_r;
  logic       lo_inf_r;
  logic [7:0] lo_nidx_w;
  assign lo_nidx_w = lo_inf_r ? ((lo_idx_r == 8'd255) ? lo_idx_r
                                                      : lo_idx_r + 8'd1)
                              : 8'd0;

  always_ff @(posedge clk_i) begin : launch_tag
    if (!mac_rst_n_w) begin
      lo_idx_r          <= 8'd0;
      lo_inf_r          <= 1'b0;
      dbg_launch_v_o    <= 1'b0;
      dbg_launch_phc_o  <= 64'd0;
      dbg_launch_type_o <= 4'd0;
      dbg_launch_seq_o  <= 16'd0;
    end else begin
      dbg_launch_v_o <= 1'b0;
      if (gmii_v_r) begin
        lo_idx_r <= lo_nidx_w;
        lo_inf_r <= 1'b1;
        if (lo_nidx_w == 8'd9) begin
          dbg_launch_v_o   <= 1'b1;
          dbg_launch_phc_o <= phc_ns_o;
        end
        if (lo_nidx_w == 8'd22) dbg_launch_type_o      <= gmii_d_r[3:0];
        if (lo_nidx_w == 8'd52) dbg_launch_seq_o[15:8] <= gmii_d_r;
        if (lo_nidx_w == 8'd53) dbg_launch_seq_o[7:0]  <= gmii_d_r;
      end else begin
        lo_inf_r <= 1'b0;
      end
    end
  end : launch_tag

  // ======================================================================= //
  //  The real observer, on the framed octet stream                          //
  // ======================================================================= //
  assign obs_rst_n_w = mac_rst_n_w & ~obs_rst_i;

  KL_gptp_gmii_launch #(
      .REF_OCTET_P      (8),
      .TYPE_OCTET_P     (22),
      .TAG_OCTET_HI_P   (52),
      .TAG_OCTET_LO_P   (53),
      .TXTS_DELTA_EXP_P (45)
  ) u_launch (
      .eth_clk_i     (clk_i),
      .eth_rst_n     (obs_rst_n_w),
      .gmii_tvalid_i (gmii_v_r),
      .gmii_tdata_i  (gmii_d_r),
      .dp_clk_i      (clk_i),
      .dp_rst_n      (rst_n),
      .rec_valid_o   (rec_v_w),
      .rec_kind_o    (rec_kind_w),
      .rec_oidx_o    (rec_oidx_w),
      .rec_gen_o     (rec_gen_w),
      .rec_type_o    (rec_type_w),
      .rec_seq_o     (rec_seq_w),
      .rec_delta_o   (rec_delta_w),
      .rec_abort_o   (rec_abort_w),
      .seal_req_i    (seal_req_w),
      .seal_gen_i    (seal_gen_w),
      .seal_ack_o    (seal_ack_w),
      .dbg_overrun_o (dbg_rec_ovr_o)
  );

  assign dbg_rec_v_o     = rec_v_w;
  assign dbg_rec_kind_o  = rec_kind_w;
  assign dbg_rec_oidx_o  = rec_oidx_w;
  assign dbg_rec_gen_o   = rec_gen_w;
  assign dbg_rec_type_o  = rec_type_w;
  assign dbg_rec_seq_o   = rec_seq_w;
  assign dbg_rec_delta_o = rec_delta_w;
  assign dbg_rec_abort_o = rec_abort_w;

  // ======================================================================= //
  //  Test-only record delay, ORDER PRESERVING                               //
  // ======================================================================= //
  //! One record of a selected messageType is held at the head of an ordered
  //! queue and released later. Every record behind it waits, which is what
  //! a late record really does to an ordered ledger: the phases that use
  //! this are proving exactly that, and that nothing is mis-credited while
  //! it is held. Nothing is fabricated - the held record is the observer's.
  localparam int unsigned RQ_DEPTH_C = 8;
  localparam int unsigned RQ_W_C     = 1 + 12 + 4 + 4 + 16 + 8 + 1 + 1;

  logic [RQ_W_C-1:0] rq_mem_r [0:RQ_DEPTH_C-1];
  logic        [2:0] rq_wp_r, rq_rp_r;
  logic        [3:0] rq_n_r;
  logic        [1:0] rq_gap_r;
  logic              arm_r, held_r;

  logic [RQ_W_C-1:0] rq_in_w, rq_head_w;
  //! a record that cannot be drained on the very next cycle has been
  //! delayed by this fixture; the flag travels with it
  logic push_delayed_w;
  assign push_delayed_w = (rq_n_r != 4'd0) | hold_now_w | (|rq_gap_r);
  assign rq_in_w   = {rec_kind_w, rec_oidx_w, rec_gen_w, rec_type_w,
                      rec_seq_w, rec_delta_w, rec_abort_w, push_delayed_w};
  assign rq_head_w = rq_mem_r[rq_rp_r];

  logic       rq_head_kind_w, rq_head_abort_w, rq_head_delayed_w;
  logic [3:0] rq_head_type_w;
  logic [15:0] rq_head_seq_w;
  assign {rq_head_kind_w, dut_rec_oidx_w, dut_rec_gen_w, rq_head_type_w,
          rq_head_seq_w, dut_rec_delta_w, rq_head_abort_w,
          rq_head_delayed_w} = rq_head_w;
  assign dut_rec_kind_w  = rq_head_kind_w;
  assign dut_rec_type_w  = rq_head_type_w;
  assign dut_rec_seq_w   = rq_head_seq_w;
  assign dut_rec_abort_w = rq_head_abort_w;

  logic head_match_w, hold_now_w;
  assign head_match_w = (rq_n_r != 4'd0) & ~rq_head_kind_w &
                        (rq_head_type_w == rechold_type_i);
  assign hold_now_w   = held_r | (arm_r & head_match_w);
  //! The real crossing cannot present two records back to back - its
  //! request/acknowledge round trip is many cycles and the frames that
  //! produce them are a whole inter-frame gap apart - and KL_gptp_txret
  //! asserts that. This queue must not manufacture a spacing the wire never
  //! produces, so a drained record is followed by two idle cycles.
  assign dut_rec_v_w  = (rq_n_r != 4'd0) & ~hold_now_w & (rq_gap_r == 2'd0);

  always_ff @(posedge clk_i) begin : record_queue
    if (!rst_n) begin
      rq_wp_r <= 3'd0;
      rq_rp_r <= 3'd0;
      rq_n_r   <= 4'd0;
      rq_gap_r <= 2'd0;
      arm_r    <= 1'b0;
      held_r   <= 1'b0;
    end else begin
      if (dut_rec_v_w)          rq_gap_r <= 2'd2;
      else if (|rq_gap_r)       rq_gap_r <= rq_gap_r - 2'd1;
      if (rec_v_w) begin
        rq_mem_r[rq_wp_r] <= rq_in_w;
        rq_wp_r           <= rq_wp_r + 3'd1;
      end
      if (dut_rec_v_w) rq_rp_r <= rq_rp_r + 3'd1;
      if (rec_v_w & ~dut_rec_v_w)      rq_n_r <= rq_n_r + 4'd1;
      else if (~rec_v_w & dut_rec_v_w) rq_n_r <= rq_n_r - 4'd1;

      if (rechold_en_i && !held_r)              arm_r  <= 1'b1;
      if (arm_r && head_match_w && !held_r)     held_r <= 1'b1;
      if (held_r && rechold_release_i) begin
        held_r <= 1'b0;
        arm_r  <= 1'b0;
      end
    end
  end : record_queue

  //! a head that has been held at least one cycle was delayed even if it
  //! found the queue empty when it arrived
  logic head_held_r;
  always_ff @(posedge clk_i) begin : head_held
    if (!rst_n)              head_held_r <= 1'b0;
    else if (hold_now_w)     head_held_r <= 1'b1;
    else if (dut_rec_v_w)    head_held_r <= 1'b0;
  end : head_held

  assign dbg_rec_held_o       = hold_now_w;
  assign dbg_rec_held_type_o  = rq_head_type_w;
  assign dbg_rec_held_seq_o   = rq_head_seq_w;
  assign dbg_dut_rec_v_o      = dut_rec_v_w;
  assign dbg_dut_rec_kind_o   = dut_rec_kind_w;
  assign dbg_dut_rec_delayed_o = rq_head_delayed_w | head_held_r;

  // ======================================================================= //
  //  The engine's accepted result, observed at its accepted beat            //
  // ======================================================================= //
  assign dbg_eng_txts_v_o    = u_shadow.eng_txts_valid_w & u_shadow.eng_txts_ready_w;
  assign dbg_eng_txts_ns_o   = u_shadow.eng_txts_ns_w;
  assign dbg_eng_txts_seq_o  = u_shadow.eng_txts_seq_w;
  assign dbg_eng_txts_type_o = u_shadow.eng_txts_type_w;
  assign dbg_eng_txts_ok_o   = u_shadow.eng_txts_ok_w;
  assign dbg_eng_txts_gen_o  = u_shadow.eng_txts_gen_w;

  KL_ptp_clock_validity #(
      .QTICK_CYC_P   (64),
      .HOLD_QTICK_P  (2),
      .FABRIC_GPTP_P (1)
  ) u_validity (
      .clk_i            (clk_i),
      .rst_n            (rst_n),
      .fabric_sync_ok_i (pub_flags_o[3]),
      .fabric_as_cap_i  (pub_flags_o[2]),
      .fabric_disc_p_i  (pub_disc_w),
      .phc_load_p_i     (1'b0),
      .phc_adj_p_i      (step_we_w),
      .gm_id_i          (pub_gm_id_o),
      .ts_uncertain_o   (ts_uncertain_o),
      .as_capable_o     (),
      .stat_o           (),
      .tu_ivals_o       ()
  );

  always_ff @(posedge clk_i) begin : same_edge_talker_sampling
    if (!rst_n) begin
      aaf_launch_tu_o     <= 1'b0;
      crf_launch_tu_o     <= 1'b0;
      disc_launch_count_o <= 16'd0;
    end else if (pub_disc_w) begin
      aaf_launch_tu_o     <= ts_uncertain_o;
      crf_launch_tu_o     <= ts_uncertain_o;
      disc_launch_count_o <= disc_launch_count_o + 16'd1;
    end
  end : same_edge_talker_sampling

  //! program-start counter: one per rising edge of the engine's busy line
  logic        busy_r;
  logic [15:0] prog_run_r;
  always_ff @(posedge clk_i) begin : prog_run
    if (!rst_n) begin
      busy_r     <= 1'b0;
      prog_run_r <= '0;
    end else begin
      busy_r <= busy_w;
      if (busy_w && !busy_r) prog_run_r <= prog_run_r + 16'd1;
    end
  end : prog_run
  assign dbg_prog_run_o = prog_run_r;

endmodule : gptp_shadow_wrap
`default_nettype wire
