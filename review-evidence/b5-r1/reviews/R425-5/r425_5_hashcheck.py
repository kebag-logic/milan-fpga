#!/usr/bin/env python3
"""R425-5: resolve every SHA-256 on the page against the archive at a commit.

Usage: r425_5_hashcheck.py <page.md> <extracted b5-r1 dir> <MANIFEST.json>
Classifies each 64-hex value as a manifest original_sha256 of a path_redacted
file, a manifest published_sha256 (unmasked) file, or a value quoted inside a
published file of author/, author-r2/ or author-r3/. Also lists the
path_redacted files of author/ for comparison with the page's list.
"""
import json, os, re, sys

page, root, man = sys.argv[1:4]
text = open(page, encoding='utf-8').read()
hashes = []
for h in re.findall(r'\b[0-9a-f]{64}\b', text):
    if h not in hashes:
        hashes.append(h)
m = json.load(open(man))
orig = {e['original_sha256']: e for e in m}
pub = {e['published_sha256']: e for e in m}
blobs = {}
for d in ('author', 'author-r2', 'author-r3'):
    for r, _, fs in os.walk(os.path.join(root, d)):
        for f in fs:
            p = os.path.join(r, f)
            try:
                blobs[os.path.relpath(p, root)] = open(p, 'rb').read().decode('utf-8', 'replace')
            except OSError:
                pass
problems = 0
for h in hashes:
    if h in pub and not pub[h]['path_redacted']:
        kind = 'published==original ' + pub[h]['file']
    elif h in orig and orig[h]['path_redacted']:
        kind = 'original_sha256 of path_redacted ' + orig[h]['file']
    else:
        where = [p for p, b in blobs.items() if h in b]
        kind = 'quoted in ' + (', '.join(sorted(where)[:3]) if where else 'NOTHING')
        if not where:
            problems += 1
    print(h[:12], kind)
print(f'{len(hashes)} distinct SHA-256 values on the page, {problems} unresolved')
red = sorted(e['file'] for e in m if e['path_redacted'] and e['file'].split('/')[0] in ('author', 'author-r2', 'author-r3'))
print('path_redacted files in the three directories:')
for f in red:
    print(' ', f)
