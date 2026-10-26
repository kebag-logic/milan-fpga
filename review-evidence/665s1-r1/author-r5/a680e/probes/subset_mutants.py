#!/usr/bin/env python3
"""Run a named subset of aecp_mutants.DEFECTS through its own campaign() (scratch check only;
the full campaign is the evidence). Usage: subset_mutants.py CHECKOUT OUT NAME..."""
import sys
from pathlib import Path
checkout, out, names = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), set(sys.argv[3:])
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
import aecp_mutants  # noqa: E402
chosen = tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
missing = names - {d.name for d in chosen}
if missing:
    raise SystemExit(f"unknown defects: {sorted(missing)}")
aecp_mutants.controls()          # the whole table is checked first
aecp_mutants.DEFECTS = chosen
aecp_mutants.controls = lambda: None
raise SystemExit(int(aecp_mutants.campaign(out, jobs=8)))
