#!/usr/bin/env python3
"""Does the arm prove the same property at either side of the REBOOT mask?

Plants the ACMP hold (a) where unb_mutants.py plants it, on arb_want_w, and
(b) on arb_req_w, after `arb_want_w & rbt_tx_open_w`, where the arm's old
anchor sat. Each leg is built through the Makefile's notify-build recipe and
run, and its [FAIL] lines are listed. Run from a disposable copy after
`make unb-mutants` has built that copy's clean leg.

Usage: python3 arm_equiv.py <copy-root> <work-dir>
"""
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
md = root / "tb/verilator/milan_dp"
hdl = root / "protocol-processor/hdl"
top = Path("top/protocol_processor_top.sv")
crf = root / "hdl/ieee1722/crf/KL_crf_rx.sv"

HOLD = """  logic [12:0] acmp_hold_cyc_r;
  always_ff @(posedge clk_i) begin : acmp_hold
    if (!rst_n || (laneq_acmp_cnt_r == 4'd0)) acmp_hold_cyc_r <= 13'd6000;
    else if (acmp_hold_cyc_r != 13'd0)        acmp_hold_cyc_r <= acmp_hold_cyc_r - 13'd1;
  end
"""
WANT = "  assign arb_want_w[LANE_ACMP_C]     = laneq_acmp_cnt_r != 4'd0;"
WANT_HELD = HOLD + ("  assign arb_want_w[LANE_ACMP_C]     = (laneq_acmp_cnt_r != 4'd0)\n"
                    "                                     && (acmp_hold_cyc_r == 13'd0);")
REQ = "  assign arb_req_w = arb_want_w & rbt_tx_open_w;"
REQ_HELD = HOLD + ("  logic [LANE_N_C-1:0] acmp_mask_w;\n"
                   "  always_comb begin : acmp_mask\n"
                   "    acmp_mask_w = '1;\n"
                   "    acmp_mask_w[LANE_ACMP_C] = (acmp_hold_cyc_r == 13'd0);\n"
                   "  end\n"
                   "  assign arb_req_w = arb_want_w & rbt_tx_open_w & acmp_mask_w;")

results = {}
for tag, old, new in (("want", WANT, WANT_HELD), ("req", REQ, REQ_HELD)):
    tree = work / f"pp_{tag}"
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(hdl, tree)
    text = (tree / top).read_text()
    assert text.count(old) == 1, (tag, text.count(old))
    (tree / top).write_text(text.replace(old, new))
    mdir = work / f"obj_{tag}"
    out = subprocess.run(
        ["make", "-s", "-C", str(md), "-o", "ltn_rom.hex", "-o", "ucode.hex", "notify-build",
         f"CRFRX_SRC={crf}", f"PP_DIR={tree}", f"NOTIFY_MDIR={mdir}"],
        capture_output=True, text=True, check=False)
    exe = mdir / "Vmilan_dp_notify"
    if out.returncode or not exe.is_file():
        print(f"{tag}: build failed rc={out.returncode}\n{out.stderr[-1500:]}")
        sys.exit(2)
    leg = subprocess.run([str(exe)], cwd=str(md), capture_output=True, text=True, check=False)
    log = leg.stdout + leg.stderr
    (work / f"leg_{tag}.log").write_text(log)
    fails = sorted(l.strip() for l in log.splitlines() if l.strip().startswith("[FAIL]"))
    results[tag] = fails
    print(f"{tag}: leg rc {leg.returncode}, {len(fails)} [FAIL] lines")
    for line in fails:
        print(f"  {line}")
    print("  " + next((l.strip() for l in log.splitlines() if l.strip().startswith("checks:")), "no tally"))

same = results["want"] == results["req"]
print(f"identical [FAIL] sets: {same}")
sys.exit(0 if same and results["want"] else 1)
