#!/usr/bin/env python3
"""R524-3: grade the NVM planted defects NOT already graded in a previous log, through the
repository's own test_ctrl_nvm.self_test / plant_and_grade.

Usage (from the clone root): nvm_campaign_rest.py <previous-log> <work> <jobs>
A defect counts as graded only by a "self-test OK: <name>" line in <previous-log>; every other
defect of nvm_mutants.MUTANTS is graded here, so the two logs together cover each exactly once.
The unnamed-test check runs against the FULL defect list first.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path[:0] = [str(ROOT / "sw/firmware/ctrl_nvm/test"), str(ROOT / "sw/firmware/gtest")]

import nvm_mutants  # noqa: E402
import test_ctrl_nvm as gate  # noqa: E402

prev, work, jobs = Path(sys.argv[1]), Path(sys.argv[2]).resolve(), int(sys.argv[3])
done = set(re.findall(r"self-test OK: (\S+)", prev.read_text()))
everything = nvm_mutants.MUTANTS
known = {m.name for m in everything}
assert done <= known, done - known
rest = tuple(m for m in everything if m.name not in done)
print(f"previously graded {len(done)}, grading {len(rest)} here, total {len(everything)}: "
      f"{', '.join(m.name for m in rest)}", flush=True)

# The unnamed-test check against the full list, as self_test does it.
stem = gate.SELF_TEST_SHAPE
shape = gate.prepare(ROOT / "configs" / f"{stem}.yaml", work / "full" / stem)
exes = gate.build(shape, work / "full-listing" / stem, gate.fw_gtest.Build(jobs=jobs))
held = gate.suite_tests(exes, shape)
unnamed = nvm_mutants.unnamed_checks(sorted(held))
print(f"unnamed checks against all {len(everything)} defects: {unnamed or 'none'}", flush=True)

nvm_mutants.MUTANTS = rest
found = gate.self_test({}, work / "self-test", jobs)
found = [f for f in found if not f.startswith("self-test: no defect names the test")]
for f in found:
    print(f"FINDING: {f}")
print(f"rest: {len(rest) - len(found)} of {len(rest)} caught; unnamed: {len(unnamed)}")
sys.exit(1 if found or unnamed else 0)
