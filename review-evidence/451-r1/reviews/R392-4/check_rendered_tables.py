#!/usr/bin/env python3
"""Render with GFM (cmarkgfm) and check each table's rows and cell counts,
plus that the merged rows render their links.

Usage: check_rendered_tables.py REPO   (run with the pinned Markdown python)
"""
import re
import sys

import cmarkgfm
from cmarkgfm.cmark import Options

REPO = sys.argv[1]
FILES = ["docs/reference/MILAN_COMPLIANCE_MATRIX.md", "docs/findings/README.md",
         "docs/litex/CLOCK_DOMAINS.md", "docs/findings/451_TDM8_FIRST_LIGHT.md"]
bad = 0
html = {}
for f in FILES:
    h = cmarkgfm.github_flavored_markdown_to_html(
        open(f"{REPO}/{f}", encoding="utf-8").read(), options=Options.CMARK_OPT_UNSAFE)
    html[f] = h
    tables = re.findall(r"<table>(.*?)</table>", h, re.S)
    for t_i, t in enumerate(tables):
        counts = [len(re.findall(r"<t[hd][ >]", tr)) for tr in re.findall(r"<tr>(.*?)</tr>", t, re.S)]
        ok = len(set(counts)) == 1
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'} {f} rendered table {t_i + 1}: rows={len(counts)} cells={sorted(set(counts))}")


def row_html(f, key):
    for tr in re.findall(r"<tr>(.*?)</tr>", html[f], re.S):
        first = re.search(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if first and first.group(1).strip() == key:
            return tr
    return ""


checks = [
    ("docs/reference/MILAN_COMPLIANCE_MATRIX.md", "4.4.4.3", 'href="https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355"'),
    ("docs/reference/MILAN_COMPLIANCE_MATRIX.md", "4.4.4.5 / .9", 'href="../findings/451_TDM8_FIRST_LIGHT.md"'),
    ("docs/reference/MILAN_COMPLIANCE_MATRIX.md", "5.4.2.15 / .16", 'issues/602#issuecomment-5859297355'),
    ("docs/reference/MILAN_COMPLIANCE_MATRIX.md", "5.3.11.1", 'issues/602#issuecomment-5859297355'),
    ("docs/reference/MILAN_COMPLIANCE_MATRIX.md", "7.4.42.2", 'issues/599'),
]
for f, key, needle in checks:
    ok = needle in row_html(f, key)
    bad += not ok
    print(f"{'PASS' if ok else 'FAIL'} rendered row {key} carries {needle}")
idx = html["docs/findings/README.md"]
order = re.findall(r'<tr>\s*<td><a href="([^"]+)"', idx)
print("INFO rendered index order: " + ", ".join(order))
ok = order[0] == "451_TDM8_FIRST_LIGHT.md" and len(order) == len(set(order)) == 10
bad += not ok
print(f"{'PASS' if ok else 'FAIL'} rendered index: #451 first, 10 unique rows")
sys.exit(1 if bad else 0)
