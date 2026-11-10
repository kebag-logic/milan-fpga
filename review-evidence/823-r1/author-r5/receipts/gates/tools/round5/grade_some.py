"""Grade named planted defects of the split store with the suite's own functions (round 4's grade_some.py, with
the named tests' log kept for each defect under <work>/logs/<name>.log).

usage: python3 grade_some.py <lane root> <work dir> <mutant names, comma separated> [--jobs N]
"""
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as t  # noqa: E402
import nvm_mutants  # noqa: E402
import fw_gtest  # noqa: E402

work = Path(sys.argv[2]).resolve()
(work / "logs").mkdir(parents=True, exist_ok=True)
names = [n for n in sys.argv[3].split(",") if n]
jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 4
want = [m for m in nvm_mutants.MUTANTS if m.name in names]
missing = set(names) - {m.name for m in want}
if missing:
    print("unknown mutants:", sorted(missing))
    sys.exit(2)
shapes, held, shared = {}, {}, fw_gtest.Build(jobs=1)
for stem in sorted({m.shape or t.SELF_TEST_SHAPE for m in want}):
    shapes[stem] = t.prepare(root / "configs" / f"{stem}.yaml", work / "shapes" / stem)
    exes = t.build(shapes[stem], work / "listing" / stem, fw_gtest.Build(jobs=8, cache=shared.cache))
    held[stem] = t.suite_tests(exes, shapes[stem])


def grade(m):
    stem = m.shape or t.SELF_TEST_SHAPE
    shape, tree = shapes[stem], work / "mutants" / m.name / "tree"
    nvm_mutants.plant(m, tree)
    try:
        exes = t.build(shape, work / "mutants" / m.name, shared, tree)
    except t.Refusal as exc:
        return f"{m.name}: does not build: {exc}"
    logs = ""
    for binary in t.binaries(shape):
        kills = [k for k in m.kills if held[stem].get(k) == binary.name]
        if kills:
            logs += t.run_suite(exes[binary.name], t.fixture_of(shape, binary), kills)[1]
    shutil.rmtree(work / "mutants" / m.name, ignore_errors=True)
    (work / "logs" / f"{m.name}.log").write_text(logs)
    alive = nvm_mutants.survivors(m, logs)
    return f"{m.name}: NOT caught by {', '.join(alive)}" if alive else f"{m.name}: caught"


with ThreadPoolExecutor(max_workers=jobs) as pool:
    verdicts = list(pool.map(grade, want))
for v in verdicts:
    print(v)
bad = [v for v in verdicts if not v.endswith(": caught")]
print(f"graded {len(want)} mutants: {'PASS' if not bad else 'FAIL'}")
sys.exit(1 if bad else 0)
