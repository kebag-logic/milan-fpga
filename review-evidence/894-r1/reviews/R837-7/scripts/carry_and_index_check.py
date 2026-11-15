#!/usr/bin/env python3
"""Reviewer check over the published evidence archive (review-evidence/894-r1 at 9222da67).

usage: python3 -I carry_and_index_check.py ARCHIVE_DIR
 1. every author-r12/author-r13 file's bytes against MANIFEST.json's published_sha256, and none unlisted;
 2. each packet's INDEX.md rows against the files, a mismatch related to MANIFEST.json's original_sha256;
 3. the two-interface image identity between image-sha256-30a01422.txt and image-sha256-c274b9f5.txt;
 4. harness ELF identity rows.
"""
import collections
import hashlib
import json
import os
import re
import sys

d = sys.argv[1]
os.chdir(d)
man = {e['file']: e for e in json.load(open('MANIFEST.json'))}
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()  # noqa: E731
for pk in ('author-r12', 'author-r13'):
    files = [os.path.join(r, x) for r, _, fs in os.walk(pk) for x in fs]
    bad = [f for f in files if f not in man or man[f]['published_sha256'] != sha(f)]
    print(f'{pk}: {len(files)} files, manifest mismatches or unlisted: {len(bad)} {bad[:5]}')
    rows = re.findall(r'^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|', open(pk + '/INDEX.md').read(), re.M)
    for f, n, h in rows:
        q = os.path.join(pk, f)
        if sha(q) != h:
            e = man.get(q, {})
            rel = 'INDEX == manifest original' if e.get('original_sha256') == h else 'INDEX != manifest original'
            print(f'  INDEX row differs: {q}: {rel}, path_redacted={e.get("path_redacted")}')
    print(f'  INDEX rows {len(rows)}')


def load(f):
    m = {}
    for line in open(f):
        line = line.strip()
        if line and not line.startswith('#'):
            h, p = line.split(None, 1)
            m[p] = h
    return m


im = 'author-r13/receipts/images/'
a, b = load(im + 'image-sha256-30a01422.txt'), load(im + 'image-sha256-c274b9f5.txt')
two = [p for p in a if '2if' in p.split('/')[1]]
diff = sorted(p for p in a if a[p] != b.get(p))
print(f'images: {len(a)} vs {len(b)}, same names {set(a) == set(b)}; two-interface {len(two)}, identical '
      f'{sum(a[p] == b[p] for p in two)}; differing {len(diff)}: '
      f'{sorted(collections.Counter(p.split("/")[1] for p in diff))}')
for line in open(im + 'harness-elf-sha256.txt'):
    if not line.startswith('#'):
        f = line.split()
        print(f'  harness ELF {f[0]}: {f[1] == f[2]} ({f[3]})')
