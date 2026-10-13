#!/usr/bin/env python3
"""Probe only: copy check_b16_figures.py with every findings-page row line moved by a fixed offset.

usage: python3 -I shift_rows.py <check_b16_figures.py> <out copy> <offset>

Rows of README.md ("README.md:<n>") are left alone; only rows whose line field is a bare integer, inside the
ROWS-BEGIN/ROWS-END block, move. Nothing else in the check changes. Prints the count of rows moved and any
other bare 4-digit integer outside the block, so a reader can see no other line constant was missed.
"""
import re
import sys

src, dst, off = sys.argv[1], sys.argv[2], int(sys.argv[3])
lines = open(src, encoding="utf-8").read().split("\n")
b = lines.index("# ROWS-BEGIN")
e = lines.index("# ROWS-END")
moved = 0
for i in range(b + 1, e):
    m = re.match(r"^(\d+)\t", lines[i])
    if m:
        lines[i] = str(int(m.group(1)) + off) + lines[i][m.end(1):]
        moved += 1
others = [(i + 1, x) for i, x in enumerate(lines) if not (b <= i <= e) and not x.lstrip().startswith("#")
          and re.search(r"(?<![\w.:])(2[2-9]\d\d|[34]\d\d\d)(?![\w.:])", x)]
open(dst, "w", encoding="utf-8").write("\n".join(lines))
print(f"rows moved: {moved}; offset {off}")
print(f"other 4-digit constants outside the rows block: {len(others)}")
for n, x in others:
    print(f"  {n}: {x.strip()[:160]}")
