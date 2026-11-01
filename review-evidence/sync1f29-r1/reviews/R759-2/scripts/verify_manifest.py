#!/usr/bin/env python3
"""Verify author-r2 files against the evidence-branch MANIFEST.json and the packet's SHA256SUMS."""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, 'MANIFEST.json')))
sums = {}
for line in open(os.path.join(root, 'author-r2/evidence/SHA256SUMS')):
    h, n = line.split(None, 1)
    sums[n.strip()] = h
n = bad = red = sum_mismatch_explained = 0
for e in m:
    p = e['file']
    if not p.startswith('author-r2'):
        continue
    n += 1
    d = hashlib.sha256(open(os.path.join(root, p), 'rb').read()).hexdigest()
    if d != e['published_sha256']:
        bad += 1
        print('PUBLISHED-MISMATCH', p)
    if e.get('path_redacted'):
        red += 1
    b = os.path.basename(p)
    if p.startswith('author-r2/evidence/') and b in sums:
        if sums[b] != d:
            ok = sums[b] == e['original_sha256'] and e.get('path_redacted')
            print('SUM-DIFFERS', b, 'explained-by-redaction' if ok else 'UNEXPLAINED')
            sum_mismatch_explained += bool(ok)
print('files', n, 'published-mismatch', bad, 'path_redacted', red, 'sum-differs-explained', sum_mismatch_explained)
