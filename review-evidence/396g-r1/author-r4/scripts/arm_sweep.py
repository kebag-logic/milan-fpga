#!/usr/bin/env python3
"""A DUT slip 1 to 64 samples before or after each planted arm: is the run ever not FAIL?

Usage: python3 -I arm_sweep.py <path-to-tb/tools> <dir holding the reviewer's r3_probe.py> [jobs]

Captures come from the reviewer's encoder and arm set (r3_probe.grade: drop
arms at 300 and F-700, repeat arms at 500 and F-450, flip arms on channel 1
at 700 and F-200, tolerance 2). Slip sizes 1, -1, 2, -2, 3, 5, 100, 1024,
-1024, 2048, -2048, 4096, -4096 and 8192, on every channel or on channel 1
alone. Prints every case that is not FAIL, then a SUMMARY of the case count
and the non-FAIL counts by arm and side. Exit status 0.
"""
import collections
import sys
from multiprocessing import get_context

sys.path.insert(0, sys.argv[2])
TOOLS = sys.argv[1]
JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 8
sys.argv = [sys.argv[0], TOOLS]
import r3_probe as p  # noqa: E402

F = 16384


def run(args):
    arm, k, n, scope = args
    op = ("shift", arm + k, n) if scope == "all" else ("shift", arm + k, n, 1)
    v, d, _ = p.grade(F, [op])
    return args, v, d["why"], d["planted_missed"]


def main():
    arms = (300, 500, 700, F - 700, F - 450, F - 200)
    cases = [(arm, k, n, scope) for arm in arms for k in list(range(-64, 0)) + list(range(1, 65))
             for n in (1, -1, 2, -2, 3, 5, 100, 1024, -1024, 2048, -2048, 4096, -4096, 8192) for scope in ("all", "ch1")]
    bad = collections.Counter()
    with get_context("fork").Pool(JOBS) as pool:
        for args, v, why, missed in pool.imap(run, cases, chunksize=16):
            if v != "FAIL":
                bad[(args[0], "before" if args[1] < 0 else "after")] += 1
                print(args, v, why, missed, flush=True)
    print("SUMMARY", len(cases), dict(bad))


if __name__ == "__main__":
    main()
