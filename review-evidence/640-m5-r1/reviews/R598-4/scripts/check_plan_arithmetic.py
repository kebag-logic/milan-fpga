#!/usr/bin/env python3
"""Recompute the partial-central sentence of MARK_II_AREA_PLAN.md from the plan's own rows.

Usage: check_plan_arithmetic.py <repo-root>
Reads docs/design/MARK_II_AREA_PLAN.md and docs/design/AREA_BUDGET.md at the checked-out
head, extracts the figures the sentence depends on, and prints each with its source line.
Exit 0 when every recomputed figure matches the sentence, 1 otherwise.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
plan = (root / "docs/design/MARK_II_AREA_PLAN.md").read_text(encoding="utf-8").splitlines()


def find(pattern):
    hits = [(i + 1, l) for i, l in enumerate(plan) if re.search(pattern, l)]
    if len(hits) != 1:
        print(f"pattern {pattern!r}: {len(hits)} hits")
        for n, l in hits:
            print(f"  {n}: {l}")
        sys.exit(1)
    return hits[0]


def num(s):
    return int(s.replace(",", ""))


ok = True
n, l = find(r"^Thus: `50,267 - 3,910 - 4,600 - 3,800 = 37,957`\.$")
print(f"plan:{n}: {l}")
base = 50267 - 3910 - 4600 - 3800
ok &= base == 37957
n, l = find(r"^\| Partial, F5 unqualified \| Central \| 37,957 \| \+83 \| -298 \|$")
print(f"plan:{n}: {l}")

central = {}
for lane, order in (("M2", 2), ("M5", 3), ("M6", 4)):
    n, l = find(rf"^\| {order} \| {lane} \| ([0-9,]+) \|")
    central[lane] = num(re.search(rf"^\| {order} \| {lane} \| ([0-9,]+) \|", l).group(1))
    print(f"plan:{n}: central {lane} = {central[lane]}")

measured = {}
for lane, pat in (
    ("M2", r"^The reproducible saving is (34) LUTs, below the 200"),
    ("M5", r"^M5 saved (121) LUTs routed and 127 post-synthesis in its scope"),
    ("M6", r"^The reproducible saving is (418) LUTs post-synthesis, 468 routed\.$"),
):
    n, l = find(pat)
    measured[lane] = int(re.search(pat, l).group(1))
    print(f"plan:{n}: measured {lane} = {measured[lane]}")

n, l = find(r"^With the measured savings of M2 \(34\), M5 \(121\) and M6 \(418\)")
print(f"plan:{n}: {l}")
m = re.search(r"becomes about ([0-9,]+), ([0-9,]+) over 38,040", l)
stated_image, stated_over = num(m.group(1)), num(m.group(2))
image = base + sum(central[k] - measured[k] for k in central)
over = image - 38040
print(f"recomputed: {base} + " + " + ".join(f"({central[k]} - {measured[k]})" for k in central)
      + f" = {image}, {over} over 38,040")
print(f"stated:     {stated_image}, {stated_over} over 38,040")
ok &= image == stated_image and over == stated_over
# Sensitivity: every lane on one basis (for the record, not a pass criterion).
alt = {"post-synthesis basis (34, 127, 418)": (34, 127, 418), "routed basis (128, 121, 468)": (128, 121, 468)}
for name, (a, b, c) in alt.items():
    v = base + (200 - a) + (600 - b) + (600 - c)
    print(f"sensitivity {name}: {v}, {v - 38040} over 38,040")
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
