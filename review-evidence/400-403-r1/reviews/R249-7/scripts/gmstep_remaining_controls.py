#!/usr/bin/env python3
"""Run the gmstep-leg controls of gmstep_mutants.py that are neither in the
default sweep, nor the --slew set, nor on the option-off leg, so that the
three receipts together cover the whole `make gmstep-mutants` inventory.
Reuses the suite's own functions. Usage: gmstep_remaining_controls.py <milan_dp dir>
"""
import sys
import tempfile
from pathlib import Path

here = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(here))
import gmstep_mutants as gm  # noqa: E402

selected = [c for c in gm.CONTROLS if not c.acceptance and c.leg != "option-off"
            and not c.name.startswith("the policy level")]
print(f"inventory={len(gm.CONTROLS)} selected={len(selected)}")
passes = fails = 0
with tempfile.TemporaryDirectory(prefix="gmstep-rest-") as td:
    work = Path(td)
    for tag, control in enumerate(selected):
        if gm.run_control(control, work, tag):
            passes += 1
        else:
            fails += 1
print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
sys.exit(1 if fails or not selected else 0)
