#!/usr/bin/env python3
"""Verify every `| file | bytes | sha256 |` row of a receipts INDEX.md against the files beside it,
and list files present but not indexed. Usage: python3 -I verify_receipt_index.py <receipts-dir>"""
import hashlib, os, re, sys
root = sys.argv[1]
rows = re.findall(r'^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$', open(os.path.join(root, 'INDEX.md')).read(), re.M)
bad = 0
for name, size, digest in rows:
    p = os.path.join(root, name)
    if not os.path.isfile(p):
        print('MISSING', name); bad += 1; continue
    b = open(p, 'rb').read()
    if len(b) != int(size) or hashlib.sha256(b).hexdigest() != digest:
        print('MISMATCH', name); bad += 1
present = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs} - {'INDEX.md'}
unindexed = sorted(present - {r[0] for r in rows})
print('indexed rows', len(rows), 'bad', bad, 'unindexed', len(unindexed), unindexed[:10])
