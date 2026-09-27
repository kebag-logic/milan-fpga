#!/usr/bin/env python3
"""Render Markdown pages with the repository-pinned cmark-gfm binding and count
tables, and whether the per-cycle header became a table header.
usage: render_tables.py <page.md>..."""
import sys, cmarkgfm
for p in sys.argv[1:]:
    h = cmarkgfm.github_flavored_markdown_to_html(open(p).read())
    print('%s: tables=%d per-cycle-table-rendered=%s' % (p.split('/')[-1], h.count('<table'), '<th>OFF duration</th>' in h))
