/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : gptp_txts_wrap.sv
//  Project     : Milan AVB end-station -- the gPTP egress timestamp closed
//                loop (issue #360)
//
//  Description : ONE live simulation containing the real donor engine, the
//                real gPTP plane and its egress ledger, the real
//                timestamp_counter, the real launch observer, the real link
//                guard, the real merge arbiter, and the SHIPPING MAC
//                TRANSMIT CHAIN converted from the product's own migen
//                source by sw/litex/gen_mac_tx_model.py - both `mac_tx_cdc`
//                halves, `tx_sf`, the LiteEth core with its preamble, FCS,
//                padding, width conversion and inter-frame gap, and the PHY
//                transmit register stage - at the true 125:50 clock ratio.
//
//                WHY A CONVERTED MAC AND NOT A MODEL. The defect this work
//                repairs is that the old timestamp preceded exactly this
//                chain, by an amount that depends on what else is queued.
//                A bench that models the chain proves what the model does,
//                and one that replays a recorded trace proves the bytes of
//                that trace. Here every frame byte, every launch time,
//                every ready and every reset response is produced by the
//                design, and the bench drives only the datapath boundary,
//                the clocks and the recovery controls.
//
//                THE TWO SEAMS. The launch observer under test reads
//                `phy.sink`, the product connection, exported from the
//                converted chain. The bench's independent oracle reads the
//                PADS. They are two distinct signals in the same live run,
//                one register stage apart, and the bench measures that
//                relationship rather than assuming it.
//
//                CLOCK SHAPE. `dp_clk_i` carries the plane, the PHC, the
//                guard and the merge; `eth_clk_i` carries the observer and
//                the MAC transmit side; `sys_clk_i` carries the MAC system
//                side. The PHC runs the product's 20 ns tick and the
//                observation domain the product's 8 ns one, so the egress
//                correction this bench grades is the product's own 426 ns
//                and not a bench number. The engine's own timers are
//                generated for a faster second so a protocol run fits in a
//                simulation; that changes no timestamp arithmetic.
//---------------------------------------------------------------------------//
`default_nettype none

module gptp_txts_wrap #(
    parameter string       UCODE_HEX_P = "gptp_ucode.hex",
    parameter int unsigned CLK_HZ_P    = 2_000_000,
    //! the product's PHC tick and observation tick, stated because this
    //! bench's engine clock is deliberately faster than the product's
    parameter int unsigned PHC_TICK_NS_P = 20,
    parameter int unsigned ETH_TICK_NS_P = 8,
    //! the guard's settle, scaled so a bench can afford a whole episode.
    //! Everything else about the guard is the product's.
    parameter int unsigned SETTLE_CYC_C = 1024
) (
    input  wire dp_clk_i,       //! the plane, the PHC, the guard, the merge
    input  wire dp_rst_n,
    input  wire sys_clk_i,      //! the MAC system side
    input  wire sys_rst_n,
    input  wire eth_clk_i,      //! the MAC transmit side and the observer
    input  wire eth_rst_n,

    //! the plane's RX tap: peer frames enter here, through the real
    //! classifier, the real frame FIFO and the real serializer
    input  wire [63:0] rx_tdata_i,
    input  wire  [7:0] rx_tkeep_i,
    input  wire        rx_tvalid_i,
    input  wire        rx_tready_i,
    input  wire        rx_tlast_i,

    //! background traffic, entering the SAME merge the product puts in
    //! front of the MAC, so a plane frame really does queue behind it
    input  wire [63:0] bg_tdata_i,
    input  wire  [7:0] bg_tkeep_i,
    input  wire        bg_tvalid_i,
    input  wire        bg_tlast_i,
    output wire        bg_tready_o,

    //! the link guard's controls, and the eth clocks it watches
    input  wire linkg_dis_i,
    input  wire linkg_freeze_i,
    input  wire cfg_mac_reinit_i,
    input  wire eth_alive_i,

    //! the PHC's own controls, driven into the real counter
    input  wire        phc_en_i,
    input  wire [31:0] phc_incr_i,
    input  wire        phc_adj_ovr_en_i,
    input  wire signed [31:0] phc_adj_ovr_i,
    input  wire        phc_load_i,
    input  wire [63:0] phc_tod_wr_i,

    //! FAULT INJECTION, observer side only: hold the observer's view of
    //! `phy.sink.valid` low for the cycles this is asserted. It models a
    //! frame fragmented on the wire. The pads in this arm still show the
    //! whole frame, because the converted chain computes them from the
    //! same stream one register later, so this arm proves the OBSERVER
    //! refuses a fragmented frame and says nothing about the pads.
    input  wire obs_bubble_i,
    //! hold the observer in reset without touching anything else
    input  wire obs_rst_i,

    //! the PHC, observable
    output wire [63:0] phc_ns_o,

    //! THE PADS: the independent oracle's only input
    output wire        gmii_tx_en_o,
    output wire  [7:0] gmii_tx_data_o,
    //! THE SEAM: what the observer under test reads
    output wire        phy_sink_v_o,
    output wire  [7:0] phy_sink_d_o,
    //! the plane's own transmit lane, so the bench can read the frames the
    //! plane committed without reaching into the merge
    output wire [63:0] gtx_tdata_o,
    output wire  [7:0] gtx_tkeep_o,
    output wire        gtx_tvalid_o,
    output wire        gtx_tlast_o,
    output wire        gtx_tready_o,

    //! the tuple the engine ACCEPTED, at its accepted beat
    output wire        eng_txts_v_o,
    output wire [63:0] eng_txts_ns_o,
    output wire [15:0] eng_txts_seq_o,
    output wire  [3:0] eng_txts_type_o,
    output wire        eng_txts_ok_o,

    //! the observer's records, before the plane sees them
    output wire        rec_v_o,
    output wire        rec_kind_o,
    output wire [11:0] rec_oidx_o,
    output wire  [3:0] rec_type_o,
    output wire [15:0] rec_seq_o,
    output wire  [7:0] rec_delta_o,
    output wire        rec_abort_o,

    //! the plane's publication and diagnostics
    output wire [31:0] pub_flags_o,
    output wire [31:0] pub_pdelay_ns_o,
    output wire [15:0] dbg_txts_lost_o,
    output wire [15:0] dbg_txts_disc_o,
    output wire [15:0] dbg_txts_barr_o,
    output wire [15:0] dbg_txts_stall_o,
    output wire [15:0] dbg_txts_phcl_o,
    output wire [15:0] dbg_txts_torn_o,
    output wire  [7:0] dbg_txts_dirt_cyc_o,
    output wire [15:0] dbg_txts_state_o,
    output wire [15:0] dbg_rec_ovr_o,

    //! the seams between the plane and the MAC, so a bench can say WHERE a
    //! frame stopped instead of only that none arrived
    output wire dbg_eng_tx_v_o,
    output wire dbg_eng_tx_rdy_o,
    output wire dbg_mrg_tvalid_o,
    output wire dbg_mrg_tready_o,
    output wire dbg_busy_o,
    output wire dbg_eng_rx_v_o,
    output wire dbg_eng_rx_sof_o,
    output wire [15:0] dbg_tap_drop_o,
    output wire [15:0] dbg_rx_drop_o,
    output wire [15:0] dbg_ev_drop_o,

    //! the guard, observed
    output wire dbg_linkg_reinit_o,
    output wire dbg_linkg_eth_rst_o,
    output wire dbg_linkg_epi_done_o,
    output wire dbg_linkg_epi_busy_o,
    output wire dbg_recov_req_o
);

  // ======================================================================= //
  //  The PHC the plane steers, and the plane itself                         //
  // ======================================================================= //
  logic signed [31:0] adj_w, adj_eff_w;
  logic               step_we_w;
  logic        [63:0] step_w;
  assign adj_eff_w = phc_adj_ovr_en_i ? phc_adj_ovr_i : adj_w;

  timestamp_counter #(
      .COUNTER_WIDTH (64),
      .INCR_WIDTH    (32),
      .FRAC_WIDTH    (24)
  ) u_phc (
      .clk                  (dp_clk_i),
      .resetn               (dp_rst_n),
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

  logic        linkg_reinit_w, linkg_eth_rst_w;
  logic        epi_start_w, epi_done_w, epi_busy_w, recov_req_w;
  logic        rec_v_w, rec_kind_w, rec_abort_w;
  logic [11:0] rec_oidx_w;
  logic  [3:0] rec_gen_w, rec_type_w;
  logic [15:0] rec_seq_w;
  logic  [7:0] rec_delta_w;
  logic        seal_req_w, seal_ack_w;
  logic  [3:0] seal_gen_w;

  KL_gptp_shadow #(
      .TDATA_WIDTH_P (64),
      .CLK_HZ_P      (CLK_HZ_P),
      .UCODE_HEX_P   (UCODE_HEX_P),
      .PHC_TICK_NS_P (PHC_TICK_NS_P),
      .ETH_TICK_NS_P (ETH_TICK_NS_P)
  ) u_shadow (
      .clk_i            (dp_clk_i),
      .rst_n            (dp_rst_n),
      .rx_tdata_i       (rx_tdata_i),
      .rx_tkeep_i       (rx_tkeep_i),
      .rx_tvalid_i      (rx_tvalid_i),
      .rx_tready_i      (rx_tready_i),
      .rx_tlast_i       (rx_tlast_i),
      .phc_ns_i         (phc_ns_o),
      .phc_en_eff_i     (phc_en_i),
      .phc_incr_eff_ns_i(phc_incr_i),
      .phc_adj_eff_ns_i (adj_eff_w),
      .phc_load_eff_i   (phc_load_i),
      .phc_adjust_eff_i (step_we_w),
      .phc_adj_o        (adj_w),
      .phc_step_we_o    (step_we_w),
      .phc_step_o       (step_w),
      .tx_tdata_o       (gtx_tdata_o),
      .tx_tkeep_o       (gtx_tkeep_o),
      .tx_tvalid_o      (gtx_tvalid_o),
      .tx_tlast_o       (gtx_tlast_o),
      .tx_tready_i      (gtx_tready_o),
      .rec_valid_i      (rec_v_w),
      .rec_kind_i       (rec_kind_w),
      .rec_oidx_i       (rec_oidx_w),
      .rec_gen_i        (rec_gen_w),
      .rec_type_i       (rec_type_w),
      .rec_seq_i        (rec_seq_w),
      .rec_delta_i      (rec_delta_w),
      .rec_abort_i      (rec_abort_w),
      .seal_req_o       (seal_req_w),
      .seal_gen_o       (seal_gen_w),
      .seal_ack_i       (seal_ack_w),
      .mac_reinit_i     (linkg_reinit_w),
      .mac_eth_rst_i    (linkg_eth_rst_w),
      .epi_start_i      (epi_start_w),
      .epi_done_i       (epi_done_w),
      .epi_busy_i       (epi_busy_w),
      .epi_dis_i        (linkg_dis_i),
      .recov_req_o      (recov_req_w),
      .pub_gm_id_o      (),
      .pub_parent_id_o  (),
      .pub_flags_o      (pub_flags_o),
      .pub_pdelay_ns_o  (pub_pdelay_ns_o),
      .pub_offset_o     (),
      .pub_annq_o       (),
      .pub_path_count_o (),
      .pub_path_o       (),
      .pub_path_gen_o   (),
      .pub_commit_o     (),
      .pub_disc_o       (),
      .dbg_tap_drop_o   (dbg_tap_drop_o),
      .dbg_rx_drop_o    (dbg_rx_drop_o),
      .dbg_ev_drop_o    (dbg_ev_drop_o),
      .dbg_busy_o       (dbg_busy_o),
      .dbg_rx_ts_o      (),
      .dbg_tspush_v_o   (),
      .dbg_tspush_o     (),
      .dbg_tspop_v_o    (),
      .dbg_txts_lost_o  (dbg_txts_lost_o),
      .dbg_txts_disc_o  (dbg_txts_disc_o),
      .dbg_txts_barr_o  (dbg_txts_barr_o),
      .dbg_txts_stall_o (dbg_txts_stall_o),
      .dbg_txts_phcl_o  (dbg_txts_phcl_o),
      .dbg_txts_dirt_cyc_o(dbg_txts_dirt_cyc_o),
      .dbg_txts_state_o (dbg_txts_state_o),
      .dbg_txts_torn_o  (dbg_txts_torn_o)
  );

  assign eng_txts_v_o    = u_shadow.eng_txts_valid_w & u_shadow.eng_txts_ready_w;
  assign eng_txts_ns_o   = u_shadow.eng_txts_ns_w;
  assign eng_txts_seq_o  = u_shadow.eng_txts_seq_w;
  assign eng_txts_type_o = u_shadow.eng_txts_type_w;
  assign eng_txts_ok_o   = u_shadow.eng_txts_ok_w;

  assign rec_v_o     = rec_v_w;
  assign rec_kind_o  = rec_kind_w;
  assign rec_oidx_o  = rec_oidx_w;
  assign rec_type_o  = rec_type_w;
  assign rec_seq_o   = rec_seq_w;
  assign rec_delta_o = rec_delta_w;
  assign rec_abort_o = rec_abort_w;

  // ======================================================================= //
  //  The merge the product puts in front of the MAC                         //
  // ======================================================================= //
  //! The plane's lane joins the rest of the control traffic through the
  //! product's own arbiter, at the product's own no-progress window, so a
  //! plane frame really does queue behind a background frame and the
  //! arbiter's frame lock is the one under test.
  logic [63:0] mrg_tdata_w;
  logic  [7:0] mrg_tkeep_w;
  logic        mrg_tvalid_w, mrg_tlast_w, mrg_tready_w;

  adp_tx_arbiter #(.DATA_WIDTH(64), .TO_LOG2_P(16)) u_merge (
      .clk_i        (dp_clk_i),
      .rst_n        (dp_rst_n),
      .s_data_tdata (bg_tdata_i),
      .s_data_tkeep (bg_tkeep_i),
      .s_data_tvalid(bg_tvalid_i),
      .s_data_tlast (bg_tlast_i),
      .s_data_tready(bg_tready_o),
      .s_adp_tdata  (gtx_tdata_o),
      .s_adp_tkeep  (gtx_tkeep_o),
      .s_adp_tvalid (gtx_tvalid_o),
      .s_adp_tlast  (gtx_tlast_o),
      .s_adp_tready (gtx_tready_o),
      .m_tdata      (mrg_tdata_w),
      .m_tkeep      (mrg_tkeep_w),
      .m_tvalid     (mrg_tvalid_w),
      .m_tlast      (mrg_tlast_w),
      .m_tready     (mrg_tready_w),
      .diag_locked_o(),
      .abort_evt_o  (),
      .stall_evt_o  ()
  );

  //! THE RETIRED CAPTURE POINT. The old egress timestamp was latched at a
  //! plane frame's first accepted beat at the datapath's MAC boundary. The
  //! merge in front of it is a combinational mux that locks a frame from
  //! tlast to tlast, so that beat IS the plane lane's own first accepted
  //! beat, which this wrapper already exports. The baseline control
  //! derives the old timestamp from it and measures how far it is from
  //! the launch - which is the whole defect, stated as a number.

  // ======================================================================= //
  //  The converted shipping MAC transmit chain                              //
  // ======================================================================= //
  logic maceth_tx_rst_w;

  mac_tx_chain u_mac (
      .sys_clk        (sys_clk_i),
      .sys_rst        (~sys_rst_n),
      .dp_clk         (dp_clk_i),
      .dp_rst         (~dp_rst_n),
      .eth_tx_clk     (eth_clk_i),
      .eth_rx_clk     (eth_clk_i),
      .eth_phy_rst    (~eth_rst_n),
      .reinit         (linkg_reinit_w),
      .eth_rst        (linkg_eth_rst_w),
      .loopback       (1'b0),
      .dp_tdata       (mrg_tdata_w),
      .dp_tkeep       (mrg_tkeep_w),
      .dp_tvalid      (mrg_tvalid_w),
      .dp_tlast       (mrg_tlast_w),
      .dp_tready      (mrg_tready_w),
      .gmii_tx_en     (gmii_tx_en_o),
      .gmii_tx_data   (gmii_tx_data_o),
      .gmii_tx_er     (),
      .phy_sink_valid (phy_sink_v_o),
      .phy_sink_ready (),
      .phy_sink_data  (phy_sink_d_o),
      .phy_sink_last  (),
      .maceth_tx_rst  (maceth_tx_rst_w)
  );

  // ======================================================================= //
  //  The launch observer, on the product's own seam                         //
  // ======================================================================= //
  logic obs_valid_w;
  //! the fault-injection gate, and nothing else, sits between the exported
  //! seam and the observer
  assign obs_valid_w = phy_sink_v_o & ~obs_bubble_i;

  KL_gptp_gmii_launch #(
      .REF_OCTET_P      (8),
      .TYPE_OCTET_P     (22),
      .TAG_OCTET_HI_P   (52),
      .TAG_OCTET_LO_P   (53),
      .TXTS_DELTA_EXP_P (45)
  ) u_launch (
      .eth_clk_i     (eth_clk_i),
      .eth_rst_n     (~maceth_tx_rst_w & ~obs_rst_i),
      .gmii_tvalid_i (obs_valid_w),
      .gmii_tdata_i  (phy_sink_d_o),
      .dp_clk_i      (dp_clk_i),
      .dp_rst_n      (dp_rst_n),
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

  // ======================================================================= //
  //  The real link guard, at a bench-scaled settle                          //
  // ======================================================================= //
  logic eth_tgl_r;
  always_ff @(posedge eth_clk_i) begin : eth_toggle
    if (eth_alive_i) eth_tgl_r <= ~eth_tgl_r;
  end : eth_toggle

  KL_link_guard #(
      .DEAD_CYC_C   (64),
      .SETTLE_CYC_C (SETTLE_CYC_C)
  ) u_guard (
      .clk_i        (dp_clk_i),
      .rst_n        (dp_rst_n),
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

  assign dbg_eng_rx_v_o   = u_shadow.eng_rx_valid_w;
  assign dbg_eng_rx_sof_o = u_shadow.eng_rx_sof_w;
  assign dbg_eng_tx_v_o   = u_shadow.eng_tx_valid_w;
  assign dbg_eng_tx_rdy_o = u_shadow.eng_tx_ready_w;
  assign dbg_mrg_tvalid_o = mrg_tvalid_w;
  assign dbg_mrg_tready_o = mrg_tready_w;

  assign dbg_linkg_reinit_o   = linkg_reinit_w;
  assign dbg_linkg_eth_rst_o  = linkg_eth_rst_w;
  assign dbg_linkg_epi_done_o = epi_done_w;
  assign dbg_linkg_epi_busy_o = epi_busy_w;
  assign dbg_recov_req_o      = recov_req_w;

endmodule : gptp_txts_wrap
`default_nettype wire
