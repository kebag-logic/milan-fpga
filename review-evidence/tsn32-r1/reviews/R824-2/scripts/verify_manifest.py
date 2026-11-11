#!/usr/bin/env python3
"""Check every entry of the published evidence MANIFEST.json against the archive's bytes.
Usage: verify_manifest.py <evidence-root>  (the directory holding MANIFEST.json)"""
import hashlib, json, os, sys
root = sys.argv[1]
entries = json.load(open(os.path.join(root, 'MANIFEST.json')))
listed = set(); bad = 0; per = {}
for e in entries:
    p = os.path.join(root, e['file']); listed.add(e['file'])
    top = e['file'].split('/')[0]; per[top] = per.get(top, 0) + 1
    try:
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    except OSError as x:
        print('MISSING', e['file'], x); bad += 1; continue
    if h != e['published_sha256']:
        print('MISMATCH', e['file']); bad += 1
unlisted = []
for d, _, fs in os.walk(root):
    for f in fs:
        rel = os.path.relpath(os.path.join(d, f), root)
        if rel != 'MANIFEST.json' and rel not in listed:
            unlisted.append(rel)
print('entries', len(entries), 'by top dir', per)
print('mismatch_or_missing', bad)
print('unlisted', len(unlisted), unlisted[:20])
print('redacted', sum(1 for e in entries if e.get('path_redacted')),
      'original!=published', sum(1 for e in entries if e['original_sha256'] != e['published_sha256']))
sys.exit(1 if bad else 0)
