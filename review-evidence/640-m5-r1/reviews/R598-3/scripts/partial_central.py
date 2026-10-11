#!/usr/bin/env python3
"""Recompute the Mark II plan's partial-central scenario (docs/design/MARK_II_AREA_PLAN.md,
"No-split and partial-flip estimates") from the figures the composed plan states, once with
M5's measured saving alone (the plan's own sentence) and once with every measured lane the
composed plan records (M2, M5, M6). Usage: partial_central.py <plan.md>"""
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
def need(pat):
    m = re.search(pat, text)
    if not m:
        sys.exit(f"pattern not found: {pat}")
    return m
m = need(r"`50,267 - 3,910 - 4,600 - 3,800 = 37,957`")
need(r"\| 2 \| M2 \| 200 \|"); need(r"\| 3 \| M5 \| 600 \|"); need(r"\| 4 \| M6 \| 600 \|")
need(r"The reproducible saving is 34 LUTs")              # M2
need(r"The reproducible saving is 418 LUTs post-synthesis, 468 routed")  # M6
need(r"M5 saved 121 LUTs routed and 127 post-synthesis")  # M5
stated = need(r"At M5's measured 121, the partial-central scenario becomes about ([\d,]+), ([\d,]+) over 38,040")
base, split, rest, m3m10, bar = 50267, 3910, 4600, 3800, 38040
plan = {"M2": 200, "M5": 600, "M6": 600}
def image(meas):
    r = rest - sum(plan[k] for k in meas) + sum(meas.values())
    return base - split - r - m3m10
cases = {
    "plan figures (as tabled)": {},
    "M5 measured 121 only (the plan's sentence)": {"M5": 121},
    "M2 34 + M5 121 + M6 418 (reproducible figures)": {"M2": 34, "M5": 121, "M6": 418},
    "M2 34 + M5 127 + M6 418 (all post-synthesis)": {"M2": 34, "M5": 127, "M6": 418},
    "M2 34 + M5 121 + M6 468 (M6 routed)": {"M2": 34, "M5": 121, "M6": 468},
}
print(f"plan sentence states: {stated.group(1)}, {stated.group(2)} over {bar:,}")
for name, meas in cases.items():
    img = image(meas)
    print(f"{name:52s} image {img:,}  vs 38,040: {img - bar:+,}")
