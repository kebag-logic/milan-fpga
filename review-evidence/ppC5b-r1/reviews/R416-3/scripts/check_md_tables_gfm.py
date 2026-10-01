#!/usr/bin/env python3
"""GFM table cell check (pipes split cells even inside code spans unless
escaped as \\|). For each markdown file given, report table rows whose cell
count differs from their header row. With --added BASE, only report rows
whose text was added since git revision BASE."""
import re, subprocess, sys
args = sys.argv[1:]
base = None
if args and args[0] == '--added':
    base = args[1]; args = args[2:]
def ncells(l):
    s = l.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|') and not s.endswith('\\|'): s = s[:-1]
    return len(re.split(r'(?<!\\)\|', s))
total = 0
for f in args:
    added = None
    if base:
        d = subprocess.run(['git', 'diff', '-U0', base, '--', f], capture_output=True, text=True).stdout
        added = {l[1:] for l in d.split('\n') if l.startswith('+') and not l.startswith('+++')}
    lines = open(f).read().split('\n')
    hdr = None
    for i, l in enumerate(lines):
        if l.lstrip().startswith('|'):
            if hdr is None:
                hdr = ncells(l); continue
            if re.match(r'^\s*\|[\s:|-]+\|\s*$', l):
                continue
            n = ncells(l)
            if n != hdr and (added is None or l in added):
                total += 1
                print(f'{f}:{i+1}: {n} cells vs header {hdr}: {l[:110]}')
        else:
            hdr = None
print(f'{total} rows off their header')
