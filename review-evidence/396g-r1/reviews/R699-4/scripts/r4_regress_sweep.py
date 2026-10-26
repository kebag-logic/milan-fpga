#!/usr/bin/env python3
"""Round-4 focused sweep near the one constant-mask regression found by r4_probe group C.

Usage: python3 -I r4_regress_sweep.py <path-to-tb/tools> <dir holding r3_probe.py and r4_probe.py> [jobs]

Code-bit (0x100) and 0x80000 excursions of 64..70 and 100 words starting near a
block boundary, with a one-word corruption 1..4 samples beside one or both ends.
Same oracle as r4_probe group C (flip neighbours). Run against two heads and diff.
"""
import sys
from multiprocessing import get_context

TOOLS, HERE = sys.argv[1], sys.argv[2]
JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 8
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], TOOLS, HERE]
import r4_probe as q  # noqa: E402


def cases():
    for mask in (0x100, 0x80000):
        for length in (64, 65, 66, 67, 70, 100):
            for begin in list(range(4080, 4097)) + list(range(6138, 6146)) + [3000]:
                for gap in (1, 2, 3, 4):
                    for side in ("before", "after", "both"):
                        yield mask, length, begin, gap, side, "flip"


def main():
    with get_context("fork").Pool(JOBS) as pool:
        res = pool.map(q.case_c, list(cases()), chunksize=8)
    bad = 0
    for name, ok, obs in res:
        bad += not ok
        print(name, "OK" if ok else "DEVIATION", flush=True)
    print("SUMMARY", len(res), "DEVIATION", bad)


if __name__ == "__main__":
    main()
