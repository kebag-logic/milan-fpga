#!/usr/bin/env python3
"""Instrument a private copy of gptp_tables_wrap.sv: report the first cycle
after reset in which the plane's transmit FIFO is NOT valid yet tx_tkeep_o
is non-zero, for the new FIFO and for the old-form reference FIFO.
Usage: python3 -I idle_keep_probe.py <copy>/tb/verilator/gptp_tables/gptp_tables_wrap.sv"""
import sys
from pathlib import Path
p = Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
anchor = "endmodule : gptp_tables_wrap"
probe = """
  logic idle_new_seen_r = 1'b0, idle_old_seen_r = 1'b0;
  always_ff @(posedge clk_i) begin : idle_keep_probe
    if (run_w && !u_bench.u_shadow.txf_out_valid_w && (tx_tkeep_o != 8'd0) && !idle_new_seen_r) begin
      idle_new_seen_r <= 1'b1;
      $display("IDLE_KEEP new: tvalid low, tx_tkeep_o=%b, tx_fifo count field=%0d", tx_tkeep_o, u_bench.u_shadow.txf_cnt_w);
    end
    if (run_w && !rt_valid_w && (rt_keep_w != 8'd0) && !idle_old_seen_r) begin
      idle_old_seen_r <= 1'b1;
      $display("IDLE_KEEP old-form reference: tvalid low, tkeep=%b", rt_keep_w);
    end
  end
"""
assert t.count(anchor) == 1
p.write_text(t.replace(anchor, probe + anchor, 1), encoding="utf-8")
