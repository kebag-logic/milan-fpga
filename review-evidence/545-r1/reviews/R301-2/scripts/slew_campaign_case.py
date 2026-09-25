#!/usr/bin/env python3
"""Run ONE case of the head's tb/verilator/mmcm_servo/slew_mutants.py campaign.

The campaign's own module is imported from the scratch copy of the head and
its own run_case() grades the case, with the same anchor-count rule and the
same named-failure acceptance as main(). Only the per-invocation split is the
reviewer's: this host's foreground command limit is shorter than the whole
campaign, so cases run as separate commands (clean, clean_unit, then each
control). Usage: slew_campaign_case.py <case-name>
"""
import os
import sys
import tempfile
from pathlib import Path

PKT = Path(os.environ.get("PKT", "$REVIEWS/545-r301-2-packet"))
HERE = PKT / "scratch/tree/tb/verilator/mmcm_servo"
sys.path.insert(0, str(HERE))
import slew_mutants as sm  # noqa: E402

name = sys.argv[1]
source = sm.RTL.read_text()
cases = {"clean": (source, None, False), "clean_unit": (source, None, True)}
for n, anchor, repl, failure in (*sm.MUTANTS, sm.STREAK_MUTANT):
    if source.count(anchor) != 1:
        cases[n] = None
    else:
        cases[n] = (source.replace(anchor, repl), failure, n == sm.STREAK_MUTANT[0])
print("campaign cases:", ", ".join(cases))
if name not in cases:
    raise SystemExit(f"unknown case {name}")
if cases[name] is None:
    print(f"FAIL {name}: expected exactly one mutation anchor")
    raise SystemExit(1)
text, failure, unit = cases[name]
with tempfile.TemporaryDirectory(prefix="r301-slew-case-", dir=str(PKT / "scratch")) as d:
    ok = sm.run_case(Path(d), name, text, failure, unit=unit)
print(f"CASE {name}: {'PASS' if ok else 'FAIL'} (expected failure: {failure})")
raise SystemExit(0 if ok else 1)
