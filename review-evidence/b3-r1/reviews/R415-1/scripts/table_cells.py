#!/usr/bin/env python3
"""Render each page with cmark-gfm (GFM tables) and report, per table, the
source column count and the set of rendered cell counts per row.
usage: table_cells.py <page.md>...   (needs the pinned Markdown environment)"""
import re, sys, cmarkgfm
from cmarkgfm.cmark import Options
bad = 0
for p in sys.argv[1:]:
    src = open(p).read()
    html = cmarkgfm.github_flavored_markdown_to_html(src, options=Options.CMARK_OPT_UNSAFE)
    tables = re.findall(r"<table>(.*?)</table>", html, re.S)
    srct = [b for b in re.split(r"\n(?!\|)", src) if b.lstrip().startswith("|")]
    for i, t in enumerate(tables):
        rows = re.findall(r"<tr>(.*?)</tr>", t, re.S)
        counts = {len(re.findall(r"<t[hd][ >]", r)) for r in rows}
        ok = len(counts) == 1
        bad += not ok
        print(f"{p} table {i + 1}: rows {len(rows)} rendered cells per row {sorted(counts)} {'OK' if ok else 'MISMATCH'}")
    print(f"{p}: {len(tables)} tables rendered")
sys.exit(1 if bad else 0)
