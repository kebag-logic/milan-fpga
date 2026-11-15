#!/usr/bin/env python3
"""Check every author-r6 file in the archive against MANIFEST.json's published_sha256.
Usage: audit_packet.py EVIDENCE_DIR  (the extracted review-evidence/665s11-r1)"""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, 'MANIFEST.json')))
listed = {e['file']: e for e in m if e['file'].startswith('author-r6/')}
bad = 0
for f, e in sorted(listed.items()):
    p = os.path.join(root, f)
    if not os.path.isfile(p):
        print('MISSING', f); bad += 1; continue
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    if h != e['published_sha256']:
        print('MISMATCH', f); bad += 1
on_disk = set()
for d, _, fs in os.walk(os.path.join(root, 'author-r6')):
    for x in fs:
        on_disk.add(os.path.relpath(os.path.join(d, x), root))
extra = on_disk - set(listed)
for x in sorted(extra):
    print('UNLISTED', x); bad += 1
red = sum(1 for e in listed.values() if e.get('path_redacted') or e['original_sha256'] != e['published_sha256'])
print(f'listed {len(listed)} on-disk {len(on_disk)} redacted-or-rewritten {red} bad {bad}')
sys.exit(1 if bad else 0)
