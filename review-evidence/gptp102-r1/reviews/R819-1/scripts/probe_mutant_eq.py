#!/usr/bin/env python3
"""Run tb/mutation_jobs_test.py's own checks against a planted-defect copy
of the driver, reusing a recorded --jobs 1 run instead of repeating it.

usage: probe_mutant_eq.py <tree> <driver> <jobs1-dir> <jobs1-rc>

The --jobs 1 path is untouched by the defects planted (they live in the
concurrent scheduler and in the printer), so the recorded serial run of the
same subset stands for it; the --jobs 4 run is executed for real.
"""
import sys
from pathlib import Path

tree, driver, j1, rc1 = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), int(sys.argv[4])
sys.path.insert(0, str(tree / "tb"))
sys.dont_write_bytecode = True
import mutation_jobs_test as t  # noqa: E402

real_run = t.run


def run(drv, jobs):
    if jobs == 1:
        return rc1, (j1 / "jobs1.stdout").read_bytes(), (j1 / "jobs1.stderr").read_bytes(), 0.0
    return real_run(drv, jobs)


t.run = run
sys.exit(t.main([driver, "--out", str(Path.cwd() / "out")]))
