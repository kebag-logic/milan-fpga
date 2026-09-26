#!/usr/bin/env python3
"""Run only the option-off-leg controls of tb/verilator/milan_dp/gmstep_mutants.py.

The composed tree grades #387/#545's two option-off controls against this
PR's changed sim_main.cpp. This driver reuses the suite's own CONTROLS,
LEGS, build and verdict functions unchanged and selects the controls whose
leg is "option-off". Usage: gmstep_optoff_controls.py <milan_dp dir>
"""
import sys
import tempfile
from pathlib import Path

here = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(here))
import gmstep_mutants as gm  # noqa: E402

selected = [c for c in gm.CONTROLS if c.leg == "option-off"]
passes = fails = 0
with tempfile.TemporaryDirectory(prefix="gmstep-optoff-") as td:
    work = Path(td)
    leg = gm.LEGS["option-off"]
    exe = leg.clean_mdir / leg.exe_name
    if not gm.is_fresh(leg, exe):
        print("[INFO] positive control rebuilt")
        exe = gm.build(leg, {}, work / "obj_clean_optoff")
    answer = gm.verdict(*gm.run_leg(leg, exe), None) if exe else "did not compile"
    print(f"[{'PASS' if answer == 'pass' else 'FAIL'}] unmutated option-off leg: {answer}")
    passes, fails = (1, 0) if answer == "pass" else (0, 1)
    for tag, control in enumerate(selected):
        if gm.run_control(control, work, tag):
            passes += 1
        else:
            fails += 1
print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL ({len(selected)} option-off controls)")
sys.exit(1 if fails or not selected else 0)
