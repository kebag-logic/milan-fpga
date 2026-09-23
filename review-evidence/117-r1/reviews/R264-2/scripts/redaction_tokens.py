#!/usr/bin/env python3
"""Derive the byte runs a redaction replaced, by aligning each original file
with its published copy, and print a histogram of replaced runs WITHOUT
printing the original bytes: only counts, lengths, a SHA-256 prefix of each
distinct original run, and the published replacement text.

Same-length files are compared byte by byte. Length-changing (text) files
are aligned line by line, then each changed line pair character by character.

usage: redaction_tokens.py ORIG_ROOT PUB_ROOT MANIFEST.json OUT_TOKENS_FILE
OUT_TOKENS_FILE receives the distinct original runs (hex), one per line; it is
kept in a private scratch area and never published.
"""
import sys, json, hashlib, collections, difflib, os

orig_root, pub_root, manifest, out = sys.argv[1:5]
m = json.load(open(manifest))
runs = collections.Counter()
repl = {}
same_len = diff_len = 0


def add(a, b):
    runs[a] += 1
    repl.setdefault(a, set()).add(b)


for e in m:
    if e['original_sha256'] == e['published_sha256']:
        continue
    po, pp = os.path.join(orig_root, e['file']), os.path.join(pub_root, e['file'])
    a, b = open(po, 'rb').read(), open(pp, 'rb').read()
    if hashlib.sha256(a).hexdigest() != e['original_sha256']:
        print('ORIGINAL-UNAVAILABLE', e['file'])
        continue
    if len(a) == len(b):
        same_len += 1
        i, n = 0, len(a)
        while i < n:
            # fast skip over equal stretches
            j = i
            while j < n and a[j] == b[j]:
                j += 1
            if j >= n:
                break
            k = j
            while k < n and a[k] != b[k]:
                k += 1
            add(a[j:k], b[j:k])
            i = k
    else:
        diff_len += 1
        la, lb = a.splitlines(True), b.splitlines(True)
        sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                continue
            xa, xb = b''.join(la[i1:i2]), b''.join(lb[j1:j2])
            cm = difflib.SequenceMatcher(None, xa, xb, autojunk=False)
            for t2, p1, p2, q1, q2 in cm.get_opcodes():
                if t2 != 'equal':
                    add(xa[p1:p2], xb[q1:q2])
print('files same length', same_len, 'different length', diff_len)
print('distinct differing runs', len(runs))
with open(out, 'w') as f:
    for r, n in runs.most_common():
        f.write(r.hex() + '\n')
for i, (r, n) in enumerate(runs.most_common(80), 1):
    rp = sorted(x.decode('latin-1') for x in repl[r])
    print('R%d' % i, 'occurrences', n, 'original length', len(r), '-> published', [x[:40] for x in rp][:3])
