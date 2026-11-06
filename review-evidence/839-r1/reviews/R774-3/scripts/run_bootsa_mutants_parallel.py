#!/usr/bin/env python3
"""Run the repository's own bootsa_mutants.py campaign with its mutants in parallel.

Usage: python3 -I run_bootsa_mutants_parallel.py <clone>/tb/verilator/milan_dp <workdir> <jobs>

The clean control and each MUTATIONS entry run in a separate child interpreter
that imports the campaign module unchanged and calls its own verdict() /
run_mutant(), so the plants, the named checks and the catch rule are the
repository's; only the scheduling differs (children in parallel instead of a
loop). Each child's stdout is captured whole. Set VERILATOR / VERILATOR_JOBS
in the environment; make's `?=` picks them up.
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

here = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3])
work.mkdir(parents=True, exist_ok=True)

CHILD = r"""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import bootsa_mutants as bm
idx = int(sys.argv[3])
if idx < 0:
    clean = Path(sys.argv[1]) / "obj_bootsa" / bm.EXE
    ok = clean.is_file() and bm.verdict(*bm.run_leg(clean), []) == "pass"
    print("[PASS] the unmutated gateware passes the obj_bootsa leg" if ok else
          "[FAIL] the unmutated gateware does NOT pass obj_bootsa")
else:
    d = Path(sys.argv[2]) / f"m{idx:02d}"
    d.mkdir(parents=True, exist_ok=True)
    ok = bm.run_mutant(bm.MUTATIONS[idx], d)
sys.exit(0 if ok else 1)
"""


def count() -> int:
    out = subprocess.run([sys.executable, "-I", "-c",
                          "import sys; sys.path.insert(0, sys.argv[1]); import bootsa_mutants as bm; "
                          "print(len(bm.MUTATIONS))", str(here)],
                         capture_output=True, text=True, check=True)
    return int(out.stdout.strip())


def one(idx: int):
    out = subprocess.run([sys.executable, "-I", "-c", CHILD, str(here), str(work), str(idx)],
                         capture_output=True, text=True, check=False)
    return idx, out.returncode == 0, out.stdout + out.stderr


n = count()
with ThreadPoolExecutor(max_workers=jobs) as ex:
    results = sorted(ex.map(one, range(-1, n)))
passes = fails = 0
for idx, ok, out in results:
    sys.stdout.write(out)
    passes += ok
    fails += not ok
print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL  ({n} mutants + clean control)")
sys.exit(1 if fails else 0)
