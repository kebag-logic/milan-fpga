#!/usr/bin/env python3
"""Rewrite a figures-check rows or coverage TSV with findings-page line numbers moved by an offset.

usage: python3 -I norm_lines.py <rows|coverage> <in.tsv> <offset>   (writes to stdout)
rows: column 2 is the line (README rows are 'README.md:<n>' and stay). coverage: column 1 is
'<doc>:<line>' or a bare line; only the findings page's lines move.
"""
import re, sys
kind, path, off = sys.argv[1], sys.argv[2], int(sys.argv[3])
for x in open(path, encoding="utf-8").read().split("\n"):
    if x.startswith("#") or not x:
        print(x); continue
    f = x.split("\t")
    i = 1 if kind == "rows" else 0
    m = re.fullmatch(r"((?:629_MEDIA_CLOCK_FOLLOWING_BENCH\.md:)?)(\d+)", f[i])
    if m:
        f[i] = m.group(1) + str(int(m.group(2)) + off)
    print("\t".join(f))
