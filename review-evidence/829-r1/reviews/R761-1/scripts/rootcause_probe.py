#!/usr/bin/env python3
"""Print the observer's seam cycle by cycle for the first frame, in three builds:
MII with the fix cut, MII as shipped, GMII as shipped. Works on a disposable tree copy.
usage: rootcause_probe.py <tree copy> <out dir> <verilator>"""
import subprocess, sys
from pathlib import Path
tree, out, verilator = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
out.mkdir(parents=True, exist_ok=True)
suite = tree / "tb/verilator/gptp_txts"
rtl = tree / "hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv"
original = rtl.read_text()
PROBE = '''
  //! review probe, disposable tree only
  int unsigned rv_cyc = 0; bit rv_done = 0; int unsigned rv_recs = 0;
  longint unsigned rv_held = 0, rv_trans = 0;
  final $display("SEAM-TOTALS valid_not_ready=%0d valid_and_ready=%0d records=%0d", rv_held, rv_trans, rv_recs);
  always @(posedge eth_clk_i) if (eth_rst_n) begin
    if (gmii_tvalid_i && !gmii_tready_i) rv_held++;
    if (gmii_tvalid_i && gmii_tready_i) rv_trans++;
    if (frame_push_w || abort_push_w) begin
      rv_recs++;
      if (rv_recs <= 3) $display("RECORD n=%0d delta=%0d abort=%0d", rv_recs, delta_r, (delta_r != TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P)) | abort_push_w);
    end
    if (gmii_tvalid_i && !rv_done) begin
      $display("SEAM cyc=%0d d=%02x ready=%0d nidx=%0d inf=%0d chk=%0d cand=%0d mine=%0d ref=%0d delta=%0d", rv_cyc, gmii_tdata_i, gmii_tready_i, nidx_w, inf_r, chk_w, cand_r, mine_r, ref_r, delta_r);
      rv_cyc++;
      if (rv_cyc == 40) rv_done = 1;
    end
  end
'''
END = "endmodule : KL_gptp_gmii_launch"
def build(name, target, cut):
    text = original.replace(END, PROBE + END)
    if cut:
        assert "        if (gmii_tready_i) begin\n" in text
        text = text.replace("        if (gmii_tready_i) begin\n", "        if (1'b1) begin\n")
    rtl.write_text(text)
    done = subprocess.run(["make", "-s", target, f"VERILATOR={verilator}"], cwd=suite, capture_output=True, text=True)
    (out / f"{name}.log").write_text(done.stdout + done.stderr)
    (out / f"{name}.rc").write_text(f"{done.returncode}\n")
try:
    build("mii-fix-cut", "run-mii", True)
    build("mii-shipped", "run-mii", False)
    build("gmii-shipped", "run", False)
finally:
    rtl.write_text(original)
