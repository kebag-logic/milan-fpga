#!/usr/bin/env python3
"""Check every author-r2 file of the published evidence against MANIFEST.json's
published_sha256 and report files present but unlisted. Usage: ROOT (the
review-evidence/pp185-r1 directory)."""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, 'MANIFEST.json')))
listed = {e['file']: e for e in m}
ok = bad = missing = 0
for f, e in listed.items():
    if not f.startswith('author-r2/'):
        continue
    p = os.path.join(root, f)
    if not os.path.exists(p):
        missing += 1; print('MISSING', f); continue
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    if h == e['published_sha256']: ok += 1
    else: bad += 1; print('MISMATCH', f)
unlisted = []
for d, _, fs in os.walk(os.path.join(root, 'author-r2')):
    for x in fs:
        r = os.path.relpath(os.path.join(d, x), root)
        if r not in listed: unlisted.append(r)
for r in unlisted: print('UNLISTED', r)
print(f'author-r2 listed ok={ok} mismatch={bad} missing={missing} unlisted={len(unlisted)}')
sys.exit(1 if (bad or missing) else 0)
