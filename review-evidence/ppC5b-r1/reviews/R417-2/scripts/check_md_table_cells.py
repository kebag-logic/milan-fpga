#!/usr/bin/env python3
"""R417-2 probe: report GFM table rows whose cell count differs from their
header row. GFM tables extension: a row with more cells than the header has
the excess ignored, so a stray `|` drops the last column's content on render.
Pipes inside backtick code spans and escaped pipes are not separators.
Usage: check_md_table_cells.py FILE..."""
import re
import sys


def cells(line: str) -> int:
    s = re.sub(r"`[^`]*`", "C", line.strip())
    s = s.replace("\\|", "E")
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return len(s.split("|"))


bad = 0
for path in sys.argv[1:]:
    lines = open(path, encoding="utf-8").read().splitlines()
    head = None
    for n, line in enumerate(lines, 1):
        t = line.strip()
        if not t.startswith("|"):
            head = None
            continue
        if head is None:
            head = cells(t)
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?", t):
            continue
        c = cells(t)
        if c != head:
            bad += 1
            print(f"{path}:{n}: {c} cells, header has {head}: {t[:90]}...")
print(f"table rows off their header's cell count: {bad}")
