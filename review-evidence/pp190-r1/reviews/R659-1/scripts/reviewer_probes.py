#!/usr/bin/env python3
"""Reviewer probes for the per-source TSpec MaxFrameSize (issue #190).

Plants extra defects in the top's talker stage with the suite's own mutation
machinery (tb/pp_top/acmp_mutants.py of the tree under review) and grades each
against section TS (`--tspec-only`). A probe marked EXPECT_SURVIVE plants a
change the design is meant to be blind to.

Usage: python3 reviewer_probes.py TREE OUTPUT VERILATOR JOBS
"""
import concurrent.futures
import json
import sys
from pathlib import Path

tree, output, verilator, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), \
    sys.argv[3], int(sys.argv[4])
sys.path.insert(0, str(tree / "tb" / "pp_top"))
import acmp_mutants as am  # noqa: E402  (the tree under review)

TOP = am.TOP
SLOT = am.TS_SLOT
SUITE = am.PP_TOP_TS
PROBES = (
    # neighbouring slots swapped (src ^ 1): a wrong but per-source index
    ("rv_slot_xor1", ((TOP, SLOT, "mfs:   cfg_tspec_max_frame_i[32'(tkr_gate_src_w ^ 1'b1) * 16 +: 16],"),),
     ("TS1: source 0 declares its own slot's MaxFrameSize",
      "TS1: source 1 declares its own slot's MaxFrameSize"), "KILL"),
    # stride 8 instead of 16: overlapping slices
    ("rv_stride8", ((TOP, SLOT, "mfs:   cfg_tspec_max_frame_i[32'(tkr_gate_src_w) * 8 +: 16],"),),
     ("TS1: source 1 declares its own slot's MaxFrameSize",), "KILL"),
    # only the upper byte of the slot (a narrowed field)
    ("rv_low_byte_dropped", ((TOP, SLOT, "mfs:   {cfg_tspec_max_frame_i[32'(tkr_gate_src_w) * 16 + 8 +: 8], 8'd0},"),),
     ("TS1: source 1 declares its own slot's MaxFrameSize",), "KILL"),
    # gate close takes slot 0: the SRP core stores the TSpec on gate open only
    # (KL_srp_talker_fsm walk_tspec_write, KL_srp_top S_GATE), so a close
    # carries no TSpec; this probe is expected to survive (equivalent)
    ("rv_close_slot0", ((TOP, SLOT,
      "mfs:   cfg_tspec_max_frame_i[(tkr_gate_open_w ? 32'(tkr_gate_src_w) : 32'd0) * 16 +: 16],"),),
     ("TS1: source 1 declares its own slot's MaxFrameSize",), "EXPECT_SURVIVE"),
)


def one(p):
    name, edits, checks, expect = p
    rec = am.judge(name, SUITE, edits, checks, (tree, output, verilator))
    rec["expect"] = expect
    return rec


output.mkdir(parents=True, exist_ok=True)
gold = am.judge("golden-tspec", SUITE, (), (), (tree, output, verilator))
records = [gold]
if gold["verdict"] == "PASS":
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        records += list(pool.map(one, PROBES))
(output / "results.json").write_text(json.dumps(records, indent=1) + "\n")
ok = gold["verdict"] == "PASS"
for r in records:
    print(json.dumps({k: r.get(k) for k in ("mutant", "verdict", "expect", "missing", "failing_checks")}))
    if r.get("expect") == "KILL" and r["verdict"] != "KILLED":
        ok = False
    if r.get("expect") == "EXPECT_SURVIVE" and r["verdict"] != "SURVIVED":
        ok = False
print("PROBES", "AS EXPECTED" if ok else "UNEXPECTED")
sys.exit(0 if ok else 1)
