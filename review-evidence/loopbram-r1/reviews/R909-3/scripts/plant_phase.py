"""Reviewer probe: write a copy of milan_datapath.sv with one output stream held off
for exactly one traffic phase. Phase is counted by axis_resetn assertions: the first
boot is assertion 1, the boot-clip reset is assertion 2. Usage:
  plant_phase.py <head milan_datapath.sv> <out.sv> <edits_stream|-1> <clipped_stream|-1>
or, for the whole-run hold used by the parent campaign (R910-2's exact text):
  plant_phase.py <in> <out> whole <mask-hex>"""
import sys
src = open(sys.argv[1]).read()
if sys.argv[3] == "whole":
    old = ".stream_en_i (aaf_stream_en_w),"
    new = ".stream_en_i (aaf_stream_en_w & N_STREAMS'(8'h%s))," % sys.argv[4]
else:
    e, c = int(sys.argv[3]), int(sys.argv[4])
    old = "  assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;"
    hold = []
    if e >= 0: hold.append("(N_STREAMS'(probe_rst_n_r == 2'd1) << %d)" % e)
    if c >= 0: hold.append("(N_STREAMS'(probe_rst_n_r >= 2'd2) << %d)" % c)
    new = ("  logic probe_rst_prev_r = 1'b1;\n  logic [1:0] probe_rst_n_r = 2'd0;\n"
           "  always_ff @(posedge axis_clk) begin\n    probe_rst_prev_r <= axis_resetn;\n"
           "    if (!axis_resetn && probe_rst_prev_r && probe_rst_n_r != 2'd3) probe_rst_n_r <= probe_rst_n_r + 2'd1;\n"
           "  end\n"
           "  assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r & ~(" + " | ".join(hold) + ");")
assert src.count(old) == 1, ("anchor count", src.count(old))
open(sys.argv[2], "w").write(src.replace(old, new))
print("planted", sys.argv[3:], "->", sys.argv[2])
