#!/usr/bin/env python3
"""Compare maap mutants.py's per-arm tallies with tb/maap/README.md's 'N FAIL of M' column, row for row."""
import re
import sys
readme = open(sys.argv[1]).read()
summary = open(sys.argv[2]).read()
table = readme[readme.index("| Arm (patch) |"):]
expected = []
last = None
for line in table.splitlines()[2:]:
    if not line.startswith("|"):
        break
    cells = [c.strip() for c in line.strip("|").split("|")]
    arm = cells[0].strip("`") if cells[0] != "(same arm)" else last
    last = arm
    m = re.search(r"(\d+) FAIL of ([\d,]+)\s*$", cells[-1])
    expected.append((arm, int(m.group(1)), int(m.group(2).replace(",", ""))))
got = [(a, int(f), int(n)) for a, n, f in
       re.findall(r"^([\w-]+) \[\w+\]: rc=\d+ tally=\((\d+), (\d+)\) named=\d+ KILLED$", summary, re.M)]
print(f"README rows {len(expected)}, KILLED arm runs {len(got)}")
mism = sorted(set(expected) ^ set(got))
print("same rows, by arm:", sorted(expected) == sorted(got), "; same order:", expected == got)
print("mismatches:", mism)
sys.exit(bool(mism) or len(expected) != len(got))
