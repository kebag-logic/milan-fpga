#!/usr/bin/env python3
"""Verify a published review-evidence subtree against its MANIFEST.json and
its generated INDEX.md files.

usage: verify_evidence.py <evidence-root> <subdir-prefix>
  evidence-root  directory holding MANIFEST.json (review-evidence/pp202-r1)
  subdir-prefix  manifest prefix to check, e.g. author-r5/
Prints one line per mismatch and a summary; exit 0 only when every file
under the prefix is listed, every listed file is present with the published
sha256, and every INDEX.md row (file and sub-INDEX) matches the bytes.
"""
import hashlib, json, os, re, sys

root, prefix = sys.argv[1], sys.argv[2]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


bad = 0
man = {e['file']: e for e in json.load(open(os.path.join(root, 'MANIFEST.json')))}
listed = {k for k in man if k.startswith(prefix)}
present = set()
for d, _, fs in os.walk(os.path.join(root, prefix)):
    for f in fs:
        present.add(os.path.relpath(os.path.join(d, f), root))
for k in sorted(listed - present):
    print('MISSING', k); bad += 1
for k in sorted(present - listed):
    print('UNLISTED', k); bad += 1
nred = 0
for k in sorted(listed & present):
    e = man[k]
    nred += bool(e.get('path_redacted'))
    if sha(os.path.join(root, k)) != e['published_sha256']:
        print('HASH', k); bad += 1
# INDEX.md rows: | name | bytes | sha256 |  and  | dir/ | n | sha256 of INDEX |
nidx = 0
row = re.compile(r'^\|\s*([^|]+?)\s*\|\s*([0-9]+)\s*\|\s*([0-9a-f]{64})\s*\|')
for d, _, fs in os.walk(os.path.join(root, prefix)):
    if 'INDEX.md' not in fs:
        continue
    for line in open(os.path.join(d, 'INDEX.md'), encoding='utf-8'):
        m = row.match(line)
        if not m:
            continue
        name, n, h = m.groups()
        nidx += 1
        if name.endswith('/'):
            p = os.path.join(d, name, 'INDEX.md')
            # the generated count excludes the INDEX.md files themselves
            cnt = sum(len([f for f in x[2] if f != 'INDEX.md'])
                      for x in os.walk(os.path.join(d, name)))
            if not os.path.exists(p) or sha(p) != h or cnt != int(n):
                print('SUBINDEX', os.path.relpath(p, root), cnt, n); bad += 1
        else:
            p = os.path.join(d, name)
            if (not os.path.exists(p) or sha(p) != h
                    or os.path.getsize(p) != int(n)):
                print('INDEXROW', os.path.relpath(p, root)); bad += 1
print(f'prefix={prefix} listed={len(listed)} present={len(present)} '
      f'redacted={nred} index_rows={nidx} mismatches={bad}')
sys.exit(1 if bad else 0)
