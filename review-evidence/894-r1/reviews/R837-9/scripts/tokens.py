#!/usr/bin/env python3
"""Superseded 1x1/1if row figures: every numeric cell of section 13's
rows-history table (docs/design/SPLIT_CONTROL_MEMORY.md, the table headed
'| Head | R4 (20) | R4L') whose value differs from the head row's cell in
the same column, plus the 800 us/merge tiers table figures in the
paragraph after the tiers table.  Usage: tokens.py <repo>"""
import re, sys, pathlib
doc = pathlib.Path(sys.argv[1], "docs/design/SPLIT_CONTROL_MEMORY.md").read_text().splitlines()
start = next(i for i, l in enumerate(doc) if l.startswith("| Head | R4 (20) | R4L"))
rows = []
for l in doc[start + 2:]:
    if not l.startswith("|"):
        break
    rows.append([c.strip() for c in l.strip("|").split("|")])
num = re.compile(r"\d+\.\d+")
head = rows[-1]
headv = [set(num.findall(c)) for c in head]
out = set()
for r in rows[:-1]:
    for j, c in enumerate(r[1:], 1):
        for v in num.findall(c):
            if v not in headv[j]:
                out.add(v)
for v in sorted(out, key=float):
    print(v)
print("# head row:", " ".join(sorted({v for s in headv for v in s}, key=float)), file=sys.stderr)
