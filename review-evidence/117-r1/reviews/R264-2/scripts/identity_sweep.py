#!/usr/bin/env python3
"""Sweep a published evidence tree (and optional extra trees) for the exact
strings a redaction removed, in raw, hex (both cases) and UTF-16LE forms, and
for the repository's own scrub rules. Prints classes, file paths and counts
only; never the matched text.

usage: identity_sweep.py REPO_ROOT ORIG_ROOT PUB_ROOT [EXTRA_ROOT ...]

Tokens are taken from the ORIGINAL copies of files the published tree changed:
for each line pair that differs, the original's differing span is recovered
at the placeholder boundary (text) or as the run replaced by '#' (binary).
"""
import sys, os, re, difflib, hashlib, collections, json

repo, orig_root, pub_root = sys.argv[1:4]
extra = sys.argv[4:]
sys.dont_write_bytecode = True  # never write into the reviewed clone
sys.path.insert(0, os.path.join(repo, 'scripts'))
import docs_check  # noqa: E402  (the reviewed head's own rule table)

PLACE = re.compile(rb'<(bench-host-prefix|MAC-derived-interface|bench-switch-vendor-name|'
                   rb'peer-product-name|device-serial|home|local-path|[a-z-]+)>')


def files(root):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            yield os.path.relpath(p, root), p


tokens = {}  # bytes -> class
for rel, po in files(orig_root):
    pp = os.path.join(pub_root, rel)
    if not os.path.exists(pp):
        continue
    a, b = open(po, 'rb').read(), open(pp, 'rb').read()
    if a == b:
        continue
    if len(a) == len(b):
        n, i = len(a), 0
        while i < n:
            j = i
            while j < n and a[j] == b[j]:
                j += 1
            if j >= n:
                break
            k = j
            while k < n and a[k] != b[k]:
                k += 1
            # widen to the whole '#' run in the published copy
            s, e = j, k
            while s > 0 and b[s - 1:s] == b'#' and a[s - 1] != b[s - 1]:
                s -= 1
            while e < n and b[e:e + 1] == b'#' and a[e] != b[e]:
                e += 1
            tok = a[s:e]
            if len(tok) >= 3:
                tokens.setdefault(tok, 'binary-run:' + rel.split('/')[-1].split('.')[-1])
            i = k
        continue
    la, lb = a.splitlines(), b.splitlines()
    sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'replace' or (i2 - i1) != (j2 - j1):
            continue
        for x, y in zip(la[i1:i2], lb[j1:j2]):
            # split the published line at placeholders; the literal pieces
            # between them anchor the original line, the gaps are the tokens
            parts = PLACE.split(y)
            lits = parts[0::2]
            names = parts[1::2]
            pat = b'(.*?)'.join(re.escape(l) for l in lits)
            mm = re.fullmatch(pat, x, re.S)
            if not mm:
                continue
            for name, g in zip(names, mm.groups()):
                g = g.strip()
                if len(g) >= 2:
                    tokens.setdefault(g, name.decode())

cls = collections.Counter(tokens.values())
# neutral, stable token ids; the token text and its hash are never printed
ids = {t: 'T%d' % i for i, t in enumerate(sorted(tokens, key=lambda t: (tokens[t], len(t), hashlib.sha256(t).digest())), 1)}
print('distinct redacted tokens recovered:', len(tokens))
for c, n in sorted(cls.items()):
    print('  class', c, n)
for t in sorted(tokens, key=lambda t: ids[t]):
    print('  %s class %s length %d' % (ids[t], tokens[t], len(t)))


def forms(t):
    out = [(t, 'raw')]
    out.append((t.hex().encode(), 'hex-lower'))
    out.append((t.hex().upper().encode(), 'hex-upper'))
    out.append((t.decode('latin-1').encode('utf-16-le'), 'utf16le'))
    return out


def sweep(root, label):
    hits = collections.Counter()
    where = collections.defaultdict(set)
    for rel, p in files(root):
        if '/.git/' in p or p.endswith('/.git'):
            continue
        data = open(p, 'rb').read()
        low = data.lower()
        for t, c in tokens.items():
            for f, fname in forms(t):
                # exact case for raw text (a lowercased match of a short token
                # is a coincidence, not a leak); hex compared case-insensitively
                if fname == 'raw':
                    ff, hay = f, data
                elif fname == 'utf16le':
                    ff, hay = f, data
                else:
                    ff, hay = f.lower(), low
                if ff in hay:
                    hits[(ids[t] + ' ' + c, fname)] += 1
                    where[(ids[t] + ' ' + c, fname)].add(rel)
        # path names
        for t, c in tokens.items():
            if t.lower() in rel.encode().lower():
                hits[(ids[t] + ' ' + c, 'path')] += 1
                where[(ids[t] + ' ' + c, 'path')].add(rel)
        # the repository's own scrub rules over the decoded bytes
        text = data.decode('latin-1')
        for rx, klass, _fix in docs_check.SCRUB_RULES:
            if rx.search(text):
                hits[('scrub:' + klass, 'rule')] += 1
                where[('scrub:' + klass, 'rule')].add(rel)
    print('==', label, root)
    if not hits:
        print('  no hit')
    for k in sorted(hits):
        print('  HIT', k[0], k[1], 'files', len(where[k]))
        for r in sorted(where[k])[:40]:
            print('     ', r)


sweep(pub_root, 'published')
for r in extra:
    sweep(r, 'extra')
