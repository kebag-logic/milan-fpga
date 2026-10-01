#!/usr/bin/env python3
"""Render Markdown pages with cmark-gfm (pinned) and report each table's
header cell count and the set of body-row cell counts. usage: table_cells.py <md>..."""
import sys
import cmarkgfm
import html5lib
for p in sys.argv[1:]:
    html = cmarkgfm.github_flavored_markdown_to_html(open(p, encoding="utf-8").read())
    doc = html5lib.parse(html, namespaceHTMLElements=False)
    for i, t in enumerate(doc.iter("table")):
        rows = [len([c for c in tr if c.tag in ("td", "th")]) for tr in t.iter("tr")]
        print(p, "table", i + 1, "header", rows[0], "body", sorted(set(rows[1:])), "rows", len(rows) - 1,
              "OK" if set(rows[1:]) <= {rows[0]} else "MISMATCH")
