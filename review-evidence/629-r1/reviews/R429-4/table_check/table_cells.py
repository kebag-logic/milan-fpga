#!/usr/bin/env python3
"""Render a Markdown file with the pinned GFM renderer (tables) and report every
table row whose cell count differs from its header's, and any cell that
contains a literal '|' character after rendering. Usage: table_cells.py FILE"""
import sys
import cmarkgfm
from cmarkgfm.cmark import Options
import html5lib

src = open(sys.argv[1], encoding='utf-8').read()
html = cmarkgfm.github_flavored_markdown_to_html(src, options=Options.CMARK_OPT_UNSAFE)
doc = html5lib.parse(html, namespaceHTMLElements=False)
bad = 0
ntab = 0
nrow = 0
pipes = 0
for t, tbl in enumerate(doc.iter('table')):
    ntab += 1
    rows = list(tbl.iter('tr'))
    hdr = len(list(rows[0]))
    for i, r in enumerate(rows[1:], 1):
        nrow += 1
        cells = [c for c in r if c.tag in ('td', 'th')]
        txt = [''.join(c.itertext()) for c in cells]
        empty_tail = sum(1 for x in txt if x.strip() == '')
        if len(cells) != hdr:
            bad += 1
            print(f'table {t} row {i}: {len(cells)} cells vs header {hdr}: {txt[0][:60]!r}')
        for x in txt:
            if '`' in x:
                bad += 1
                print(f'table {t} row {i}: stray backtick (a broken code span): {x[:80]!r}')
            if '|' in x:
                pipes += 1
                print(f'table {t} row {i}: literal pipe in cell: {x[:80]!r}')
# source side: unescaped pipes per table row against the header row
import re
lines = src.split('\n')
src_bad = []
hdr_n = None
for n, ln in enumerate(lines, 1):
    if ln.startswith('|'):
        c = len(re.findall(r'(?<!\\)\|', ln))
        if hdr_n is None:
            hdr_n = c
        elif c != hdr_n:
            src_bad.append(n)
    else:
        hdr_n = None
print(f'source rows whose unescaped-pipe count differs from their header: {src_bad}')
print(f'tables={ntab} body_rows={nrow} rows_with_wrong_cell_count_or_stray_backtick={bad} cells_with_literal_pipe={pipes}')
