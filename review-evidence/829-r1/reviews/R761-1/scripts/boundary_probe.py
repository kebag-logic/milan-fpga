#!/usr/bin/env python3
"""Disposable-tree probes of the MII shape: the guard's boundary, and frames that start on a stuck nibble phase.
usage: boundary_probe.py <tree copy> <out dir> <verilator>"""
import subprocess, sys
from pathlib import Path
tree, out, verilator = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
out.mkdir(parents=True, exist_ok=True)
suite = tree / "tb/verilator/gptp_txts"
txret = tree / "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
launch = tree / "hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv"
sim = suite / "sim_main.cpp"
keep = {p: p.read_text() for p in (txret, launch, sim)}
GUARD = "(RECON_NEED_CYC_C > RECON_GUARD_CYC_P) ? RECON_NEED_CYC_C : RECON_GUARD_CYC_P;"
ARM = "pad_cur_.gptp && pad_idx_ == 22"
assert GUARD in keep[txret] and ARM in keep[sim]
PHASE = '''
  //! review probe, disposable tree only
  bit rv_prev = 0; longint unsigned rv_stuck = 0, rv_starts = 0, rv_ok = 0, rv_bad = 0;
  final $display("PHASE-TOTALS frame_starts=%0d started_on_ready=%0d records_ok=%0d records_bad=%0d", rv_starts, rv_stuck, rv_ok, rv_bad);
  always @(posedge eth_clk_i) if (eth_rst_n) begin
    rv_prev <= gmii_tvalid_i;
    if (gmii_tvalid_i && !rv_prev) begin rv_starts++; if (gmii_tready_i) rv_stuck++; end
    if (frame_push_w) begin if (delta_r == TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P)) rv_ok++; else rv_bad++; end
  end
'''
END = "endmodule : KL_gptp_gmii_launch"
MAKE_ARGS = []
def case(name, guard=None, arm=None, phase=False):
    for p, text in keep.items():
        p.write_text(text)
    if guard is not None:
        txret.write_text(keep[txret].replace(GUARD, f"{guard};"))
    if arm is not None:
        sim.write_text(keep[sim].replace(ARM, f"pad_open_ && pad_idx_ == {arm}"))
    if phase:
        launch.write_text(keep[launch].replace(END, PHASE + END))
    done = subprocess.run(["make", "-s", *MAKE_ARGS, "run-mii", f"VERILATOR={verilator}"], cwd=suite, capture_output=True, text=True)
    (out / f"{name}.log").write_text(done.stdout + done.stderr)
    (out / f"{name}.rc").write_text(f"{done.returncode}\n")
    print(name, "rc", done.returncode)
try:
    case("shipped-load-at-octet-1", arm=9)
    case("guard-150-load-at-octet-14", guard="150")
    case("guard-150-load-at-octet-1", guard="150", arm=9)
    case("shipped-phase-census", phase=True)
    # every frame starts with the PHY's nibble mux left at 1, the state an eth_rst leaves it in mid-octet
    gen = suite / "generated/mac_tx_chain_mii.v"
    gen_keep = gen.read_text()
    anchor = "assign liteethphymiitx_converter_last = (liteethphymiitx_converter_mux == 1'd1);"
    assert anchor in gen_keep
    gen.write_text(gen_keep.replace(anchor, anchor + "\nalways @(posedge eth_tx_clk) if (!eth_tx_rst && !phy_sink_valid) liteethphymiitx_converter_mux <= 1'd1;"))
    MAKE_ARGS.append("-o"); MAKE_ARGS.append("model")
    case("stuck-nibble-phase-every-frame", phase=True)
    gen.write_text(gen_keep)
finally:
    for p, text in keep.items():
        p.write_text(text)
