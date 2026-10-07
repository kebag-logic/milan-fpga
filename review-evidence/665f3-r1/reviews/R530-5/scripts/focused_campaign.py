#!/usr/bin/env python3
"""focused_campaign.py CLONE OUT JOBS - the head's own ctrl defect campaign
(ctrl_mutants.campaign, unchanged grading) restricted to every planted defect
whose file is the app composition (app/ctrl_app.[ch]) or whose name is a
round-6 composition defect, at the review clone's exact head.

Run with PYTHONDONTWRITEBYTECODE=1; the clone is only read (the planted
copies and builds go under OUT).
"""

from __future__ import annotations

import sys
from pathlib import Path

CLONE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
JOBS = int(sys.argv[3])
sys.path.insert(0, str(CLONE / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(CLONE / "sw/firmware/gtest"))

import ctrl_mutants  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

COMPOSITION = {"app-maap-channel-unbound", "app-three-way-pass-overrun", "maap-app-channel-closed",
               "maap-app-missing-rx-interrupt"}

selected = tuple(m for m in ctrl_mutants.MUTANTS if m.path.startswith("app/") or m.name in COMPOSITION)
print(f"focused: {len(selected)} of {len(ctrl_mutants.MUTANTS)} defects: {', '.join(m.name for m in selected)}",
      flush=True)
ctrl_mutants.MUTANTS = selected
# The table is restricted on purpose, so "a test no defect names" is not a
# finding of this run (the full table's check is the author's campaign).
ctrl_mutants.unnamed_tests = lambda *a, **k: []
OUT.mkdir(parents=True, exist_ok=True)
reuse = OUT / "reuse"
cut_reuse(reuse)
failed = ctrl_mutants.campaign(OUT / "mutants", reuse, JOBS)
print(f"focused_campaign: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
