#!/usr/bin/env python3
"""Run bootsa_mutants.py's positive control and every MUTATIONS arm through
its own run_mutant()/verdict(), several arms at once, one process per arm.

Usage: python3 -I run_mutants_parallel.py <repo>/tb/verilator/milan_dp <workdir> [workers]
Set VERILATOR and VERILATOR_JOBS in the environment (the Makefile reads both
with ?=). Exit 0 only when the clean leg passes and every arm is caught.
"""
import contextlib
import io
import multiprocessing
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(HERE))
import bootsa_mutants as bm  # noqa: E402


def one(m):
    buf = io.StringIO()
    t0 = time.time()
    with contextlib.redirect_stdout(buf):
        ok = bm.run_mutant(m, WORK)
    return ok, buf.getvalue().strip(), time.time() - t0


def main() -> int:
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    WORK.mkdir(parents=True, exist_ok=True)
    clean = HERE / "obj_bootsa" / bm.EXE
    answer = bm.verdict(*bm.run_leg(clean), []) if clean.is_file() else "no clean build"
    print(f"clean leg: {answer}", flush=True)
    ctx = multiprocessing.get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        results = list(pool.map(one, bm.MUTATIONS))
    caught = 0
    for ok, text, dt in results:
        caught += ok
        print(f"{text}  [{dt:.0f}s]")
    n = len(bm.MUTATIONS)
    print(f"\nclean leg {answer}; {caught}/{n} mutants caught")
    return 0 if answer == "pass" and caught == n else 1


if __name__ == "__main__":
    sys.exit(main())
