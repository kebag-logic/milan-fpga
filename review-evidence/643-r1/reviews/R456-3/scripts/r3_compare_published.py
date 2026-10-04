#!/usr/bin/env python3
"""R456-3: compare every window this round's tdm8render-law-boundary run
printed with the author's published round3-boundary-walks.md, cell by cell.
Usage: r3_compare_published.py BND_LOG PUBLISHED_MD SECTION
SECTION is the published heading's processor ("631eeb34" or "c4cb84ff").

From the log: each verdict line sets (design, history); the "[i]   +p:" lines
under it give (nearest-pop low..high, walk, clearance, outcome). The published
table has one row per phase with Ascending, Descending and Alone cells for the
unmutated design; its header also says the setpoint defects give the same
offsets, so the defect runs are compared with the same cells."""
import re
import sys

log, md, sec = sys.argv[1], sys.argv[2], sys.argv[3]
VER = re.compile(r"^\[(?:PASS|FAIL)\] law boundary, (the [^,]+), (the leg's own scan|descending|\+\d+ alone)")
WIN = re.compile(r"^  \[i\]   \+(\d+): (graded PASS|graded FAIL|NOT GRADABLE|no verdict); the pop nearest "
                 r"the boundary ([+-]\d+)\.\.([+-]\d+) \(walk (\d+)\), least clearance (\d+)")
mine: dict[tuple[str, str, int], tuple] = {}
ctx = None
for ln in open(log, errors="replace"):
    m = VER.match(ln)
    if m:
        h = m[2]
        ctx = (m[1], "asc" if h.startswith("the leg") else "desc" if h == "descending" else "alone")
        continue
    m = WIN.match(ln)
    if m and ctx:
        out = {"graded PASS": "P", "graded FAIL": "F", "NOT GRADABLE": "N"}.get(m[2], "?")
        mine[(ctx[0], ctx[1], int(m[1]))] = (f"{m[3]}..{m[4]}", int(m[5]), int(m[6]), out)
pub: dict[tuple[str, int], tuple] = {}
on = False
for ln in open(md):
    if ln.startswith("## "):
        on = sec in ln
        continue
    if not on or not ln.startswith("| +"):
        continue
    c = [x.strip() for x in ln.strip().strip("|").split("|")]
    phase = int(c[0])
    for i, hist in ((1, "asc"), (5, "desc"), (9, "alone")):
        if c[i]:
            pub[(hist, phase)] = (c[i], int(c[i + 1]), int(c[i + 2]), c[i + 3])
designs = sorted({k[0] for k in mine})
bad = 0
n = 0
for d in designs:
    for (hist, phase), cell in sorted(pub.items()):
        got = mine.get((d, hist, phase))
        n += 1
        exp = cell
        if d != "the unmutated gateware" and cell[3] == "P":
            exp = cell[:3] + ("F",)
        if got != exp:
            bad += 1
            print(f"DIFF {d} {hist} +{phase}: mine {got} published {cell}")
extra = [k for k in mine if (k[1], k[2]) not in pub]
print(f"{sec}: {n} published cells x designs compared, {bad} differ; "
      f"{len(mine)} windows in the log, {len(extra)} not in the table "
      f"({sorted({k[2] for k in extra})})")
print("designs:", designs)
sys.exit(1 if bad else 0)
