#!/usr/bin/env python3
"""Show what the fragment arm's bubble masks on the MII build, and whether a real refusal is what the check reads.
usage: bubble_probe.py <tree copy> <out dir> <verilator>"""
import subprocess, sys
from pathlib import Path
tree, out, verilator = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
out.mkdir(parents=True, exist_ok=True)
suite = tree / "tb/verilator/gptp_txts"
launch = tree / "hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv"
gen = suite / "generated/mac_tx_chain_mii.v"
keep = {p: p.read_text() for p in (launch, gen)}
PROBE = '''
  //! review probe, disposable tree only
  always @(posedge eth_clk_i) if (eth_rst_n) begin
    if (inf_r && !gmii_tvalid_i && (gap_r < 3)) $display("MASKED ready=%0d nidx=%0d delta=%0d gap=%0d t=%0t", gmii_tready_i, nidx_w, delta_r, gap_r, $time);
    if (frame_push_w && delta_r != TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P)) $display("REFUSED delta=%0d", delta_r);
  end
'''
END = "endmodule : KL_gptp_gmii_launch"
ANCHOR = "assign liteethphymiitx_converter_last = (liteethphymiitx_converter_mux == 1'd1);"
STUCK = ANCHOR + "\nalways @(posedge eth_tx_clk) if (!eth_tx_rst && !phy_sink_valid) liteethphymiitx_converter_mux <= 1'd1;"
def case(name, stuck, cut_refusal=False):
    text = keep[launch].replace(END, PROBE + END)
    if cut_refusal:
        # a defect the fragment check claims to catch: the record says whole whatever the distance
        old = "(delta_r != TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P))};"
        assert old in text
        text = text.replace(old, "1'b0};")
    launch.write_text(text)
    gen.write_text(keep[gen].replace(ANCHOR, STUCK) if stuck else keep[gen])
    done = subprocess.run(["make", "-s", "-o", "model", "run-mii", f"VERILATOR={verilator}"], cwd=suite, capture_output=True, text=True)
    (out / f"{name}.log").write_text(done.stdout + done.stderr)
    print(name, "rc", done.returncode)
try:
    case("shipped", False)
    case("stuck", True)
    case("refusal-bit-cut", False, cut_refusal=True)
finally:
    for p, text in keep.items():
        p.write_text(text)
