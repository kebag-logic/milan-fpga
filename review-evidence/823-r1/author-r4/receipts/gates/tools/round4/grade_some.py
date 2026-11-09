"""Grade named planted defects of the F1 store with the suite's own functions.

usage: python3 grade_some.py <lane root> <work dir> <mutant names, comma separated> [--widths]
"""
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as t  # noqa: E402
import nvm_mutants  # noqa: E402
import fw_gtest  # noqa: E402

work = Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
names = [n for n in sys.argv[3].split(",") if n]
want = [m for m in nvm_mutants.MUTANTS if m.name in names]
missing = set(names) - {m.name for m in want}
if missing:
    print("unknown mutants:", sorted(missing))
    sys.exit(2)
stem = t.SELF_TEST_SHAPE
shape = t.prepare(root / "configs" / f"{stem}.yaml", work / "shape")
shared = fw_gtest.Build(jobs=1)
exes = t.build(shape, work / "listing", fw_gtest.Build(jobs=8, cache=shared.cache))
held = t.suite_tests(exes, shape)
unnamed = nvm_mutants.unnamed_checks(sorted(held))
print("unnamed checks:", unnamed)
bad = [v for v in (t.plant_and_grade(m, shape, held, work / "mutants", shared) for m in want) if v]
if "--widths" in sys.argv:
    bad += t.over_width_control(shape, work / "width-control", shared)
for b in bad:
    print("FINDING:", b)
print(f"graded {len(want)} mutants{' and the width controls' if '--widths' in sys.argv else ''}: "
      f"{'PASS' if not bad and not unnamed else 'FAIL'}")
sys.exit(1 if bad or unnamed else 0)
