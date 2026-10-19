#!/usr/bin/env python3
"""Verify a published review-evidence packet.

Usage: python3 -I verify_evidence.py <gptp84-r1 dir>
Checks every MANIFEST.json entry's published_sha256 against the file bytes,
reports unlisted files and redacted entries outside reviews/, and checks
author-r2/receipts/INDEX.md (size and 16-hex SHA-256 prefix per row) against
the files present under that directory.
"""
import hashlib, json, os, re, sys

root = sys.argv[1]
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
man = json.load(open(os.path.join(root, 'MANIFEST.json')))
listed, bad = set(), []
for e in man:
    f = os.path.join(root, e['file']); listed.add(e['file'])
    if not os.path.isfile(f) or sha(f) != e['published_sha256']:
        bad.append(e['file'])
present = {os.path.relpath(os.path.join(r, x), root)
           for r, _, fs in os.walk(root) for x in fs} - {'MANIFEST.json'}
red = [e['file'] for e in man if (e['path_redacted'] or
       e['original_sha256'] != e['published_sha256'])
       and not e['file'].startswith('reviews/')]
print(f"manifest entries {len(man)}; mismatched/missing {len(bad)}; "
      f"unlisted {len(present - listed)}; redacted outside reviews/ {len(red)}")
rec = os.path.join(root, 'author-r2', 'receipts')
rows = {}
for line in open(os.path.join(rec, 'INDEX.md')):
    m = re.match(r'\| `(.+?)` \| (\d+) \| `([0-9a-f]{16})` \|', line)
    if m:
        rows[m.group(1)] = (int(m.group(2)), m.group(3))
files = {os.path.relpath(os.path.join(r, x), rec)
         for r, _, fs in os.walk(rec) for x in fs} - {'INDEX.md'}
wrong = [f for f, (n, h) in rows.items() if f not in files or
         os.path.getsize(os.path.join(rec, f)) != n or
         sha(os.path.join(rec, f))[:16] != h]
print(f"author-r2 INDEX rows {len(rows)}; files {len(files)}; wrong {len(wrong)}; "
      f"unindexed {len(files - set(rows))}; missing {len(set(rows) - files)}")
for p in sorted(os.listdir(os.path.join(root, 'author-r2'))):
    if p.endswith('.patch'):
        print(f"{sha(os.path.join(root, 'author-r2', p))[:16]}  author-r2/{p}")
sys.exit(1 if bad or wrong or (present - listed) or red else 0)
