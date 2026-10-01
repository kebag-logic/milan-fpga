#!/usr/bin/env python3
"""Render a page with the pinned cmark-gfm and report every table whose body
rows do not all have the header's cell count."""
import sys
import cmarkgfm
from cmarkgfm.cmark import Options
import html5lib

src = open(sys.argv[1], encoding="utf-8").read()
html = cmarkgfm.github_flavored_markdown_to_html(src, options=Options.CMARK_OPT_UNSAFE)
doc = html5lib.parse(html, namespaceHTMLElements=False)
tables = doc.findall(".//table")
bad = 0
rows = 0
for i, t in enumerate(tables):
    head = t.find("./thead/tr")
    n = len(head.findall("./th"))
    for r in t.findall("./tbody/tr"):
        rows += 1
        cells = r.findall("./td")
        empty_tail = sum(1 for c in cells if not "".join(c.itertext()).strip())
        if len(cells) != n:
            bad += 1
            print(f"table {i}: IRREGULAR row with {len(cells)} cells, header {n}")
        elif empty_tail:
            print(f"table {i}: regular row with {empty_tail} empty cell(s): "
                  f"{''.join(cells[0].itertext()).strip()[:40]!r}")
print(f"tables {len(tables)}, body rows {rows}, irregular rows {bad}")
sys.exit(1 if bad else 0)
