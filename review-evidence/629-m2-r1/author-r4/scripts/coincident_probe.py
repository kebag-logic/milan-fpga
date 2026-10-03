#!/usr/bin/env python3
"""Probe, outside the tree: the gmstep --all control "a PHC step suppresses a
coincident CRF restart", as published (anchor RESTART_TRIGGER, the request's
last line) and planted inside the selected-CRF term group (anchor
CRF_RESTART_TERMS). Runs the campaign's own run_control on each."""
import importlib.util
import sys
import tempfile
from pathlib import Path

SUITE = Path("$LANES/629-m2-impl/tb/verilator/milan_dp")
spec = importlib.util.spec_from_file_location("gmstep_mutants", SUITE / "gmstep_mutants.py")
gm = importlib.util.module_from_spec(spec)
sys.modules["gmstep_mutants"] = gm
spec.loader.exec_module(gm)

published = [c for c in gm.CONTROLS if c.name == "a PHC step suppresses a coincident CRF restart"][0]
fixed = published._replace(
    name="the same defect planted inside the selected-CRF term group",
    anchor=gm.CRF_RESTART_TERMS,
    replacement=gm.CRF_RESTART_TERMS[:-1] + " & ~media_rebase_p_w)")
print("published anchor :", repr(published.anchor))
print("published replace:", repr(published.replacement))
print("fixed anchor     :", repr(fixed.anchor))
print("fixed replace    :", repr(fixed.replacement))
results = []
with tempfile.TemporaryDirectory(prefix="coinc-") as td:
    for tag, control in enumerate((published, fixed), start=1):
        caught = gm.run_control(control, Path(td), tag)
        results.append((control.name, caught))
for name, caught in results:
    print(f"{'CAUGHT' if caught else 'SURVIVED'}: {name}")
sys.exit(0 if results == [(published.name, False), (fixed.name, True)] else 1)
