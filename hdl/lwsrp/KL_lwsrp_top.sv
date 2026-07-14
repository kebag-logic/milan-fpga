/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_top.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : lwSRP engine top — the one instance milan_datapath takes
//                (docs/LWSRP_FPGA_ARCHITECTURE.md §3/§5):
//
//                  KL_lwsrp_timers   join/leaveall/1 kHz strobes
//                  KL_lwsrp_tx       always-declare applicant (MSRP + MVRP)
//                  KL_lwsrp_rx       tap -> FIFO -> walker -> registrar
//                  KL_lwsrp_bw_gate  reservation + slope + gate ordering
//
//                Integration contract:
//                  m_axis_*          -> the low-rate control TX merge
//                  rx_*              -> monitor tap on rx_axis_to_dma
//                  stream_gate_o     -> AAF admission (with the CSR bypass
//                                       resolved at the datapath level)
//                  slope_en/idle_slope -> CBS slope MUX for the class-A queue
//                  listener_ready_o  -> ACMP listener_observed (replaces the
//                                       manual A_ACMP_LOBS override)
//---------------------------------------------------------------------------//

`default_nettype none

module KL_lwsrp_top #(
  //! Datapath clock (AX7101 100 MHz, Arty 50 MHz) — MRP timer base.
  parameter int unsigned CLK_FREQ_HZ_P   = 100_000_000,
  parameter int          FIFO_DEPTH_BYTES_P = 2048
)(
    input  wire         clk_i,
    input  wire         rst_n,

    // ---- CSR control ------------------------------------------------------
    input  wire         enable_i,          //! LWSRP_CTRL[0]
    input  wire         talker_en_i,       //! LWSRP_CTRL[1]
    input  wire         is_1g_i,           //! port rate (MAC_CTRL is_1g)

    // ---- ACMP listener SM hooks (listener endpoint role) ------------------
    input  wire         lstn_bound_i,      //! binding valid (track the TA)
    input  wire         lstn_declare_i,    //! declare the Listener attribute
    input  wire [63:0]  lstn_sid_i,        //! bound stream_id
    output wire         ta_registered_o,   //! TalkerAdvertise registered (lsid)
    output wire         ta_failed_o,       //! TalkerFailed registered (lsid)
    output wire [7:0]   ta_fail_code_o,
    output wire         lstn_declared_o,   //! Listener attr on the wire

    // ---- identity + stream table row 0 (CSR) ------------------------------
    input  wire [47:0]  station_mac_i,     //! [47:40] = first wire byte
    input  wire [15:0]  unique_id_i,
    input  wire [47:0]  dest_mac_i,
    input  wire [11:0]  vid_i,
    input  wire [15:0]  max_frame_i,
    input  wire [15:0]  interval_frames_i,
    input  wire [31:0]  latency_i,

    // ---- RX monitor tap (little lane, inputs only) ------------------------
    input  wire         rx_tvalid_i,
    input  wire [63:0]  rx_tdata_i,
    input  wire [7:0]   rx_tkeep_i,
    input  wire         rx_tlast_i,

    // ---- AXIS master (little lane; -> low-rate control TX merge) ----------
    output logic [63:0] m_axis_tdata,
    output logic [7:0]  m_axis_tkeep,
    output logic        m_axis_tvalid,
    output logic        m_axis_tlast,
    input  wire         m_axis_tready,

    // ---- reservation outputs ----------------------------------------------
    output wire         stream_gate_o,     //! AAF admission
    output wire         slope_en_o,        //! CBS slope MUX select
    output wire [31:0]  idle_slope_o,      //! granted idleSlope, bps
    output wire         res_active_o,
    output wire         listener_ready_o,  //! -> ACMP listener_observed

    // ---- CSR status ---------------------------------------------------------
    output wire         talker_declared_o,
    output wire         listener_reg_o,
    output wire [1:0]   listener_decl_o,
    output wire         domain_ok_o,
    output wire         over_limit_o,
    output wire         tfail_valid_o,
    output wire [7:0]   tfail_code_o,
    output wire [15:0]  tx_count_o,
    output wire [15:0]  rx_pdus_o,
    output wire [7:0]   rx_drops_o
);

  wire tick_1khz_w, join_tick_w, leaveall_tick_w, rx_leaveall_w;

  KL_lwsrp_timers #(.CLK_FREQ_HZ_P(CLK_FREQ_HZ_P)) timers (
    .clk_i (clk_i), .rst_n (rst_n),
    .tick_1khz_o (tick_1khz_w),
    .join_tick_o (join_tick_w),
    .leaveall_tick_o (leaveall_tick_w)
  );

  KL_lwsrp_tx tx (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (enable_i), .talker_en_i (talker_en_i),
    .join_tick_i (join_tick_w), .leaveall_tick_i (leaveall_tick_w),
    .rx_leaveall_i (rx_leaveall_w),
    .lstn_declare_i (lstn_declare_i),
    .lstn_ready_i (ta_registered_o),   // Ready while the TA is registered
    .lstn_sid_i (lstn_sid_i),
    .station_mac_i (station_mac_i), .unique_id_i (unique_id_i),
    .dest_mac_i (dest_mac_i), .vid_i (vid_i),
    .max_frame_i (max_frame_i), .interval_frames_i (interval_frames_i),
    .latency_i (latency_i),
    .m_axis_tdata (m_axis_tdata), .m_axis_tkeep (m_axis_tkeep),
    .m_axis_tvalid(m_axis_tvalid), .m_axis_tlast (m_axis_tlast),
    .m_axis_tready(m_axis_tready),
    .talker_declared_o (talker_declared_o),
    .lstn_declared_o (lstn_declared_o),
    .tx_count_o (tx_count_o)
  );

  KL_lwsrp_rx #(.FIFO_DEPTH_BYTES_P(FIFO_DEPTH_BYTES_P)) rx (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (enable_i), .tick_1khz_i (tick_1khz_w),
    .rx_tvalid_i (rx_tvalid_i), .rx_tdata_i (rx_tdata_i),
    .rx_tkeep_i (rx_tkeep_i),   .rx_tlast_i (rx_tlast_i),
    .station_mac_i (station_mac_i), .unique_id_i (unique_id_i),
    .vid_i (vid_i),
    .lsid_i (lstn_sid_i), .lsid_en_i (lstn_bound_i),
    .ta_registered_o (ta_registered_o),
    .ta_failed_o (ta_failed_o), .ta_fail_code_o (ta_fail_code_o),
    .listener_ready_o (listener_ready_o),
    .listener_reg_o (listener_reg_o), .listener_decl_o (listener_decl_o),
    .domain_ok_o (domain_ok_o),
    .tfail_valid_o (tfail_valid_o), .tfail_code_o (tfail_code_o),
    .rx_leaveall_p_o (rx_leaveall_w),
    .rx_pdus_o (rx_pdus_o), .rx_drops_o (rx_drops_o),
    .pdu_cnt_o ()
  );

  KL_lwsrp_bw_gate bw_gate (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (enable_i),
    .talker_declared_i (talker_declared_o),
    .listener_ready_i (listener_ready_o),
    .domain_ok_i (domain_ok_o),
    .is_1g_i (is_1g_i),
    .max_frame_i (max_frame_i), .interval_frames_i (interval_frames_i),
    .stream_gate_o (stream_gate_o),
    .slope_en_o (slope_en_o), .idle_slope_o (idle_slope_o),
    .res_active_o (res_active_o),
    .over_limit_o (over_limit_o)
  );

endmodule

`default_nettype wire
