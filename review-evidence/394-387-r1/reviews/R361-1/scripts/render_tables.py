"""Render a Markdown page with the repository's pinned GitHub renderer
(cmark-gfm through cmarkgfm, tools/markdown/requirements.txt) and report
every pipe-table block: its header/delimiter cell counts and whether the
renderer produced a <table> containing that header.

Usage: <venv python> -B render_tables.py <page.md>
Exit 1 when a pipe-table block is not rendered as a table.
"""
import re
import sys

import cmarkgfm
from cmarkgfm.cmark import Options

text = open(sys.argv[1], encoding="utf-8").read()
html = cmarkgfm.github_flavored_markdown_to_html(text, options=Options.CMARK_OPT_UNSAFE)
lines = text.splitlines()
bad = 0
for i in range(len(lines) - 1):
    head, delim = lines[i], lines[i + 1]
    if head.startswith("|") and re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", delim.strip()):
        nh = len(head.strip().strip("|").split("|"))
        nd = len(delim.strip().strip("|").split("|"))
        cells = [c.strip() for c in head.strip().strip("|").split("|")]
        first = cells[0]
        # the whole header row, in order, as <th> cells of one rendered row
        pat = r"<tr>\s*" + r"\s*".join(r"<th[^>]*>" + re.escape(c) + r"</th>" for c in cells)
        rendered = re.search(pat, html) is not None
        ok = rendered and nh == nd
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} line {i + 1}: header cells={nh} delimiter cells={nd} rendered-as-table={rendered} first-header={first!r}")
print("table count in HTML:", html.count("<table>"))
print("FAILURES", bad)
sys.exit(1 if bad else 0)
