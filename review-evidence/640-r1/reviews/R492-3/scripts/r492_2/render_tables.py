#!/usr/bin/env python3
"""Render a page with the pinned cmark-gfm and report, per table, the rows
whose source line does not start with a pipe (prose absorbed into a table).
Usage: render_tables.py <page.md>"""
import sys, re
import cmarkgfm
from cmarkgfm.cmark import Options
import html5lib

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
html = cmarkgfm.github_flavored_markdown_to_html(src, options=Options.CMARK_OPT_SOURCEPOS | Options.CMARK_OPT_UNSAFE)
doc = html5lib.parse(html, namespaceHTMLElements=False)
lines = src.split("\n")
bad = 0
ntab = 0
for table in doc.iter("table"):
    ntab += 1
    for tr in table.iter("tr"):
        pos = tr.get("data-sourcepos")
        if not pos:
            continue
        ln = int(pos.split(":")[0])
        text = lines[ln - 1]
        if not text.lstrip().startswith("|"):
            bad += 1
            print(f"{path}:{ln}: prose rendered as a table row: {text!r}")
print(f"{path}: {ntab} tables, {bad} absorbed prose rows")
sys.exit(1 if bad else 0)
