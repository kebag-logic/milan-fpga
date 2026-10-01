#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Render docs/design/MEDIA_CLOCK_FOLLOWING.md with the pinned GitHub-flavoured
renderer (cmarkgfm from tools/markdown/requirements.txt) and check every table
body row: as many cells as its header, every code span closed inside its cell,
and no stray backtick in a rendered cell. Run with the pinned environment's
interpreter from the lane worktree. Exit 1 on any irregular row."""
import re
import sys

import cmarkgfm
from cmarkgfm.cmark import Options

src = open("docs/design/MEDIA_CLOCK_FOLLOWING.md").read()
html = cmarkgfm.github_flavored_markdown_to_html(
    src, options=Options.CMARK_OPT_UNSAFE)
tables = re.findall(r"<table>(.*?)</table>", html, re.S)
bad = rows = 0
for t in tables:
    head = re.findall(r"<th(?:\s[^>]*)?>", t)
    body = re.findall(r"<tbody>(.*?)</tbody>", t, re.S)
    for row in re.findall(r"<tr>(.*?)</tr>", body[0] if body else "", re.S):
        rows += 1
        cells = re.findall(r"<td(?:\s[^>]*)?>(.*?)</td>", row, re.S)
        txt = [re.sub(r"<[^>]+>", "", c) for c in cells]
        if (len(cells) != len(head)
                or any(c.count("<code>") != c.count("</code>") for c in cells)
                or any("`" in x for x in txt)):
            bad += 1
            print("irregular:", len(cells), "of", len(head),
                  " | ".join(txt)[:150])
print(f"rendered tables {len(tables)}, body rows {rows}, irregular rows {bad}")
sys.exit(1 if bad else 0)
