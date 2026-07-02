/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Wrapper instantiating cdc_pulse + cdc_handshake with shared src/dest clocks so
 * one Verilator harness exercises both open CDC primitives (Track 1.4).
 */
`default_nettype none

module cdc_tb_top #(
  parameter int WIDTH = 64
)(
  input  wire             src_clk,
  input  wire             src_rst_n,
  input  wire             dest_clk,
  input  wire             dest_rst_n,
  // pulse CDC
  input  wire             p_src_pulse,
  output wire             p_dest_pulse,
  // value CDC (handshake)
  input  wire [WIDTH-1:0] h_src_in,
  input  wire             h_src_send,
  output wire             h_src_rcv,
  output wire [WIDTH-1:0] h_dest_out,
  output wire             h_dest_req
);

  cdc_pulse #(.DEST_SYNC_FF(2)) u_pulse (
    .src_clk(src_clk), .src_rst_n(src_rst_n), .src_pulse(p_src_pulse),
    .dest_clk(dest_clk), .dest_rst_n(dest_rst_n), .dest_pulse(p_dest_pulse)
  );

  cdc_handshake #(.WIDTH(WIDTH), .DEST_SYNC_FF(2), .SRC_SYNC_FF(2)) u_hs (
    .src_clk(src_clk), .src_rst_n(src_rst_n),
    .src_in(h_src_in), .src_send(h_src_send), .src_rcv(h_src_rcv),
    .dest_clk(dest_clk), .dest_rst_n(dest_rst_n),
    .dest_out(h_dest_out), .dest_req(h_dest_req)
  );

endmodule

`default_nettype wire
