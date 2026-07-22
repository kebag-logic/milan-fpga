/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_rx.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : lwSRP receive chain: monitor tap -> packet FIFO -> streaming
//                walker -> registrar (docs/LWSRP_FPGA_ARCHITECTURE.md §3).
//                One module so the datapath integration and the Verilator
//                bridge-PDU suite drive the identical boundary.
//
//                rx_leaveall_p_o is exported for the applicant (KL_lwsrp_tx
//                re-declares promptly on a received LeaveAll).
//---------------------------------------------------------------------------//

`default_nettype none

module KL_lwsrp_rx #(
  parameter int FIFO_DEPTH_BYTES_P = 2048,
  //! extra context match lanes (see KL_lwsrp_walker); tie ext_en_i = 0
  //! on unused lanes — the default single lane then synthesizes away
  parameter int unsigned EXT_LANES_P = 1
)(
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire         enable_i,          //! lwSRP engine enable (CSR)
    input  wire         tick_1khz_i,       //! 1 ms strobe (KL_lwsrp_timers)

    // ---- RX monitor tap (MAC RX AXIS, little lane, inputs only) --------
    input  wire         rx_tvalid_i,
    input  wire [63:0]  rx_tdata_i,
    input  wire [7:0]   rx_tkeep_i,
    input  wire         rx_tlast_i,

    // ---- our identity -----------------------------------------------------
    input  wire [47:0]  station_mac_i,     //! [47:40] = first wire byte
    input  wire [15:0]  unique_id_i,
    input  wire [11:0]  vid_i,

    // ---- listener-side bound stream (ACMP listener SM) --------------------
    input  wire [63:0]  lsid_i,
    input  wire         lsid_en_i,
    output wire         ta_registered_o,   //! TalkerAdvertise registered
    output wire         ta_failed_o,       //! TalkerFailed registered
    output wire [7:0]   ta_fail_code_o,
    output wire [11:0]  ta_vlan_o,         //! registered Talker-attr vlan
    output wire [31:0]  ta_acclat_o,       //! ...AccumulatedLatency
    output wire [63:0]  ta_fail_bridge_o,  //! ...TF bridge_id (listener side)

    // ---- registration state (to bw_gate / CSR) ---------------------------
    output wire         listener_ready_o,
    output wire         listener_reg_o,
    output wire [1:0]   listener_decl_o,
    output wire         domain_ok_o,
    output wire         tfail_valid_o,
    output wire [7:0]   tfail_code_o,
    output wire [63:0]  tfail_bridge_o,    //! our-talker TF bridge_id
    output wire         rx_leaveall_p_o,   //! to the applicant (re-declare)

    // ---- extra context lanes (context table; en=0 lanes inert) -----------
    input  wire [EXT_LANES_P*64-1:0] ext_sid_i,
    input  wire [EXT_LANES_P-1:0]    ext_en_i,
    output wire [EXT_LANES_P-1:0]    ext_lstn_p_o,
    output wire [EXT_LANES_P-1:0]    ext_tadv_p_o,
    output wire [EXT_LANES_P-1:0]    ext_tfail_p_o,
    output wire [EXT_LANES_P*3-1:0]  ext_evt_o,
    output wire [EXT_LANES_P*2-1:0]  ext_par_o,
    output wire [7:0]                ext_tfail_code_o,

    // ---- diagnostics -------------------------------------------------------
    output wire [15:0]  rx_pdus_o,         //! matched MRPDU frames accepted
    output wire [7:0]   rx_drops_o,        //! frames dropped (FIFO full)
    output wire [15:0]  pdu_cnt_o          //! cleanly parsed PDUs
);

  wire [63:0] f_tdata;
  wire [7:0]  f_tkeep;
  wire        f_tvalid, f_tlast, f_tuser, f_tready;

  KL_lwsrp_ingress #(.FIFO_DEPTH_BYTES_P(FIFO_DEPTH_BYTES_P)) ingress (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (enable_i),
    .rx_tvalid_i (rx_tvalid_i), .rx_tdata_i (rx_tdata_i),
    .rx_tkeep_i (rx_tkeep_i),   .rx_tlast_i (rx_tlast_i),
    .m_tdata (f_tdata), .m_tkeep (f_tkeep), .m_tvalid (f_tvalid),
    .m_tlast (f_tlast), .m_tuser (f_tuser), .m_tready (f_tready),
    .rx_pdus_o (rx_pdus_o), .rx_drops_o (rx_drops_o)
  );

  wire        w_leaveall_p;
  wire        w_domain_p;
  wire [7:0]  w_domain_class, w_domain_prio;
  wire [15:0] w_domain_vid;
  wire [2:0]  w_domain_evt;
  wire        w_listener_p;
  wire [2:0]  w_listener_evt;
  wire [1:0]  w_listener_decl;
  wire        w_tadv_p, w_tfail_p;
  wire [7:0]  w_tfail_code;
  wire [11:0] w_tk_vlan;
  wire [31:0] w_tk_acclat;
  wire [63:0] w_tk_bridge;
  wire        w_l_tadv_p, w_l_tfail_p;
  wire [2:0]  w_l_evt;
  wire [7:0]  w_l_tfail_code;

  assign rx_leaveall_p_o = w_leaveall_p;

  KL_lwsrp_walker #(.EXT_LANES_P(EXT_LANES_P)) walker (
    .clk_i (clk_i), .rst_n (rst_n),
    .s_tdata (f_tdata), .s_tkeep (f_tkeep), .s_tvalid (f_tvalid),
    .s_tlast (f_tlast), .s_tuser (f_tuser), .s_tready (f_tready),
    .station_mac_i (station_mac_i), .unique_id_i (unique_id_i),
    .lsid_i (lsid_i), .lsid_en_i (lsid_en_i),
    .ext_sid_i (ext_sid_i), .ext_en_i (ext_en_i),
    .ext_lstn_p_o (ext_lstn_p_o), .ext_tadv_p_o (ext_tadv_p_o),
    .ext_tfail_p_o (ext_tfail_p_o),
    .ext_evt_o (ext_evt_o), .ext_par_o (ext_par_o),
    .ext_tfail_code_o (ext_tfail_code_o),
    .leaveall_p_o (w_leaveall_p),
    .domain_p_o (w_domain_p),
    .domain_class_o (w_domain_class), .domain_prio_o (w_domain_prio),
    .domain_vid_o (w_domain_vid),     .domain_evt_o (w_domain_evt),
    .listener_p_o (w_listener_p),
    .listener_evt_o (w_listener_evt), .listener_decl_o (w_listener_decl),
    .tadv_p_o (w_tadv_p),
    .tfail_p_o (w_tfail_p), .tfail_code_o (w_tfail_code),
    .tk_vlan_o (w_tk_vlan), .tk_acclat_o (w_tk_acclat), .tk_bridge_o (w_tk_bridge),
    .l_tadv_p_o (w_l_tadv_p), .l_tfail_p_o (w_l_tfail_p),
    .l_evt_o (w_l_evt), .l_tfail_code_o (w_l_tfail_code),
    .pdu_cnt_o (pdu_cnt_o)
  );

  KL_lwsrp_ta_registrar ta_registrar (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (enable_i & lsid_en_i), .tick_1khz_i (tick_1khz_i),
    .leaveall_p_i (w_leaveall_p),
    .l_tadv_p_i (w_l_tadv_p), .l_tfail_p_i (w_l_tfail_p),
    .l_evt_i (w_l_evt), .l_tfail_code_i (w_l_tfail_code),
    .tk_vlan_i (w_tk_vlan), .tk_acclat_i (w_tk_acclat), .tk_bridge_i (w_tk_bridge),
    .ta_registered_o (ta_registered_o),
    .ta_failed_o (ta_failed_o), .ta_fail_code_o (ta_fail_code_o),
    .ta_vlan_o (ta_vlan_o), .ta_acclat_o (ta_acclat_o),
    .ta_fail_bridge_o (ta_fail_bridge_o)
  );

  KL_lwsrp_registrar registrar (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (enable_i), .tick_1khz_i (tick_1khz_i),
    .vid_i (vid_i),
    .leaveall_p_i (w_leaveall_p),
    .domain_p_i (w_domain_p),
    .domain_class_i (w_domain_class), .domain_prio_i (w_domain_prio),
    .domain_vid_i (w_domain_vid),     .domain_evt_i (w_domain_evt),
    .listener_p_i (w_listener_p),
    .listener_evt_i (w_listener_evt), .listener_decl_i (w_listener_decl),
    .tadv_p_i (w_tadv_p),
    .tfail_p_i (w_tfail_p), .tfail_code_i (w_tfail_code),
    .tk_bridge_i (w_tk_bridge),
    .listener_ready_o (listener_ready_o),
    .listener_reg_o (listener_reg_o), .listener_decl_o (listener_decl_o),
    .domain_ok_o (domain_ok_o),
    .tfail_valid_o (tfail_valid_o), .tfail_code_o (tfail_code_o),
    .tfail_bridge_o (tfail_bridge_o)
  );

endmodule

`default_nettype wire
