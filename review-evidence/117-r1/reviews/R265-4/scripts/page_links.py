#!/usr/bin/env python3
"""Resolve every relative link and fragment in the three pages the PR changes.
usage: page_links.py <repo>   (run at the exact head; reads the working tree)"""
import os, re, sys
repo = sys.argv[1]
os.chdir(repo)
def slug(h):
    h = re.sub(r'[`*_]', '', h.strip().lower())
    return re.sub(r'[^\w\- ]', '', h).replace(' ', '-')
def anchors(path):
    a, inf = set(), False
    for l in open(path, encoding='utf-8'):
        if l.startswith('```'):
            inf = not inf
        if not inf and re.match(r'#{1,6} ', l):
            a.add(slug(re.sub(r'^#+ ', '', l)))
    return a
files = ['docs/findings/117_GPTP_SILICON_EVIDENCE.md', 'docs/design/GM_LOSS_RECOVERY.md', 'docs/findings/README.md']
bad = n = 0
for f in files:
    for m in re.finditer(r'\]\(([^)\s]+)\)', open(f, encoding='utf-8').read()):
        t = m.group(1)
        n += 1
        if t.startswith('http'):
            continue
        p, _, frag = t.partition('#')
        tgt = os.path.normpath(os.path.join(os.path.dirname(f), p)) if p else f
        ok = os.path.exists(tgt) and (not frag or not tgt.endswith('.md') or frag in anchors(tgt))
        if not ok:
            bad += 1
            print('BROKEN', f, t)
print('relative links/anchors checked', n, 'broken', bad)
