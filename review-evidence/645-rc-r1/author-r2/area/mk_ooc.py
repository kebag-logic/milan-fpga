#!/usr/bin/env python3
"""Wrap milan_datapath's settle block (SRC_SETTLE_ERR_C .. g_settle_recentre) as an OOC top.

usage: mk_ooc.py <milan_datapath.sv> <lb_streams> <out.sv>
The block is copied verbatim, as tb/verilator/follow_ring/settle_control.py copies it.
Inputs are the names it reads; outputs are its two pulses. Shipping 50 MHz axis clock.
"""
import sys
from pathlib import Path

src, n, out = Path(sys.argv[1]).read_text(), int(sys.argv[2]), Path(sys.argv[3])
begin = src.index("  localparam int unsigned SRC_SETTLE_ERR_C")
end = src.index("  end : g_settle_recentre", begin) + len("  end : g_settle_recentre")
body = src[begin:end]
top = f"""`default_nettype none
module settle_ooc (
  input  wire        axis_clk,
  input  wire        axis_resetn,
  input  wire [15:0] media_clk_src_r,
  input  wire        follow_sel_r,
  input  wire        mga_engaged_w,
  input  wire        mcsrv_locked_w,
  input  wire signed [15:0] mga_err_w,
  input  wire        media_tick_p,
  input  wire        lb_tap_tvalid_w,
  input  wire        lb_tap_tlast_w,
  input  wire [3:0]  lb_tap_tuser_w,
  input  wire [{n}-1:0] strtbl_bind_rise_w,
  input  wire [{n}-1:0] strtbl_bind_fall_w,
  output logic       settle_recentre_p_r,
  output logic       src_recentre_p_r_o
);
  localparam int unsigned MILAN_CLK_FREQ_HZ = 50_000_000;
  localparam int unsigned MCSRV_WIN_LOG2_C  = 9;
  localparam int LB_STREAMS_C = {n};
{body}
  assign src_recentre_p_r_o = src_recentre_p_r;
endmodule
`default_nettype wire
"""
out.write_text(top)
