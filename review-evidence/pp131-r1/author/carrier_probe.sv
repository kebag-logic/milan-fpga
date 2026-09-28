// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reproduce the two acknowledgement domains using unchanged production RTL.
`default_nettype none
module carrier_probe
  import pp_acmp_pkg::*;
(
  input wire clk_i,
  input wire rst_n,
  input wire go_i,
  input wire change_i,
  input wire csr_we_i,
  input wire [5:0] csr_addr_i,
  input wire [31:0] csr_data_i,
  input wire finish_memory_i,
  output wire restored_o,
  output wire producer_pending_o,
  output wire alarm_o,
  output wire backend_dirty_o,
  output wire backend_stale_o,
  output wire backend_backed_o,
  output wire port_done_o,
  output wire device_done_o,
  output wire device_write_o,
  output wire mem_write_o,
  output wire [31:0] mem_addr_o,
  output wire [63:0] mem_data_o,
  output wire [7:0] mem_strb_o,
  output wire mem_read_o,
  output wire [31:0] csr_rdata_o
);
  logic [ACMP_REC_W_C-1:0] record_w;
  always_comb begin : capture_record
    record_w = '0;
    record_w[11] = 1'b1;
    record_w[12] = 1'b1;
    record_w[32 +: 64] = 64'h1020304050607080;
    record_w[96 +: 16] = 16'h1234;
    record_w[128 +: 64] = 64'h8877665544332211;
  end

  wire m_req_w, m_we_w, m_wvalid_w, m_wready_w, m_rvalid_w;
  wire m_rready_w, m_busy_w, m_done_w, m_err_w, m_abort_w;
  wire [7:0] m_id_w, m_wdata_w, m_rdata_w;
  wire [1:0] m_cause_w;
  KL_acmp_nvm_shadow #(.N_SINKS_P(1), .DEB_TICKS_P(4)) u_producer (
    .clk_i(clk_i), .rst_n(rst_n), .tick_i(1'b1), .restore_go_i(go_i),
    .restore_busy_o(), .restore_done_o(restored_o), .restore_fail_o(),
    .restore_blank_o(), .restore_cause_o(), .alarm_o(alarm_o),
    .cap_wr_i(change_i), .cap_sink_i(1'b0), .cap_rec_i(record_w),
    .pre_valid_o(), .pre_sink_o(), .pre_talker_eid_o(), .pre_talker_uid_o(),
    .pre_ctlr_eid_o(), .pre_sw_o(), .pre_started_o(), .pre_ready_i(1'b1),
    .nvm_req_o(m_req_w), .nvm_we_o(m_we_w), .nvm_record_id_o(m_id_w),
    .nvm_wvalid_o(m_wvalid_w), .nvm_wready_i(m_wready_w), .nvm_wdata_o(m_wdata_w),
    .nvm_rvalid_i(m_rvalid_w), .nvm_rready_o(m_rready_w), .nvm_rdata_i(m_rdata_w),
    .nvm_busy_i(m_busy_w), .nvm_done_i(m_done_w), .nvm_err_i(m_err_w),
    .nvm_err_cause_i(m_cause_w), .nvm_abort_o(m_abort_w),
    .dbg_dirty_o(producer_pending_o), .dbg_valid_o(), .dbg_touched_o()
  );

  wire p_req_w, p_we_w, p_wvalid_w, p_wready_w, p_rvalid_w;
  wire p_rready_w, p_busy_w, p_done_w, p_err_w;
  wire [7:0] p_id_w, p_wdata_w, p_rdata_w;
  wire [1:0] p_cause_w;
  KL_pp_nvm_mgr_arb u_arb (
    .clk_i(clk_i), .rst_n(rst_n),
    .m0_req_i(m_req_w), .m0_we_i(m_we_w), .m0_rid_i(m_id_w),
    .m0_wvalid_i(m_wvalid_w), .m0_wdata_i(m_wdata_w), .m0_rready_i(m_rready_w),
    .m0_wready_o(m_wready_w), .m0_rvalid_o(m_rvalid_w), .m0_rdata_o(m_rdata_w),
    .m0_busy_o(m_busy_w), .m0_done_o(m_done_w), .m0_err_o(m_err_w),
    .m0_err_cause_o(m_cause_w), .m0_abort_i(m_abort_w),
    .m1_req_i(1'b0), .m1_we_i(1'b0), .m1_rid_i(8'd0),
    .m1_wvalid_i(1'b0), .m1_wdata_i(8'd0), .m1_rready_i(1'b0),
    .m1_wready_o(), .m1_rvalid_o(), .m1_rdata_o(), .m1_gnt_o(),
    .m1_done_o(), .m1_err_o(), .m1_err_cause_o(), .m1_abort_i(1'b0),
    .p_req_o(p_req_w), .p_we_o(p_we_w), .p_rid_o(p_id_w),
    .p_wvalid_o(p_wvalid_w), .p_wdata_o(p_wdata_w), .p_rready_o(p_rready_w),
    .p_wready_i(p_wready_w), .p_rvalid_i(p_rvalid_w), .p_rdata_i(p_rdata_w),
    .p_busy_i(p_busy_w), .p_done_i(p_done_w), .p_err_i(p_err_w),
    .p_err_cause_i(p_cause_w), .dbg_drain_o()
  );

  wire d_req_w, d_gnt_w, d_wvalid_w, d_wready_w, d_rvalid_w;
  wire d_rready_w, d_busy_w, d_done_w, d_err_w;
  wire [1:0] d_op_w;
  wire [7:0] d_region_w, d_wdata_w, d_rdata_w;
  wire [15:0] d_offset_w, d_len_w;
  KL_pp_nvm_port u_port (
    .clk_i(clk_i), .rst_n(rst_n),
    .nvm_req_i(p_req_w), .nvm_we_i(p_we_w), .nvm_record_id_i(p_id_w),
    .nvm_wvalid_i(p_wvalid_w), .nvm_wdata_i(p_wdata_w), .nvm_rready_i(p_rready_w),
    .nvm_wready_o(p_wready_w), .nvm_rvalid_o(p_rvalid_w), .nvm_rdata_o(p_rdata_w),
    .nvm_busy_o(p_busy_w), .nvm_done_o(p_done_w), .nvm_err_o(p_err_w),
    .nvm_err_cause_o(p_cause_w),
    .dev_req_o(d_req_w), .dev_gnt_i(d_gnt_w), .dev_op_o(d_op_w),
    .dev_region_o(d_region_w), .dev_offset_o(d_offset_w), .dev_len_o(d_len_w),
    .dev_wvalid_o(d_wvalid_w), .dev_wready_i(d_wready_w), .dev_wdata_o(d_wdata_w),
    .dev_rvalid_i(d_rvalid_w), .dev_rdata_i(d_rdata_w), .dev_rready_o(d_rready_w),
    .dev_busy_i(d_busy_w), .dev_done_i(d_done_w), .dev_err_i(d_err_w)
  );

  KL_nvm_backend #(
    .CLK_HZ_P(10000), .N_STREAM_IN_P(1), .N_STREAM_OUT_P(1),
    .N_SPORT_IN_P(1), .N_SPORT_OUT_P(1), .N_NAME_P(1)
  ) u_backend (
    .clk_i(clk_i), .rst_n(rst_n),
    .dev_req_i(d_req_w), .dev_gnt_o(d_gnt_w), .dev_op_i(d_op_w),
    .dev_region_i(d_region_w), .dev_offset_i(d_offset_w), .dev_len_i(d_len_w),
    .dev_wvalid_i(d_wvalid_w), .dev_wready_o(d_wready_w), .dev_wdata_i(d_wdata_w),
    .dev_rvalid_o(d_rvalid_w), .dev_rdata_o(d_rdata_w), .dev_rready_i(d_rready_w),
    .dev_busy_o(d_busy_w), .dev_done_o(d_done_w), .dev_err_o(d_err_w),
    .mem_req_valid_o(mem_read_o), .mem_req_ready_i(1'b0),
    .mem_req_addr_o(), .mem_req_beats_o(), .mem_rsp_valid_i(1'b0),
    .mem_rsp_ready_o(), .mem_rsp_data_i(64'd0), .mem_rsp_last_i(1'b0),
    .mem_rsp_err_i(1'b0), .mem_wr_valid_o(mem_write_o),
    .mem_wr_ready_i(1'b1), .mem_wr_addr_o(mem_addr_o), .mem_wr_data_o(mem_data_o),
    .mem_wr_strb_o(mem_strb_o), .mem_wr_done_i(mem_write_o && finish_memory_i),
    .mem_wr_err_i(1'b0), .csr_sel_i(1'b1), .csr_we_i(csr_we_i),
    .csr_addr_i(csr_addr_i), .csr_wdata_i(csr_data_i), .csr_rdata_o(csr_rdata_o),
    .pend_i(producer_pending_o), .alarm_i(alarm_o),
    .nvm_backed_o(backend_backed_o), .nvm_dirty_o(backend_dirty_o),
    .nvm_stale_o(backend_stale_o), .nvm_verdict_o(), .img_valid_o(),
    .nvm_pend_o(), .nvm_unres_o()
  );
  assign port_done_o = m_done_w;
  assign device_done_o = d_done_w;
  assign device_write_o = d_req_w && d_gnt_w && (d_op_w == 2'd1);
endmodule
`default_nettype wire
