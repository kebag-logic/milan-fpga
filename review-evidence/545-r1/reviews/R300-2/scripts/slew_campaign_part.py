#!/usr/bin/env python3
"""Reviewer driver for the author's explicit servo slew campaign (#545).

Imports tb/verilator/mmcm_servo/slew_mutants.py from an exact-head tree and
calls its own run_case() for the named cases, so grading, anchors and
expected named failures are the author's, byte for byte. It exists only so
the campaign can be split across foreground invocations.

Usage: slew_campaign_part.py <tree> <work-dir> <case>...
  case: clean | clean_unit | <MUTANTS name> | slew_streak_reset_removed
"""
import sys
from pathlib import Path

tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "tb/verilator/mmcm_servo"))
import slew_mutants as m  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
source = m.RTL.read_text()
table = {name: (a, r, f) for name, a, r, f in (*m.MUTANTS, m.STREAK_MUTANT)}
results = []
for case in sys.argv[3:]:
    if case == "clean":
        ok = m.run_case(work, "clean", source, None)
    elif case == "clean_unit":
        ok = m.run_case(work, "clean_unit", source, None, unit=True)
    else:
        anchor, repl, failure = table[case]
        if source.count(anchor) != 1:
            print(f"FAIL {case}: expected exactly one mutation anchor")
            ok = False
        else:
            ok = m.run_case(work, case, source.replace(anchor, repl), failure,
                            unit=case == m.STREAK_MUTANT[0])
    results.append(ok)
    print(f"CASE {case}: {'PASS' if ok else 'FAIL'}", flush=True)
print(f"PART: {len(results)} cases, {sum(not r for r in results)} failures")
sys.exit(1 if not all(results) else 0)
