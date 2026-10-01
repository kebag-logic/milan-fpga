#!/usr/bin/env python3
"""Render a Markdown file with cmark-gfm (the GitHub renderer, via cmarkgfm) and
report every table body row that renders irregularly: a cell count unlike the
header's, a literal backtick left in a cell (a code span split by a pipe), or
a literal backslash-pipe. Intentionally empty cells are listed separately.
Usage: table_render.py <markdown-file> [label]"""
import sys, cmarkgfm, html5lib
from cmarkgfm.cmark import Options
src = open(sys.argv[1], encoding="utf-8").read()
html = cmarkgfm.github_flavored_markdown_to_html(src, options=Options.CMARK_OPT_UNSAFE)
doc = html5lib.parse(html, namespaceHTMLElements=False)
bad = 0; ntab = 0; nrow = 0; empty = 0
for t in doc.iter("table"):
    ntab += 1
    rows = list(t.iter("tr"))
    hdr = len([c for c in rows[0] if c.tag in ("th", "td")])
    for r in rows[1:]:
        nrow += 1
        cells = [c for c in r if c.tag in ("th", "td")]
        txt = ["".join(c.itertext()) for c in cells]
        why = []
        if len(cells) != hdr: why.append(f"{len(cells)} cells vs header {hdr}")
        if any("`" in x for x in txt): why.append("literal backtick")
        if any("\\|" in x for x in txt): why.append("literal backslash-pipe")
        if why:
            bad += 1; print(f"IRREGULAR table {ntab}: {'; '.join(why)}: {txt[0][:70]!r}")
        elif any(x.strip() == "" for x in txt):
            empty += 1; print(f"empty-cell (intentional?) table {ntab}: {txt[0][:70]!r}")
lab = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
print(f"{lab}: tables {ntab}, body rows {nrow}, irregular rows {bad}, rows with an empty cell {empty}")
