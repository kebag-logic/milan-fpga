#!/usr/bin/env python3
"""campdiff.py <base.log> <head.log>: compare two srp_top campaign logs verdict by verdict.

Verdicts are matched by label and occurrence (a label graded on two suites prints twice, in the
driver's declared order). Prints every arm whose failure count, verdict or tags differ, the arms
only one side has, and the controls of each side.
"""
import re
import sys
from collections import defaultdict

LINE = re.compile(r"^(?P<label>[A-Za-z0-9-]+): rc=(?P<rc>\d+) failures=(?P<n>\d+) (?P<v>KILLED|UNPROVEN) tags=(?P<tags>.*)$")


def read(path):
    seen = defaultdict(int)
    out = {}
    controls = []
    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("control "):
            controls.append(line)
            continue
        m = LINE.match(line)
        if not m:
            continue
        k = (m["label"], seen[m["label"]])
        seen[m["label"]] += 1
        out[k] = (int(m["n"]), m["v"], m["tags"])
    return out, controls


def main():
    base, bc = read(sys.argv[1])
    head, hc = read(sys.argv[2])
    same = moved = 0
    for k in sorted(set(base) | set(head)):
        b, h = base.get(k), head.get(k)
        if b is None:
            print(f"HEAD ONLY  {k[0]}#{k[1]}: {h[0]} {h[1]} {h[2]}")
        elif h is None:
            print(f"BASE ONLY  {k[0]}#{k[1]}: {b[0]} {b[1]} {b[2]}")
        elif b != h:
            moved += 1
            print(f"MOVED      {k[0]}#{k[1]}: base {b[0]} {b[1]} {b[2]}  ->  head {h[0]} {h[1]} {h[2]}")
        else:
            same += 1
    print(f"same {same}, moved {moved}, base {len(base)}, head {len(head)}")
    print(f"controls base {len(bc)}, head {len(hc)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
