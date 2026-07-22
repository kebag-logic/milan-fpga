/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : csr_win_live.sv  (TB-only wrapper, tb/verilator/csr)
//
//  Description : P11 indexed-window LIVE integration fixture: milan_csr
//                (N_LISTENERS_P=2, N_TALKERS_P=2) wired to the REAL context
//                engines the window drives today —
//                  * KL_lwsrp_top with N_CTX_P=3 (row 1 = listener idx 1,
//                    row 2 = talker idx 1 per the window row map) on the
//                    csr's srp_ctx master port: window CTRL/SID/DMAC
//                    commits provision live rows; 0x85C reads the live
//                    row status through the ctx grant path.
//                  * KL_acmp_lstn_ctx with the default 2-sink policy pair
//                    (ctx1 = bind record + explicit sid) on the acmp tbl
//                    port: a fast-connect CONNECT_RX bind is read back
//                    through the window SID/DMAC/STATE words.
//                The LCTX/TCTX boundary stays at the datapath ties
//                (rd_data=0, snap_ok=1). Never synthesized.
//---------------------------------------------------------------------------//

`default_nettype none

module csr_win_live #(
  parameter int unsigned CLK_FREQ_HZ_P = 10_000
)(
  input  wire        clk_i,
  input  wire        rst_n,

  // ---- AXI4-Lite (the harness BFM) ----
  input  wire [15:0] s_axi_awaddr,
  input  wire        s_axi_awvalid,
  output wire        s_axi_awready,
  input  wire [31:0] s_axi_wdata,
  input  wire [3:0]  s_axi_wstrb,
  input  wire        s_axi_wvalid,
  output wire        s_axi_wready,
  output wire [1:0]  s_axi_bresp,
  output wire        s_axi_bvalid,
  input  wire        s_axi_bready,
  input  wire [15:0] s_axi_araddr,
  input  wire        s_axi_arvalid,
  output wire        s_axi_arready,
  output wire [31:0] s_axi_rdata,
  output wire [1:0]  s_axi_rresp,
  output wire        s_axi_rvalid,
  input  wire        s_axi_rready,

  // ---- RX AXIS into both engines (ACMPDUs / MRPDUs) ----
  input  wire        rx_tvalid_i,
  input  wire [63:0] rx_tdata_i,
  input  wire [7:0]  rx_tkeep_i,
  input  wire        rx_tlast_i,

  // ---- observation ----
  output wire        acmp1_bound_o     //! ctx1 record bound (compat view)
);

  // ---- csr <-> lwSRP ctx provisioning port ----
  wire        srp_req_w, srp_we_w, srp_valid_w, srp_dir_w, srp_gnt_w;
  wire [3:0]  srp_idx_w;
  wire [63:0] srp_sid_w, srp_rd_sid_w;
  wire [47:0] srp_dmac_w;
  wire [7:0]  srp_prio_w;
  wire [15:0] srp_maxf_w, srp_intv_w, srp_rd_stat_w;
  wire [31:0] srp_lat_w;

  // ---- csr <-> ACMP tbl port ----
  wire        tbl_req_w, tbl_gnt_w;
  wire [3:0]  tbl_idx_w;
  acmp_pkg::acmp_lstn_ctx_t tbl_ctx_w;
  wire [316:0] tbl_ctx_flat_w = tbl_ctx_w;

  // ---- lwSRP engine control/status (window SRP idx0 = 0x694 alias) ----
  wire        lwsrp_en_w, lwsrp_talker_en_w;
  wire [11:0] lwsrp_vid_w;
  wire [47:0] lwsrp_dmac_w;
  wire [15:0] lwsrp_maxf_w, lwsrp_intv_w;
  wire [31:0] lwsrp_lat_w;
  wire        slope_en_w, over_limit_w, res_active_w;
  wire [2:0]  stream_gate_w;          //! per-stream (P12 follow-up); the
                                      //! flat status word packs bit 0
  wire        domain_ok_w, talker_declared_w, listener_ready_w, listener_reg_w;
  wire        tfail_valid_w;
  wire [1:0]  listener_decl_w;
  wire [7:0]  tfail_code_w, rx_drops_w;

  milan_csr #(
    .N_LISTENERS_P (2),
    .N_TALKERS_P   (2)
  ) csr (
    .aclk    (clk_i),
    .aresetn (rst_n),
    .s_axi_awaddr (s_axi_awaddr), .s_axi_awvalid (s_axi_awvalid),
    .s_axi_awready (s_axi_awready),
    .s_axi_wdata (s_axi_wdata), .s_axi_wstrb (s_axi_wstrb),
    .s_axi_wvalid (s_axi_wvalid), .s_axi_wready (s_axi_wready),
    .s_axi_bresp (s_axi_bresp), .s_axi_bvalid (s_axi_bvalid),
    .s_axi_bready (s_axi_bready),
    .s_axi_araddr (s_axi_araddr), .s_axi_arvalid (s_axi_arvalid),
    .s_axi_arready (s_axi_arready),
    .s_axi_rdata (s_axi_rdata), .s_axi_rresp (s_axi_rresp),
    .s_axi_rvalid (s_axi_rvalid), .s_axi_rready (s_axi_rready),
    // lwSRP legacy group (row-0 identity + the shared TSpec source)
    .o_lwsrp_enable (lwsrp_en_w), .o_lwsrp_talker_en (lwsrp_talker_en_w),
    .o_lwsrp_vid (lwsrp_vid_w), .o_lwsrp_dest_mac (lwsrp_dmac_w),
    .o_lwsrp_max_frame (lwsrp_maxf_w), .o_lwsrp_interval (lwsrp_intv_w),
    .o_lwsrp_latency (lwsrp_lat_w),
    .i_lwsrp_status ({rx_drops_w, tfail_code_w, 5'd0, tfail_valid_w,
                      slope_en_w, stream_gate_w[0], over_limit_w, res_active_w,
                      domain_ok_w, talker_declared_w, listener_ready_w,
                      listener_reg_w, listener_decl_w}),
    // window: LCTX/TCTX at the no-engine ties (P12 contract: rd_valid/
    // wr_rdy tied 1 = P11 fixed timing, words read 0), live SRP/ACMP engines
    .i_lctx_rd_data (32'h0), .i_lctx_rd_valid (1'b1), .i_lctx_snap_ok (1'b1),
    .i_lctx_wr_rdy (1'b1),
    .i_tctx_rd_data (32'h0), .i_tctx_rd_valid (1'b1), .i_tctx_snap_ok (1'b1),
    .i_tctx_wr_rdy (1'b1),
    .o_acmp_tbl_req (tbl_req_w), .o_acmp_tbl_idx (tbl_idx_w),
    .i_acmp_tbl_gnt (tbl_gnt_w), .i_acmp_tbl_ctx (tbl_ctx_flat_w),
    .o_srp_ctx_req (srp_req_w), .o_srp_ctx_we (srp_we_w),
    .o_srp_ctx_idx (srp_idx_w), .o_srp_ctx_valid (srp_valid_w),
    .o_srp_ctx_dir (srp_dir_w), .o_srp_ctx_sid (srp_sid_w),
    .o_srp_ctx_dmac (srp_dmac_w), .o_srp_ctx_prio_rank (srp_prio_w),
    .o_srp_ctx_max_frame (srp_maxf_w), .o_srp_ctx_interval (srp_intv_w),
    .o_srp_ctx_latency (srp_lat_w),
    .i_srp_ctx_gnt (srp_gnt_w), .i_srp_ctx_rd_sid (srp_rd_sid_w),
    .i_srp_ctx_rd_stat (srp_rd_stat_w)
    // every other i_* input is intentionally unconnected (reads as 0):
    // this fixture proves the window's live-engine paths only
  );

  // ---- live lwSRP engine: window rows 1 (listener) / 2 (talker) ----
  KL_lwsrp_top #(
    .CLK_FREQ_HZ_P (CLK_FREQ_HZ_P),
    .N_CTX_P       (3)
  ) lwsrp (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (lwsrp_en_w),
    .talker_en_i (lwsrp_talker_en_w),
    .is_1g_i (1'b1),
    .lstn_bound_i (1'b0), .lstn_declare_i (1'b0), .lstn_sid_i (64'h0),
    .ta_registered_o (), .ta_failed_o (), .ta_fail_code_o (),
    .ta_vlan_o (), .ta_acclat_o (), .ta_fail_bridge_o (),
    .tfail_bridge_o (), .lstn_declared_o (),
    .station_mac_i (48'h02_00_00_00_00_03),
    .unique_id_i (16'd0),
    .dest_mac_i (lwsrp_dmac_w),
    .vid_i (lwsrp_vid_w),
    .max_frame_i (lwsrp_maxf_w),
    .interval_frames_i (lwsrp_intv_w),
    .latency_i (lwsrp_lat_w),
    .rx_tvalid_i (rx_tvalid_i), .rx_tdata_i (rx_tdata_i),
    .rx_tkeep_i (rx_tkeep_i), .rx_tlast_i (rx_tlast_i),
    .m_axis_tdata (), .m_axis_tkeep (), .m_axis_tvalid (),
    .m_axis_tlast (), .m_axis_tready (1'b1),
    .stream_gate_o (stream_gate_w),
    .slope_en_o (slope_en_w), .idle_slope_o (),
    .res_active_o (res_active_w),
    .listener_ready_o (listener_ready_w),
    .talker_declared_o (talker_declared_w),
    .listener_reg_o (listener_reg_w), .listener_decl_o (listener_decl_w),
    .domain_ok_o (domain_ok_w), .over_limit_o (over_limit_w),
    .tfail_valid_o (tfail_valid_w), .tfail_code_o (tfail_code_w),
    .tx_count_o (), .rx_pdus_o (), .rx_drops_o (rx_drops_w),
    .ctx_req_i (srp_req_w), .ctx_we_i (srp_we_w),
    .ctx_idx_i (srp_idx_w), .ctx_valid_i (srp_valid_w),
    .ctx_dir_i (srp_dir_w), .ctx_sid_i (srp_sid_w),
    .ctx_dmac_i (srp_dmac_w), .ctx_prio_rank_i (srp_prio_w),
    .ctx_max_frame_i (srp_maxf_w), .ctx_interval_i (srp_intv_w),
    .ctx_latency_i (srp_lat_w),
    .ctx_gnt_o (srp_gnt_w), .ctx_rd_sid_o (srp_rd_sid_w),
    .ctx_rd_stat_o (srp_rd_stat_w),
    .ctx_reg_o (), .ctx_ready_o (), .ctx_failed_o (), .ctx_tx_count_o ()
  );

  // ---- live ACMP listener context engine (default 2-sink policy pair) ----
  KL_acmp_lstn_ctx #(
    .CLK_FREQ_HZ_P (CLK_FREQ_HZ_P),
    .N_SINKS_P     (2)
  ) acmp (
    .clk_i (clk_i), .rst_n (rst_n),
    .enable_i (1'b1),
    .station_mac_i (48'h02_00_00_00_00_03),
    .entity_id_i (64'h020000FFFE000003),
    .tick_1s_i (1'b0),
    .ta_registered_i (2'b00), .ta_failed_i (2'b00),
    .lstn_declare_o (), .stream_active_o (),
    .rx_tvalid_i (rx_tvalid_i), .rx_tdata_i (rx_tdata_i),
    .rx_tkeep_i (rx_tkeep_i), .rx_tlast_i (rx_tlast_i),
    .m_axis_tdata (), .m_axis_tkeep (), .m_axis_tvalid (),
    .m_axis_tlast (), .m_axis_tready (1'b1),
    .view0_state_o (), .view0_talker_o (), .view0_tuid_o (),
    .view0_sid_o (), .view0_vlan_o (), .view0_dmac_o (),
    .view0_status_o (), .view0_probing_o (), .view0_tk_avail_o (),
    .view1_bound_o (acmp1_bound_o), .view1_sid_o (), .view1_dmac_o (),
    .cmd_count_o (), .probe_count_o (), .tx_wedge_cnt_o (), .dbg_o (),
    .tbl_req_i (tbl_req_w),
    .tbl_idx_i (tbl_idx_w[0]),
    .tbl_gnt_o (tbl_gnt_w),
    .tbl_ctx_o (tbl_ctx_w)
  );

endmodule

`default_nettype wire
