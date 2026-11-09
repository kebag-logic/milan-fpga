#!/usr/bin/env python3
"""Run a slice of the F1 store's planted defects (nvm_mutants.MUTANTS[start:stop]) exactly as
test_ctrl_nvm.py --self-test grades them, so the bank fits a bounded wall-clock call.

usage: f1_selftest_slice.py <clone> <start> <stop> <jobs> [--controls]
--controls also runs the unnamed-test check and the over-capacity control (the rest of --self-test).
"""
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
start, stop, jobs = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
controls = "--controls" in sys.argv
sys.path.insert(0, str(clone / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as t  # noqa: E402

t.fw_gtest.EXECUTION.run = True
muts = t.nvm_mutants.MUTANTS[start:stop]
print(f"slice {start}:{stop} of {len(t.nvm_mutants.MUTANTS)} defects: {len(muts)}", flush=True)
with tempfile.TemporaryDirectory(prefix="f1-slice.") as tmp:
    work = Path(tmp)
    shapes = {}
    graded = {m.shape or t.SELF_TEST_SHAPE for m in muts} | ({t.SELF_TEST_SHAPE} if controls else set())
    for stem in graded:
        shapes[stem] = t.prepare(t.ROOT / "configs" / f"{stem}.yaml", work / "shapes" / stem)
    shared = t.fw_gtest.Build(jobs=1)
    listing = {s: t.build(shapes[s], work / "listing" / s, t.fw_gtest.Build(jobs=jobs, cache=shared.cache))
               for s in graded}
    held = {s: t.suite_tests(listing[s], shapes[s]) for s in graded}
    found = []
    if controls:
        found += [f"self-test: no defect names the test {n}"
                  for n in t.nvm_mutants.unnamed_checks(sorted(held[t.SELF_TEST_SHAPE]))]
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        found += [v for v in pool.map(lambda m: t.plant_and_grade(m, shapes[m.shape or t.SELF_TEST_SHAPE],
                                                                   held[m.shape or t.SELF_TEST_SHAPE],
                                                                   work / "mutants", shared), muts) if v]
    if controls:
        found += t.over_capacity_control(shapes[t.SELF_TEST_SHAPE], work / "over-capacity-control", shared)
for f in found:
    print("FINDING:", f)
print(f"slice {start}:{stop}: {len(muts) - sum(1 for f in found if 'NOT caught' in f or 'does not build' in f)} "
      f"of {len(muts)} caught; {len(found)} finding(s)")
sys.exit(1 if found else 0)
