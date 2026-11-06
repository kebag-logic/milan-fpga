#!/usr/bin/env python3
"""The comment rule and the em-dash rule over the added lines of a diff, with a positive control.
Usage: comment_scan.py <diff-file> [<diff-file> ...]"""
import re, sys
LABEL = re.compile(r'\b(S\d+[a-z]?|F\d(?:-F\d)?|B\d{1,2}|[AR]\d{2,}[a-z]?(?:-\d+)?|[Rr]ound \d+|issuecomment[-\d]*|lane)\b')
assert LABEL.search("S2's groups") and LABEL.search('the F2-F5 timing') and LABEL.search('R783-1') and LABEL.search('issuecomment-6677495623'), 'control'
for name in sys.argv[1:]:
    path = None; added = py = 0; hits = []; dash = []
    for line in open(name, encoding='utf-8'):
        if line.startswith('+++ '):
            path = line[6:].strip(); continue
        if not line.startswith('+') or line.startswith('+++'):
            continue
        added += 1
        if '—' in line:
            dash.append((path, line[:80]))
        if path.endswith('.py'):
            py += 1
            for m in LABEL.finditer(line):
                hits.append((path.rsplit('/', 1)[-1], m.group(0), line[1:].strip()[:110]))
    print(f'{name.rsplit("/", 1)[-1]}: added lines {added}, of .py {py}, label matches {len(hits)}, U+2014 lines {len(dash)}')
    for h in hits: print('   ', h)
    for d in dash: print('    DASH', d)
