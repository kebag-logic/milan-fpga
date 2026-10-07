#!/usr/bin/env python3
"""index_campaign.py CLONE OUT JOBS FIRST LAST - the head's own ctrl defect
campaign (ctrl_mutants.campaign, unchanged grading) on table entries
FIRST..LAST-1, to re-run a slice's tail whose log was cut short."""

from __future__ import annotations

import sys
from pathlib import Path

CLONE, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
JOBS, FIRST, LAST = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
sys.path.insert(0, str(CLONE / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(CLONE / "sw/firmware/gtest"))

import ctrl_mutants  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

ctrl_mutants.MUTANTS = ctrl_mutants.MUTANTS[FIRST:LAST]
print(f"entries {FIRST}..{LAST - 1}: {', '.join(m.name for m in ctrl_mutants.MUTANTS)}", flush=True)
ctrl_mutants.unnamed_tests = lambda *a, **k: []   # a partial table names only some tests
OUT.mkdir(parents=True, exist_ok=True)
cut_reuse(OUT / "reuse")
failed = ctrl_mutants.campaign(OUT / "mutants", OUT / "reuse", JOBS)
print(f"index_campaign: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
