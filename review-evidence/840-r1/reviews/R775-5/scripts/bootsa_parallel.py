#!/usr/bin/env python3
"""Run bootsa_mutants.py's own mutant list in parallel at one tree.

The repository's driver is sequential and sets no job count. This imports its
MUTATIONS, run_mutant() and verdict rules unchanged, gives each mutant its own
work directory, and runs them on a thread pool. The clean leg must already be
built in obj_bootsa, so the shared generated inputs exist before any mutant
build starts.

usage: bootsa_parallel.py <milan_dp dir> <work dir> <jobs>
Exit 0 only when the clean leg passes and every mutant is caught.
"""
import concurrent.futures as cf
import sys
from pathlib import Path

here, work, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
sys.path.insert(0, str(here))
import bootsa_mutants as bm  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
clean = here / "obj_bootsa" / bm.EXE
answer = bm.verdict(*bm.run_leg(clean), [])
print(f"clean leg: {answer}", flush=True)


def one(indexed):
    n, mutation = indexed
    d = work / f"m{n:02d}"
    d.mkdir(exist_ok=True)
    return n, mutation[0], bm.run_mutant(mutation, d)


fails = 0 if answer == "pass" else 1
with cf.ThreadPoolExecutor(jobs) as pool:
    for n, name, caught in pool.map(one, enumerate(bm.MUTATIONS)):
        print(f"RESULT m{n:02d} {'CAUGHT' if caught else 'NOT-CAUGHT'}: {name}", flush=True)
        fails += 0 if caught else 1
print(f"{len(bm.MUTATIONS)} mutants, {fails} failures", flush=True)
sys.exit(1 if fails else 0)
