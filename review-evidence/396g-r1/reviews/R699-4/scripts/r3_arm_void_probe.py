#!/usr/bin/env python3
"""A DUT slip k samples after a planted flip arm: is the run ever void?

Usage: python3 -I r3_arm_void_probe.py <path-to-tb/tools> <dir holding r3_probe.py> [jobs]

Arms as r3_probe.py (start flip arm at 700 and end flip arm at F-200, both on
channel 1, mask 0x100). The DUT slip is on every channel, or on channel 1
alone, at arm + k. Round-3 assignment item 3: a slip and a one-word
corruption in one window never void a run whose arms are all present.
Each line: <id> <verdict> <why> ; then a summary of NOT RUN counts by size.
"""
import collections
import json
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
    return f"V-arm{arm}-k{k}-n{n}-{scope}", v, d["why"]


def main():
    cases = [(arm, k, n, scope) for arm in (700, F - 200) for k in range(1, 65)
             for n in (1, 3, -2, 100, 2048, -2048, 4096, -4096, 8192) for scope in ("all", "ch1")]
    void = collections.Counter()
    total = collections.Counter()
    with get_context("fork").Pool(JOBS) as pool:
        for pid, v, why in pool.imap(run, cases, chunksize=8):
            n = pid.split("-n")[1].rsplit("-", 1)[0]
            total[n] += 1
            if v != "FAIL":
                void[n] += 1
                print(pid, v, json.dumps(why), flush=True)
    for n in total:
        print(f"SUMMARY n={n} not-FAIL={void[n]} of {total[n]}", flush=True)


if __name__ == "__main__":
    main()
