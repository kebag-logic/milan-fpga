#!/usr/bin/env python3
"""Every Markdown table row carries the header's cell count (GFM splitting).

Usage: check_table_cells.py FILE...   (exit 1 on any mismatch)
Splits on unescaped '|' as GFM does (pipes inside code spans still split
unless escaped), so a row whose source count differs from its header would
lose or pad cells when rendered.
"""
import re
import sys


def cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return len(re.split(r"(?<!\\)\|", s))


bad = 0
for path in sys.argv[1:]:
    lines = open(path, encoding="utf-8").read().splitlines()
    tables = 0
    i = 0
    in_fence = False
    while i < len(lines):
        l = lines[i]
        if l.lstrip().startswith("```"):
            in_fence = not in_fence
        if (not in_fence and l.lstrip().startswith("|") and i + 1 < len(lines)
                and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1])):
            tables += 1
            n = cells(l)
            if cells(lines[i + 1]) != n:
                print(f"FAIL {path}:{i + 2} delimiter {cells(lines[i + 1])} != header {n}")
                bad += 1
            j = i + 2
            rows = 0
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                if cells(lines[j]) != n:
                    print(f"FAIL {path}:{j + 1} row has {cells(lines[j])} cells, header {n}")
                    bad += 1
                rows += 1
                j += 1
            print(f"INFO {path}:{i + 1} table cols={n} rows={rows}")
            i = j
            continue
        i += 1
    print(f"{'PASS' if not bad else 'FAIL'} {path}: {tables} table(s)")
sys.exit(1 if bad else 0)
