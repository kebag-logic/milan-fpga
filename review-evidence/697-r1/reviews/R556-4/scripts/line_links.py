#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check every relative line link in Markdown; argv[1] = tree root.

A link [text](path#Lnn) must name an existing file and line. When the text is Suite.Case,
line nn must declare that case; otherwise the line must contain the text or the link is listed.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
bad = total = 0
for md in sorted(root.rglob('*.md')):
    if '.git' in md.parts:
        continue
    for text, target, line in re.findall(r'\[([^\]]+)\]\(([^)#:]+)#L(\d+)\)', md.read_text()):
        total += 1
        path = (md.parent / target).resolve()
        lines = path.read_text().splitlines() if path.is_file() else []
        n = int(line)
        ok = 1 <= n <= len(lines)
        if ok and re.fullmatch(r'\w+\.\w+', text):
            ok = re.search(r'\b' + text.split('.')[1] + r'\b', lines[n - 1]) is not None and 'TEST' in lines[n - 1]
        elif ok:
            ok = text.strip('`') in lines[n - 1]
        if not ok:
            bad += 1
            print('UNMATCHED', md.relative_to(root), text, target, n, repr(lines[n - 1][:80]) if 1 <= n <= len(lines) else 'missing')
print(f'line links {total}; unmatched {bad}')
