#!/usr/bin/env python3
"""Reviewer probe arms on the exact-head aecp_dispatch_mutants.py driver.

usage: probe_dispatch.py <clone> <patch_dir> <output> <verilator> <jobs>
Loads the driver from the clone, points its patch directory at the reviewer's
patches, and runs the positive control plus each probe arm. A probe whose
expected words are "V" counts as KILLED on any failing V-section check; a
SURVIVED verdict is recorded, not raised.
"""
import importlib.util
import json
import sys
from pathlib import Path

clone, patches, output, verilator, jobs = sys.argv[1:6]
spec = importlib.util.spec_from_file_location(
    "drv", Path(clone) / "tb/pp_top/aecp_dispatch_mutants.py")
drv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drv)
drv.PATCHES = Path(patches)
arms = [(p.stem, p.stem, "aecp-dispatch", "V") for p in sorted(Path(patches).glob("*.patch"))]
out = Path(output)
out.mkdir(parents=True, exist_ok=True)
records = drv.campaign(out, arms, verilator, int(jobs))
(out / "results.json").write_text(json.dumps(records, indent=2) + "\n")
for r in records:
    print(json.dumps(r))
