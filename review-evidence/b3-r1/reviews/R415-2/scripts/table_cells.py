#!/usr/bin/env python3
"""Per table: every source row has the header's cell count (split on
unescaped pipes, as GFM does, code spans included), and cmark-gfm renders the
same number of tables with that column count. A negative control (a row with
one extra cell) must be flagged. usage: table_cells.py <page.md>..."""
import re, sys, cmarkgfm
from cmarkgfm.cmark import Options
def cells(row):
    parts = re.split(r'(?<!\\)\|', row.strip())
    return len(parts) - 2
def check(name, src):
    bad = 0
    blocks, cur = [], []
    for line in src.splitlines():
        if line.startswith('|'): cur.append(line)
        elif cur: blocks.append(cur); cur = []
    if cur: blocks.append(cur)
    html = cmarkgfm.github_flavored_markdown_to_html(src, options=Options.CMARK_OPT_UNSAFE)
    rendered = re.findall(r'<table>(.*?)</table>', html, re.S)
    for i, b in enumerate(blocks):
        want = cells(b[0]); counts = [cells(r) for r in b]
        rh = len(re.findall(r'<th[ >]', rendered[i].split('</thead>')[0])) if i < len(rendered) else -1
        ok = all(c == want for c in counts) and rh == want
        bad += not ok
        print(f'{name} table {i + 1}: {len(b)} source rows, header {want} cells, rows {sorted(set(counts))}, rendered header {rh} {"OK" if ok else "MISMATCH"}')
    ok = len(rendered) == len(blocks); bad += not ok
    print(f'{name}: {len(blocks)} source tables, {len(rendered)} rendered {"OK" if ok else "MISMATCH"}')
    return bad
bad = sum(check(p, open(p).read()) for p in sys.argv[1:])
ctrl = check('negative-control', '| a | b |\n|---|---|\n| 1 | 2 | 3 |\n')
print('negative control flagged' if ctrl else 'NEGATIVE CONTROL NOT FLAGGED')
sys.exit(1 if bad or not ctrl else 0)
