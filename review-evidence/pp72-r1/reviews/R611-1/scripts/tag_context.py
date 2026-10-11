#!/usr/bin/env python3
"""For every REQ_TAG line in a tree's tb/, report the previous non-tag code line
and flag placements where an inserted statement could change control flow:
the previous line opens an unbraced if/else/for/while/do body, or the tag is
not followed by a check within 8 lines. Usage: tag_context.py TREE"""
import re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
files = subprocess.run(["git", "-C", str(root), "ls-files", "tb"], capture_output=True,
                       text=True, check=True).stdout.split()
TAG = re.compile(r'^\s*REQ_TAG\(')
CTRL = re.compile(r'^\s*(\}?\s*else\b.*|(if|for|while)\s*\(.*\)\s*|do\s*)$')
n = flagged = 0
for f in files:
    if not f.endswith(('.cpp', '.hpp', '.h', '.py')) or f.startswith('tb/common/'):
        continue
    lines = (root / f).read_text(encoding='utf-8', errors='replace').splitlines()
    for i, l in enumerate(lines):
        if not TAG.match(l):
            continue
        n += 1
        j = i - 1
        while j >= 0 and (TAG.match(lines[j]) or not lines[j].strip()
                         or lines[j].strip().startswith(('//', '/*', '*', '#'))):
            j -= 1
        prev = lines[j].rstrip() if j >= 0 else ''
        k = i + 1
        while k < len(lines) and TAG.match(lines[k]):
            k += 1
        nxt = lines[k].strip() if k < len(lines) else ''
        bad = bool(CTRL.match(prev)) or (prev.rstrip().endswith(')') and not prev.strip().startswith(('//', '*'))
                                         and re.search(r'\b(if|for|while)\b', prev) and '{' not in prev)
        if f.endswith('.py'):
            bad = not prev.strip().startswith(('def ', '"""')) and not prev.strip().endswith('"""')
        if bad:
            flagged += 1
        print(f"{'FLAG ' if bad else 'ok   '}{f}:{i+1} | prev: {prev.strip()[:90]} | next: {nxt[:80]}")
print(f"tags {n}, flagged {flagged}")
