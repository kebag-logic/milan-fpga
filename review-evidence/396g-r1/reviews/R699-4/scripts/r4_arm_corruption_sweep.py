#!/usr/bin/env python3
"""Round-4 sweep: one DUT one-word corruption at a planted arm + d.

Usage: python3 -I r4_arm_corruption_sweep.py <path-to-tb/tools> <dir holding r3_probe.py> [jobs]

Words from r3_probe.py's own encoder; arms are its standard log (drop 3 at
300 and F-700, repeat 2 at 500 and F-450, flip 0x100 on channel 1 at 700 and
F-200; tolerance 2), F = 16384. For each arm, d in -64..64, each channel and
each mask, the run's verdict. The oracle: a single DUT corruption at another
sample than the arm (d != 0) FAILs with every arm found. d = 0 is listed apart.
Prints one line per NOT RUN case and a summary table. Exit status is 0.
"""
import collections
import json
import sys
from multiprocessing import get_context

TOOLS, HERE = sys.argv[1], sys.argv[2]
JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 8
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], TOOLS]
import r3_probe as p  # noqa: E402

F = 16384
ARMS = {300: "drop3", 500: "repeat2", 700: "flip-ch1", F - 700: "drop3-end", F - 450: "repeat2-end",
        F - 200: "flip-ch1-end"}
MASKS = (0x100, 0x200, 0x1E00, 0x40000, 0x80000, 0x80100, 0x100000, 0x01000000)


def cases():
    for arm in ARMS:
        for d in range(-64, 65):
            for ch in range(p.C):
                for mask in MASKS:
                    yield arm, d, ch, mask


def case(args):
    arm, d, ch, mask = args
    v, det, dut = p.grade(F, [("xor", arm + d, ch, mask)])
    return args, v, det.get("planted_missed"), [p.brief(e) for e in dut][:6]


def main():
    with get_context("fork").Pool(JOBS) as pool:
        res = pool.map(case, list(cases()), chunksize=16)
    table = collections.Counter()
    total = collections.Counter()
    for (arm, d, ch, mask), v, missed, obs in res:
        key = (ARMS[arm], "own" if d == 0 else "other")
        total[key] += 1
        if v != "FAIL" or missed:
            table[key] += 1
            print("NOTFAIL", json.dumps({"arm": arm, "d": d, "ch": ch, "mask": f"0x{mask:X}", "verdict": v,
                                         "missed": missed, "dut": obs}), flush=True)
    for key in sorted(total):
        print("SUMMARY", key[0], key[1], f"not-FAIL={table[key]} of {total[key]}")
    byd = collections.Counter()
    for (arm, d, ch, mask), v, missed, obs in res:
        if d and (v != "FAIL" or missed):
            byd[(ARMS[arm], d, f"0x{mask:X}")] += 1
    for k in sorted(byd):
        print("BY-D", *k, byd[k])


if __name__ == "__main__":
    main()
