#!/usr/bin/env python3
"""Compare self-test case lines: every base case line must appear verbatim at head.

    python3 compare_selftest_cases.py BASE.log HEAD.log
Prints counts, base lines missing at head, and head-only case names.
Exit 0 only when no base case line is missing and both logs end in PASS.
"""
import re
import sys
from collections import Counter

PAT = re.compile(r"^  (ok  |FAIL|NOT RUN) ")


def cases(path):
    text = open(path, encoding="utf-8", errors="backslashreplace").read()
    lines = [l.rstrip("\n") for l in text.splitlines() if PAT.match(l)]
    return lines, "\nselftest: PASS\n" in text + "\n"


base, base_pass = cases(sys.argv[1])
head, head_pass = cases(sys.argv[2])
missing = Counter(base) - Counter(head)
added = Counter(head) - Counter(base)
print(f"base cases {len(base)} pass={base_pass}; head cases {len(head)} pass={head_pass}")
print(f"base case lines missing at head: {sum(missing.values())}")
for line in missing:
    print("  MISSING", line)
names = sorted({l.split()[1] for l in added})
print(f"head-only case lines: {sum(added.values())}; distinct names: {len(names)}")
print("non-linear head-only names:", [n for n in names if not n.startswith("linear-")])
# order check: base lines appear in the same relative order at head
it = iter(head)
in_order = all(any(h == b for h in it) for b in base)
print(f"base order preserved at head: {in_order}")
sys.exit(0 if not missing and base_pass and head_pass and in_order else 1)
