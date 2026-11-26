// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Each queue beat is one complete frame or one immutable state snapshot.
// Both domains belong to the same session reset, released locally.
`default_nettype none
module KL_usbaudio_crossing #(
  parameter int unsigned WIDTH_P = 288, //! complete frame and epoch width
  parameter int unsigned DEPTH_P = 64 //! power-of-two frame capacity
)(
  input wire s_clk_i, //! producer clock
  input wire s_rst_n, //! locally synchronized session reset
  input wire [WIDTH_P-1:0] data_i, //! immutable complete payload
  input wire valid_i, //! payload available
  output wire ready_o, //! payload accepted at the producer edge
  input wire m_clk_i, //! consumer clock
  input wire m_rst_n, //! locally synchronized session reset
  output wire [WIDTH_P-1:0] data_o, //! complete payload
  output wire valid_o, //! payload available
  input wire ready_i, //! payload accepted at the consumer edge
  output wire [$clog2(DEPTH_P):0] level_o //! conservative consumer frame count
);
  axis_async_fifo #(
    .DEPTH(DEPTH_P), .DATA_WIDTH(WIDTH_P), .KEEP_ENABLE(0), .KEEP_WIDTH(1),
    .LAST_ENABLE(0), .ID_ENABLE(0), .DEST_ENABLE(0), .USER_ENABLE(0)
  ) frames (
    .s_clk(s_clk_i), .s_rst(!s_rst_n), .s_axis_tdata(data_i),
    .s_axis_tkeep(1'b1), .s_axis_tvalid(valid_i), .s_axis_tready(ready_o),
    .s_axis_tlast(1'b1), .s_axis_tid(8'd0), .s_axis_tdest(8'd0), .s_axis_tuser(1'b0),
    .m_clk(m_clk_i), .m_rst(!m_rst_n), .m_axis_tdata(data_o),
    .m_axis_tkeep(), .m_axis_tvalid(valid_o), .m_axis_tready(ready_i),
    .m_axis_tlast(), .m_axis_tid(), .m_axis_tdest(), .m_axis_tuser(),
    .s_pause_req(1'b0), .s_pause_ack(), .m_pause_req(1'b0), .m_pause_ack(),
    .s_status_depth(), .s_status_depth_commit(), .s_status_overflow(),
    .s_status_bad_frame(), .s_status_good_frame(), .m_status_depth(level_o),
    .m_status_depth_commit(), .m_status_overflow(), .m_status_bad_frame(),
    .m_status_good_frame()
  );
endmodule
`default_nettype wire
