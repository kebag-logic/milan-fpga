"""Prepare the exact OOC comparison in an external scratch directory.
Run from the repository root: python3 AREA-SOURCES.py /path/to/scratch
The accompanying ooc.tcl selects one configuration through ONLY.
"""
from pathlib import Path
import shutil
import subprocess
import sys

work = Path(sys.argv[1]).resolve()
work.mkdir(parents=True, exist_ok=True)
root = Path.cwd()
base = "28f9666feab2b2ba287643c63ed3a16b1e0bb863"
head = "4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f"
ports = """#(parameter int unsigned MILAN_CLK_FREQ_HZ = 50_000_000) (
  input wire axis_clk, input wire axis_resetn,
  input wire [15:0] media_clk_src_r, input wire mga_engaged_w,
  input wire signed [15:0] mga_err_w, input wire follow_sel_r,
  input wire media_tick_p, input wire mcsrv_locked_w,
  input wire media_rebase_p_w,
  output wire render_recentre_p_o, output wire lb_recentre_p_o);
"""
for tag, revision, wrapper in [("base", base, "base"), ("head", head, "new")]:
    def source(relative):
        return subprocess.check_output(["git", "show", revision + ":" + relative], text=True)
    (work / ("cmc_" + tag + ".sv")).write_text(source("hdl/ieee1722/aaf/KL_chan_map_capture.sv"))
    dp = source("hdl/milan/milan_datapath.sv")
    start = dp.index("  localparam int unsigned SRC_SETTLE_ERR_C")
    marker = "  end : g_src_recentre" if tag == "base" else "  end : g_settle_recentre"
    end = dp.index(marker, start) + len(marker)
    piece = dp[start:end] + "\n"
    if tag == "head":
        win = next(line for line in dp.splitlines() if "localparam int unsigned MCSRV_WIN_LOG2_C" in line)
        piece = win + "\n" + piece
    (work / ("piece_" + wrapper + ".svh")).write_text(piece)
    text = "module settle_" + wrapper + " " + ports
    if tag == "head":
        text += "  logic settle_recentre_p_r;\n"
    text += '`include "piece_' + wrapper + '.svh"\n'
    extra = " | settle_recentre_p_r" if tag == "head" else ""
    text += "  assign render_recentre_p_o = media_rebase_p_w" + extra + " | src_recentre_p_r;\n"
    text += "  assign lb_recentre_p_o = " + ("settle_recentre_p_r" if tag == "head" else "1'b0") + ";\nendmodule\n"
    (work / ("settle_" + wrapper + ".sv")).write_text(text)
shutil.copy2(Path(__file__).with_name("ooc.tcl"), work / "ooc.tcl")
