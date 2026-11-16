#!/usr/bin/env python3
"""Focused ledger acceptance/refusal checks; no image builder or synthesis bank."""
import contextlib
from pathlib import Path
import sys
repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent / "scratch" / "memory"
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(repo / "sw/litex"))
import test_ctrl_memory as t
problems = []
t.ledger_arms(problems, out)
for rule, what, attempt in t.refusal_arms(out):
    if rule == "budget":
        t.refused(problems, rule, attempt, what)
t.ledger_plant_arms(problems, out, {"checks"} if not problems else set())
print("RESULT:", "FAIL" if problems else "PASS", "problems", len(problems))
sys.exit(bool(problems))
