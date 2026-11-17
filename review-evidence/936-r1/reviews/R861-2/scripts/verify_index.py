#!/usr/bin/env python3
"""Verify every `path | bytes | sha256` row of a markdown index against files beside it.
Usage: verify_index.py <index.md>  (paths in the index are relative to its directory)"""
import hashlib, os, re, sys
idx = sys.argv[1]; base = os.path.dirname(os.path.abspath(idx))
row = re.compile(r'^\|\s*`?\[?([^\]|]+?)\]?(?:\([^)]*\))?\s*\|\s*(\d+)\s*\|\s*`?([0-9a-f]{16,64})`?\s*\|')
ok = bad = 0; listed = set()
for line in open(idx, encoding='utf-8'):
    m = row.match(line)
    if not m: continue
    p, n, h = m.group(1).strip().strip('`'), int(m.group(2)), m.group(3)
    f = os.path.join(base, p); listed.add(os.path.normpath(f))
    try: b = open(f, 'rb').read()
    except OSError: print('MISSING', p); bad += 1; continue
    if len(b) == n and hashlib.sha256(b).hexdigest().startswith(h): ok += 1
    else: print('MISMATCH', p, len(b), n); bad += 1
unlisted = [os.path.relpath(os.path.join(d, x), base) for d, _, fs in os.walk(base) for x in fs
            if os.path.normpath(os.path.join(d, x)) not in listed and os.path.normpath(os.path.join(d, x)) != os.path.normpath(os.path.abspath(idx))]
print(f'{idx}: ok={ok} bad={bad} unlisted={len(unlisted)}')
for u in unlisted[:20]: print('UNLISTED', u)
sys.exit(1 if bad else 0)
