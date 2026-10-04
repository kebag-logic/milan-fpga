#!/usr/bin/env python3
"""cmp_sim_output.py A.log B.log - compare two suite logs on their simulation output.

Keeps only the lines a simulation prints ("[ ok ]", "[FAIL]", "[i]", "PROGRESS",
"AUDIO", "LOSS", "checks", "RESULT" and "==" tally lines), strips scratch-tree
paths and wall-clock figures, and reports whether the kept lines are identical,
plus each log's [FAIL] lines. Exit 0 when identical, 1 otherwise.
"""
import re
import sys

KEEP = re.compile(r"^\s*(\[ ok \]|\[FAIL\]|\[PASS\]|\[i\]|PROGRESS|AUDIO|LOSS|checks|RESULT|==|LOSS)")
STRIP = [(re.compile(r"/\S*/scratch/[^/\s]+/"), "<tree>/"),
         (re.compile(r"/tmp/\S+?/"), "<tmp>/"),
         (re.compile(r"wall_clock_seconds=\S+"), "wall_clock_seconds=<t>")]


def kept(path):
    out = []
    with open(path, errors="replace") as f:
        for line in f:
            if KEEP.match(line):
                for rx, rep in STRIP:
                    line = rx.sub(rep, line)
                out.append(line.rstrip("\n"))
    return out


def main():
    a, b = kept(sys.argv[1]), kept(sys.argv[2])
    same = a == b
    print(f"{sys.argv[1]}: {len(a)} simulation-output lines; {sys.argv[2]}: {len(b)}; identical={same}")
    for name, lines in ((sys.argv[1], a), (sys.argv[2], b)):
        for line in lines:
            if "[FAIL]" in line or line.lstrip().startswith("=="):
                print(f"  {name.rsplit('/', 1)[-1]}: {line.strip()[:200]}")
    if not same:
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print(f"  first difference at kept line {i + 1}:\n    A: {x[:200]}\n    B: {y[:200]}")
                break
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
