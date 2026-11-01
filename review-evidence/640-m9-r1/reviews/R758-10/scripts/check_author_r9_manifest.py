#!/usr/bin/env python3
"""Usage: check_author_r9_manifest.py <review-evidence/640-m9-r1 dir>. Reconciles author-r9 files, SHA256SUMS and MANIFEST.json."""
import hashlib, json, os, sys
os.chdir(sys.argv[1])
rows = {e['file']: e for e in json.load(open('MANIFEST.json'))}
sums = {}
for line in open('author-r9/evidence/SHA256SUMS'):
    digest, name = line.split(None, 1)
    sums['author-r9/evidence/' + name.strip().removeprefix('./')] = digest
actual = {}
for d, _, files in os.walk('author-r9'):
    for f in files:
        p = os.path.join(d, f)
        actual[p] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
print('published files', len(actual), 'absent from manifest', [p for p in actual if p not in rows])
print('published digest differs from manifest', [p for p in actual if p in rows and rows[p]['published_sha256'] != actual[p]])
print('SHA256SUMS rows', len(sums), 'differ from manifest original', [p for p, h in sums.items() if p in rows and rows[p]['original_sha256'] != h])
differ = [p for p, h in sums.items() if actual.get(p) != h]
print('published files differing from SHA256SUMS', len(differ), 'not flagged path_redacted', [p for p in differ if not rows.get(p, {}).get('path_redacted')])
print('rc files', sum(p.endswith('.rc') for p in actual), 'nonzero', [p for p in actual if p.endswith('.rc') and open(p).read().strip() != '0'])
