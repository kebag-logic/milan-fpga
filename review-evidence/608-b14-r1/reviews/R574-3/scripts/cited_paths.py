#!/usr/bin/env python3
"""List backticked packet paths cited in the page and test each against the archive author tree.
usage: cited_paths.py <page.md> <author-dir extracted at archive commit 273764df>
A path containing NNN is tested as a glob over three-digit cycle numbers."""
import glob
import os
import re
import sys

page = open(sys.argv[1]).read()
A = sys.argv[2]
tops = set(os.listdir(A))
cands = set()
for t in re.findall(r'`([^`\s]+)`', page):
    t = t.rstrip('/')
    head = t.split('/')[0]
    if '/' in t and head in tops:
        cands.add(t)
missing = []
for t in sorted(cands):
    p = os.path.join(A, t)
    hit = os.path.exists(p) or bool(glob.glob(p.replace('NNN', '[0-9][0-9][0-9]')))
    print(('OK      ' if hit else 'MISSING ') + t)
    if not hit:
        missing.append(t)
print('cited', len(cands), 'missing', len(missing))
