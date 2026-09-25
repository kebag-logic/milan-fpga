#!/usr/bin/env python3
"""Reviewer driver for the author's explicit servo slew campaign (#545), R300-3.

Imports tb/verilator/mmcm_servo/slew_mutants.py from an exact-head tree and
calls its own run_case() for the named cases, so grading, anchors and
expected named failures are the author's, byte for byte. It exists only so
the campaign can be split across foreground invocations. Differs from the
R300-2 driver only in reading the round-3 STREAK_MUTANTS tuple.

Usage: slew_campaign_part_r3.py <tree> <work-dir> <case>...
  case: clean | clean_unit | <MUTANTS name> | <STREAK_MUTANTS name>
"""
import sys
from pathlib import Path

tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "tb/verilator/mmcm_servo"))
import slew_mutants as m  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
source = m.RTL.read_text()
streak = {item[0] for item in m.STREAK_MUTANTS}
table = {name: (a, r, f) for name, a, r, f in (*m.MUTANTS, *m.STREAK_MUTANTS)}
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
                            unit=case in streak)
    results.append(ok)
    print(f"CASE {case}: {'PASS' if ok else 'FAIL'}", flush=True)
print(f"PART: {len(results)} cases, {sum(not r for r in results)} failures")
sys.exit(1 if not all(results) else 0)
