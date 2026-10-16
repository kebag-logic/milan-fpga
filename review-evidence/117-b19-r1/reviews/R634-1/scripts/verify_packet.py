#!/usr/bin/env python3
"""Verify the published evidence packet against its MANIFEST.json and the
author's MANIFEST.sha256. Usage: verify_packet.py <packet-root>"""
import hashlib, json, os, sys
root = sys.argv[1]
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
m = json.load(open(os.path.join(root, 'MANIFEST.json')))
bad = 0; red = []
listed = set()
for e in m:
    p = os.path.join(root, e['file']); listed.add(e['file'])
    if not os.path.exists(p):
        print('MISSING', e['file']); bad += 1; continue
    if sha(p) != e['published_sha256']:
        print('PUBLISHED-MISMATCH', e['file']); bad += 1
    if e['original_sha256'] != e['published_sha256'] or e.get('path_redacted'):
        red.append(e['file'])
on_disk = set()
for d, _, fs in os.walk(root):
    for f in fs:
        on_disk.add(os.path.relpath(os.path.join(d, f), root))
on_disk.discard('MANIFEST.json')
print('manifest entries', len(m), 'files on disk', len(on_disk))
print('unlisted', sorted(on_disk - listed))
print('redacted/changed entries', len(red))
for r in red: print('  ', r)
# author MANIFEST.sha256
am = os.path.join(root, 'author', 'MANIFEST.sha256')
n = ok = miss = mm = 0
for line in open(am):
    line = line.rstrip('\n')
    if not line: continue
    h, f = line.split(None, 1); f = f.lstrip('*')
    if f.startswith('./'): f = f[2:]
    n += 1
    p = os.path.join(root, 'author', f)
    if not os.path.exists(p): miss += 1; print('ABSENT', f); continue
    if sha(p) == h: ok += 1
    else: mm += 1; print('AUTHOR-MISMATCH', f, ('author/'+f) in red and '(redacted by publisher)' or 'NOT-REDACTED')
print('author MANIFEST.sha256 lines', n, 'match', ok, 'absent from publication', miss, 'mismatch', mm)
print('RESULT', 'FAIL' if bad else 'PASS')
