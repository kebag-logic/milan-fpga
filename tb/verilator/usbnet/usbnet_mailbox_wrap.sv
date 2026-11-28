// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// The local merger drives the production mailbox receiver at the system clock.
`default_nettype none
module usbnet_mailbox_wrap (
  input wire clk_i, rst_ni,
  input wire s_active_i, s_valid_i, s_last_i,
  input wire [63:0] s_data_i,
  input wire [7:0] s_keep_i,
  input wire net_valid_i, net_last_i,
  input wire [7:0] net_data_i,
  output wire net_ready_o,
  output wire m_valid_o, m_ready_o, m_last_o,
  output wire [7:0] m_data_o,
  output wire [79:0] dropped_o,
  output wire [79:0] rate_dropped_o,
  output wire [79:0] passed_o
);
  KL_usbnet_local_rx local_rx (
    .clk_i, .rst_ni, .station_mac_i(48'h024b4c000101),
    .s_active_i, .s_valid_i, .s_last_i, .s_data_i, .s_keep_i,
    .net_valid_i, .net_last_i, .net_data_i, .net_ready_o,
    .m_valid_o, .m_ready_i(m_ready_o), .m_last_o, .m_data_o,
    .copied_o(), .full_o()
  );
  KL_mbx_rx mailbox (
    .clk_i, .rst_n(rst_ni), .ms_tick_p_i(1'b0), .now_ms_i(32'd0),
    .own_eid_i(64'd0), .own_mac_i(48'h024b4c000101),
    .bnd_req_i(1'b0), .bnd_we_i(1'b0), .bnd_if_i(1'b0),
    .bnd_entry_i(5'd0), .bnd_reg_i(2'd0), .bnd_wdata_i(32'd0),
    .bnd_eid_o(), .bnd_eid_vld_o(), .bnd_en_o(),
    .open_i(5'b11111), .maap_base_i(48'h91e0f000fe00), .maap_count_i(16'd32),
    .rx_valid_i(m_valid_o), .rx_ready_o(m_ready_o), .rx_data_i(m_data_o),
    .rx_last_i(m_last_o), .rx_if_i(1'b0),
    .wr_en_o(), .wr_ch_o(), .wr_addr_o(), .wr_data_o(),
    .rx_tail_words_i(80'd0), .rx_head_words_o(),
    .rx_drop_cnt_o(dropped_o), .rate_drop_cnt_o(rate_dropped_o), .rx_pass_cnt_o(passed_o),
    .mismatch_cnt_o(), .err_p_o()
  );
endmodule
`default_nettype wire
