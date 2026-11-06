#!/usr/bin/env python3
"""Equivalence probe for unb_mutants.py's first arm.
Usage: probe_unb_arm_equiv.py <milan_dp dir of a disposable copy> <out dir>
Plants the 6,000-cycle ACMP hold at two stages of a disposable copy: the
head's stage (arb_want_w) and the stage the arm used before processor #203
(the request the arbiter receives, arb_req_w, after the REBOOT gate), builds
each through the driver's own recipe, and compares the sets of [FAIL] lines
and the tallies. Equal sets mean the re-anchored arm plants the same defect."""
import importlib.util, pathlib, re, sys, tempfile
here = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("unb", here / "unb_mutants.py")
unb = importlib.util.module_from_spec(spec); sys.modules["unb"] = unb; spec.loader.exec_module(unb)
GATE = "  assign arb_req_w = arb_want_w & rbt_tx_open_w;"
HOLD = """  logic [12:0] acmp_hold_cyc_r;
  always_ff @(posedge clk_i) begin : acmp_hold
    if (!rst_n || (laneq_acmp_cnt_r == 4'd0)) acmp_hold_cyc_r <= 13'd6000;
    else if (acmp_hold_cyc_r != 13'd0)        acmp_hold_cyc_r <= acmp_hold_cyc_r - 13'd1;
  end
  logic [LANE_N_C-1:0] acmp_hold_mask_w;
  always_comb begin : acmp_hold_mask
    acmp_hold_mask_w = '1;
    acmp_hold_mask_w[LANE_ACMP_C] = (acmp_hold_cyc_r == 13'd0);
  end
  assign arb_req_w = arb_want_w & rbt_tx_open_w & acmp_hold_mask_w;"""
arm = unb.MUTATIONS[0]
stage_req = arm._replace(name="req stage", edits=[("pp", GATE, HOLD)])
stage_want = arm._replace(name="want stage")
results = {}
with tempfile.TemporaryDirectory(prefix="unb-equiv-", dir=out.parent) as td:
    work = pathlib.Path(td)
    for tag, m in (("want", stage_want), ("req", stage_req)):
        planted = unb.plant(m, work, tag)
        assert planted, tag
        exe = unb.build(planted[0], planted[1], work / f"obj_{tag}")
        assert exe, tag
        rc, text = unb.run_leg(exe)
        (out / f"unb_arm1_{tag}.log").write_text(text)
        fails = sorted(l.strip() for l in text.splitlines() if l.strip().startswith("[FAIL]"))
        tally = re.findall(r"checks: (\d+)\s+failures: (\d+)", text)
        results[tag] = (rc, fails, tally, unb.verdict(rc, text, m))
for tag, (rc, fails, tally, v) in results.items():
    print(tag, "rc", rc, "tally", tally, "verdict", v)
    for f in fails:
        print("   ", re.sub(r"\s+got.*|\s+=.*", "", f)[:150])
norm = lambda fs: [re.sub(r"\(.*", "", f) for f in fs]
same = norm(results["want"][1]) == norm(results["req"][1]) and results["want"][2] == results["req"][2]
print("EQUIVALENT" if same else "DIFFERENT")
sys.exit(0 if same else 1)
