#!/usr/bin/env python3
"""Render a Markdown page with cmark-gfm (tables extension) and check that every
rendered table row has the header's cell count and no cell is empty; also count
source pipe rows per table. Usage: table_cells.py <page.md>"""
import json, sys
import cmarkgfm
from cmarkgfm.cmark import Options
import html5lib
src = open(sys.argv[1], encoding="utf-8").read()
html = cmarkgfm.github_flavored_markdown_to_html(src, options=Options.CMARK_OPT_UNSAFE)
doc = html5lib.parse(html, namespaceHTMLElements=False)
out = []
for i, t in enumerate(doc.iter("table")):
    rows = list(t.iter("tr"))
    counts = [len([c for c in r if c.tag in ("td", "th")]) for r in rows]
    empty = sum(1 for r in rows for c in r if c.tag in ("td", "th") and not "".join(c.itertext()).strip())
    head = "".join(rows[0].itertext()).strip()[:60]
    out.append({"table": i + 1, "header": head, "rows": len(rows), "cells_per_row": sorted(set(counts)), "empty_cells": empty,
                "ok": len(set(counts)) == 1 and empty == 0})
print(json.dumps({"tables": len(out), "all_ok": all(x["ok"] for x in out), "detail": out}, indent=1))
