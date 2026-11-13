#!/usr/bin/env python3
"""Reviewer re-run of the lane's own planted defects (#894), each on a disposable copy the
campaign drivers make under OUT_DIR; the reviewed clone is only read.

usage: run_lane_mutants.py CLONE OUT_DIR {ctrl|aecp|srp} [JOBS]
  ctrl  loop_step_mutants.tier_mutants (THE TIERS in ctrl_loop.c) through ctrl_mutants.campaign
  aecp  aecp_owed_mutants.ROWS and aecp_fan_mutants.ROWS through aecp_mutants.campaign
  srp   srp_transmit_mutants.sliced_defects through srp_mutants.campaign, at 2 and 1 interfaces
Each row's verdict line is the driver's own ([ok] caught on its named test's words / [ESCAPED]).
"""
import sys
from pathlib import Path

clone, out, which = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(clone / "sw/firmware/gtest"))
sys.dont_write_bytecode = True
out.mkdir(parents=True, exist_ok=True)

if which == "ctrl":
    import ctrl_mutants
    import loop_step_mutants
    from ctrl_reuse import cut_reuse
    from ctrl_mutant import Mutant
    table = loop_step_mutants.tier_mutants(Mutant)
    print(f"ctrl: {len(table)} tier mutants")
    ctrl_mutants.MUTANTS = tuple(table)
    ctrl_mutants.unnamed_tests = lambda: []   # the subset names only its own tests; the full table is the author's gate
    reuse = out / "reuse"
    cut_reuse(reuse)
    failed = ctrl_mutants.campaign(out, reuse, jobs, shard=[0, 1])
elif which == "aecp":
    import aecp_mutants
    import aecp_owed_mutants
    import aecp_fan_mutants
    names = {row[0] for row in (*aecp_owed_mutants.ROWS, *aecp_fan_mutants.ROWS)}
    aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
    aecp_mutants.controls = lambda: None   # the full-table drift check is the author gate's; this runs a subset
    print(f"aecp: {len(aecp_mutants.DEFECTS)} owed-queue and fan-out defects")
    failed = aecp_mutants.campaign(out, jobs)
elif which == "srp":
    import srp_mutants
    import srp_transmit_mutants
    table = tuple(srp_transmit_mutants.sliced_defects(srp_mutants.Defect))
    print(f"srp: {len(table)} resumed-build defects")
    srp_mutants.DEFECTS = table
    lwsrp = clone / "third_party/lwSRP"
    failed = srp_mutants.campaign(out / "if2", lwsrp, jobs, 2)
    failed = srp_mutants.campaign(out / "if1", lwsrp, jobs, 1) or failed
else:
    raise SystemExit(f"unknown campaign {which!r}")
print(f"RESULT: {'ESCAPED' if failed else 'ALL CAUGHT'}")
sys.exit(1 if failed else 0)
