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
  parameter int          FIFO_DEPTH_BYTES_P = 2048,
  //! attribute contexts. 1 (default) = today's single talker+listener pair,
  //! wire-behavior byte-identical (the extra-context engine is instantiated
  //! but can never own a row, and the TX mux is a generate passthrough).
  //! N > 1 adds N-1 generic context-table rows (talker OR listener each),
  //! provisioned through the ctx_* request/grant port — the 2nd-listener /
  //! CRF-reservation gap (docs/MILAN_COMPLIANCE_GAPS.md §3).
  parameter int unsigned N_CTX_P        = 1
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
    output wire [11:0]  ta_vlan_o,         //! registered Talker-attr vlan
    output wire [31:0]  ta_acclat_o,       //! ...AccumulatedLatency
    output wire [63:0]  ta_fail_bridge_o,  //! ...TF bridge_id (listener)
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
    output wire [63:0]  tfail_bridge_o,    //! our-talker TF bridge_id
    output wire [15:0]  tx_count_o,
    output wire [15:0]  rx_pdus_o,
    output wire [7:0]   rx_drops_o,

    // ---- context table port (rows 1..N-1; row 0 = the legacy pair) --------
    //! request/grant provisioning (the future NxN CSR lane / the datapath
    //! ACMP side): hold ctx_req_i until the one-cycle ctx_gnt_o; a write
    //! (ctx_we_i=1) applies the record at the grant, a read snapshots
    //! sid+status into ctx_rd_*. Unconnected (all-0) = inert.
    input  wire         ctx_req_i,
    input  wire         ctx_we_i,
    input  wire [3:0]   ctx_idx_i,
    input  wire         ctx_valid_i,
    input  wire         ctx_dir_i,         //! 0 = talker, 1 = listener
    input  wire [63:0]  ctx_sid_i,
    input  wire [47:0]  ctx_dmac_i,
    input  wire [7:0]   ctx_prio_rank_i,
    input  wire [15:0]  ctx_max_frame_i,
    input  wire [15:0]  ctx_interval_i,
    input  wire [31:0]  ctx_latency_i,
    output wire         ctx_gnt_o,
    output wire [63:0]  ctx_rd_sid_o,
    output wire [15:0]  ctx_rd_stat_o,     //! {valid,dir,declared,reg,ready,
                                           //!  failed,decl[1:0],code[7:0]}
    //! live per-context status vectors, bit 0 = legacy row
    output wire [15:0]  ctx_reg_o,
    output wire [15:0]  ctx_ready_o,
    output wire [15:0]  ctx_failed_o,
    output wire [15:0]  ctx_tx_count_o     //! extra-context MRPDUs sent
);

  //! extra context-table rows; 1 inert lane when N_CTX_P = 1
  localparam int unsigned EXT_LANES_C = (N_CTX_P > 1) ? N_CTX_P - 1 : 1;

  wire tick_1khz_w, join_tick_w, leaveall_tick_w, rx_leaveall_w;

  KL_lwsrp_timers #(.CLK_FREQ_HZ_P(CLK_FREQ_HZ_P)) timers (
    .clk_i (clk_i), .rst_n (rst_n),
    .tick_1khz_o (tick_1khz_w),
    .join_tick_o (join_tick_w),
    .leaveall_tick_o (leaveall_tick_w)
  );

  // ---- context table + shared registrar + shared serializer --------------
  wire [EXT_LANES_C*64-1:0] lane_sid_w, row_sid_w;
  wire [EXT_LANES_C-1:0]    lane_en_w;
  wire [EXT_LANES_C-1:0]    e_lstn_p_w, e_tadv_p_w, e_tfail_p_w;
  wire [EXT_LANES_C*3-1:0]  e_evt_w;
  wire [EXT_LANES_C*2-1:0]  e_par_w;
  wire [7:0]                e_tfail_code_w;
  wire [EXT_LANES_C-1:0]    row_valid_w, row_dir_w, row_fresh_w, row_lv_w;
  wire [EXT_LANES_C-1:0]    row_ready_w, ctxtx_fresh_w, ctxtx_lv_w;
  wire                      ctx_tx_go_w, ctx_tx_done_w, ctx_fastjoin_w;
  wire [3:0]                rec_addr_w;
  wire [119:0]              rec_data_w;
  wire [63:0]               ctxtx_tdata_w;
  wire [7:0]                ctxtx_tkeep_w;
  wire                      ctxtx_tvalid_w, ctxtx_tlast_w, ctxtx_tready_w;
  wire [63:0]               tx0_tdata_w;
  wire [7:0]                tx0_tkeep_w;
  wire                      tx0_tvalid_w, tx0_tlast_w, tx0_tready_w;

  KL_lwsrp_ctx #(
    .N_CTX_P     (N_CTX_P),
    .EXT_LANES_P (EXT_LANES_C)
  ) ctx (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (enable_i), .tick_1khz_i (tick_1khz_w),
    .join_tick_i (join_tick_w), .leaveall_tick_i (leaveall_tick_w),
    .rx_leaveall_i (rx_leaveall_w),
    .ctx_req_i (ctx_req_i), .ctx_we_i (ctx_we_i), .ctx_idx_i (ctx_idx_i),
    .ctx_valid_i (ctx_valid_i), .ctx_dir_i (ctx_dir_i),
    .ctx_sid_i (ctx_sid_i), .ctx_dmac_i (ctx_dmac_i),
    .ctx_prio_rank_i (ctx_prio_rank_i),
    .ctx_max_frame_i (ctx_max_frame_i), .ctx_interval_i (ctx_interval_i),
    .ctx_latency_i (ctx_latency_i),
    .ctx_gnt_o (ctx_gnt_o),
    .ctx_rd_sid_o (ctx_rd_sid_o), .ctx_rd_stat_o (ctx_rd_stat_o),
    .leg_valid_i (enable_i & talker_en_i),
    .leg_declared_i (talker_declared_o),
    .leg_reg_i (listener_reg_o), .leg_ready_i (listener_ready_o),
    .leg_failed_i (tfail_valid_o), .leg_decl_i (listener_decl_o),
    .leg_code_i (tfail_code_o),
    .leg_sid_i ({station_mac_i, unique_id_i}),
    .lane_sid_o (lane_sid_w), .lane_en_o (lane_en_w),
    .lane_lstn_p_i (e_lstn_p_w), .lane_tadv_p_i (e_tadv_p_w),
    .lane_tfail_p_i (e_tfail_p_w),
    .lane_evt_i (e_evt_w), .lane_par_i (e_par_w),
    .lane_tfail_code_i (e_tfail_code_w),
    .row_valid_o (row_valid_w), .row_dir_o (row_dir_w),
    .row_fresh_o (row_fresh_w), .row_lv_o (row_lv_w),
    .row_ready_o (row_ready_w), .row_sid_o (row_sid_w),
    .tx_go_o (ctx_tx_go_w), .tx_done_i (ctx_tx_done_w),
    .tx_fresh_i (ctxtx_fresh_w), .tx_lv_i (ctxtx_lv_w),
    .rec_addr_i (rec_addr_w), .rec_data_o (rec_data_w),
    .fastjoin_p_o (ctx_fastjoin_w),
    .ctx_reg_o (ctx_reg_o), .ctx_ready_o (ctx_ready_o),
    .ctx_failed_o (ctx_failed_o)
  );

  KL_lwsrp_ctx_tx #(.EXT_LANES_P(EXT_LANES_C)) ctx_tx (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (enable_i),
    .station_mac_i (station_mac_i), .vid_i (vid_i),
    .row_valid_i (row_valid_w), .row_dir_i (row_dir_w),
    .row_fresh_i (row_fresh_w), .row_lv_i (row_lv_w),
    .row_ready_i (row_ready_w), .row_sid_i (row_sid_w),
    .tx_go_i (ctx_tx_go_w), .tx_done_o (ctx_tx_done_w),
    .tx_fresh_o (ctxtx_fresh_w), .tx_lv_o (ctxtx_lv_w),
    .rec_addr_o (rec_addr_w), .rec_data_i (rec_data_w),
    .m_axis_tdata (ctxtx_tdata_w), .m_axis_tkeep (ctxtx_tkeep_w),
    .m_axis_tvalid (ctxtx_tvalid_w), .m_axis_tlast (ctxtx_tlast_w),
    .m_axis_tready (ctxtx_tready_w),
    .tx_count_o (ctx_tx_count_o)
  );

  KL_lwsrp_tx tx (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (enable_i), .talker_en_i (talker_en_i),
    .join_tick_i (join_tick_w), .leaveall_tick_i (leaveall_tick_w),
    .rx_leaveall_i (rx_leaveall_w),
    .ext_fastjoin_i (ctx_fastjoin_w),
    .lstn_declare_i (lstn_declare_i),
    .lstn_ready_i (ta_registered_o),   // Ready while the TA is registered
    .lstn_sid_i (lstn_sid_i),
    .station_mac_i (station_mac_i), .unique_id_i (unique_id_i),
    .dest_mac_i (dest_mac_i), .vid_i (vid_i),
    .max_frame_i (max_frame_i), .interval_frames_i (interval_frames_i),
    .latency_i (latency_i),
    .m_axis_tdata (tx0_tdata_w), .m_axis_tkeep (tx0_tkeep_w),
    .m_axis_tvalid(tx0_tvalid_w), .m_axis_tlast (tx0_tlast_w),
    .m_axis_tready(tx0_tready_w),
    .talker_declared_o (talker_declared_o),
    .lstn_declared_o (lstn_declared_o),
    .tx_count_o (tx_count_o)
  );

  // ---- TX frame mux: STRUCTURAL passthrough at N = 1 (the no-regression
  // ---- axiom); frame-atomic 2:1 with legacy priority otherwise -----------
  generate
    if (N_CTX_P > 1) begin : g_txmux
      reg sel_r, busy_r;
      always_ff @(posedge clk_i or negedge rst_n) begin : txmux_S
        if (!rst_n) begin
          sel_r <= 1'b0; busy_r <= 1'b0;
        end else if (busy_r) begin
          if (m_axis_tvalid && m_axis_tready && m_axis_tlast)
            busy_r <= 1'b0;
        end else if (tx0_tvalid_w) begin
          busy_r <= 1'b1; sel_r <= 1'b0;
        end else if (ctxtx_tvalid_w) begin
          busy_r <= 1'b1; sel_r <= 1'b1;
        end
      end
      assign m_axis_tdata  = sel_r ? ctxtx_tdata_w  : tx0_tdata_w;
      assign m_axis_tkeep  = (busy_r && (sel_r ? ctxtx_tvalid_w
                                              : tx0_tvalid_w))
                             ? (sel_r ? ctxtx_tkeep_w : tx0_tkeep_w) : 8'h00;
      assign m_axis_tvalid = busy_r && (sel_r ? ctxtx_tvalid_w
                                              : tx0_tvalid_w);
      assign m_axis_tlast  = busy_r && (sel_r ? ctxtx_tlast_w
                                              : tx0_tlast_w);
      assign tx0_tready_w   = busy_r && !sel_r && m_axis_tready;
      assign ctxtx_tready_w = busy_r &&  sel_r && m_axis_tready;
    end else begin : g_txpass
      assign m_axis_tdata   = tx0_tdata_w;
      assign m_axis_tkeep   = tx0_tkeep_w;
      assign m_axis_tvalid  = tx0_tvalid_w;
      assign m_axis_tlast   = tx0_tlast_w;
      assign tx0_tready_w   = m_axis_tready;
      assign ctxtx_tready_w = 1'b1;      // ctx_tx can never own a row here
    end
  endgenerate

  KL_lwsrp_rx #(
    .FIFO_DEPTH_BYTES_P (FIFO_DEPTH_BYTES_P),
    .EXT_LANES_P        (EXT_LANES_C)
  ) rx (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (enable_i), .tick_1khz_i (tick_1khz_w),
    .rx_tvalid_i (rx_tvalid_i), .rx_tdata_i (rx_tdata_i),
    .rx_tkeep_i (rx_tkeep_i),   .rx_tlast_i (rx_tlast_i),
    .station_mac_i (station_mac_i), .unique_id_i (unique_id_i),
    .vid_i (vid_i),
    .lsid_i (lstn_sid_i), .lsid_en_i (lstn_bound_i),
    .ta_registered_o (ta_registered_o),
    .ta_failed_o (ta_failed_o), .ta_fail_code_o (ta_fail_code_o),
    .ta_vlan_o (ta_vlan_o), .ta_acclat_o (ta_acclat_o),
    .ta_fail_bridge_o (ta_fail_bridge_o),
    .listener_ready_o (listener_ready_o),
    .listener_reg_o (listener_reg_o), .listener_decl_o (listener_decl_o),
    .domain_ok_o (domain_ok_o),
    .tfail_valid_o (tfail_valid_o), .tfail_code_o (tfail_code_o),
    .tfail_bridge_o (tfail_bridge_o),
    .rx_leaveall_p_o (rx_leaveall_w),
    .ext_sid_i (lane_sid_w), .ext_en_i (lane_en_w),
    .ext_lstn_p_o (e_lstn_p_w), .ext_tadv_p_o (e_tadv_p_w),
    .ext_tfail_p_o (e_tfail_p_w),
    .ext_evt_o (e_evt_w), .ext_par_o (e_par_w),
    .ext_tfail_code_o (e_tfail_code_w),
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
