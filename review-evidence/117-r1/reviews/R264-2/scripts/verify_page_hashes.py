#!/usr/bin/env python3
"""Resolve every SHA-256 (full and 8-hex prefix followed by '...') quoted on
the findings page against the published evidence tree at the pinned commit.

usage: verify_page_hashes.py PAGE EVIDENCE_ROOT
EVIDENCE_ROOT is review-evidence/117-r1 extracted from the pinned commit.
Sources consulted, in order: MANIFEST.json (original and published hashes),
the per-packet MANIFEST.sha256 files, identity/expected-crc.txt of each packet,
and bench-a200/bench/tool-revisions.txt. A value found nowhere is reported
UNRESOLVED (it may be defined by an issue comment; checked separately).
"""
import sys, os, re, json, hashlib, collections
page, root = sys.argv[1:3]
text = open(page).read()
lines = text.splitlines()
man = json.load(open(os.path.join(root, 'MANIFEST.json')))
by_orig = collections.defaultdict(list)
by_pub = collections.defaultdict(list)
for e in man:
    by_orig[e['original_sha256']].append(e)
    by_pub[e['published_sha256']].append(e)
msha = {}
for pk in ('bench-a200', 'bench-a202'):
    for ln in open(os.path.join(root, pk, 'MANIFEST.sha256')):
        h, p = ln.split(None, 1)
        msha.setdefault(h, []).append(pk + '/' + p.strip().lstrip('./'))
other = {}
for rel in ('bench-a200/identity/expected-crc.txt', 'bench-a202/identity/expected-crc.txt',
            'bench-a200/bench/tool-revisions.txt'):
    p = os.path.join(root, rel)
    if os.path.exists(p):
        for h in re.findall(r'\b[0-9a-f]{64}\b', open(p).read()):
            other.setdefault(h, set()).add(rel)
allhex = set(by_orig) | set(by_pub) | set(msha) | set(other)


def where(h):
    out = []
    for e in by_orig.get(h, []):
        red = e['original_sha256'] != e['published_sha256']
        pub = os.path.join(root, e['file'])
        ok = hashlib.sha256(open(pub, 'rb').read()).hexdigest() == e['published_sha256']
        out.append('%s %s%s' % (e['file'], 'REDACTED->' + e['published_sha256'][:8] if red else 'as-recorded',
                                '' if ok else ' PUBLISHED-HASH-MISMATCH'))
    for e in by_pub.get(h, []):
        if e['original_sha256'] != h:
            out.append('%s (published copy hash)' % e['file'])
    if not out and h in msha:
        out.append('MANIFEST.sha256 only: ' + ','.join(msha[h]))
    if h in other:
        out.append('listed in ' + ','.join(sorted(other[h])))
    return out


print('== full SHA-256 values on the page')
section = ''
counts = collections.Counter()
for i, ln in enumerate(lines, 1):
    if ln.startswith('#'):
        section = ln.strip('# ')
    for h in re.findall(r'`([0-9a-f]{64})`', ln):
        w = where(h)
        state = 'UNRESOLVED' if not w else ('REDACTED' if any('REDACTED' in x for x in w) else 'RESOLVED')
        counts[(section, state)] += 1
        print('L%d [%s] %s %s: %s' % (i, section[:24], h[:12], state, '; '.join(w) if w else '-'))
print('== 8-hex prefixes followed by ...')
for i, ln in enumerate(lines, 1):
    for p in re.findall(r'`([0-9a-f]{8})\.\.\.`|\(`([0-9a-f]{8})\.\.\.`\)', ln):
        p = p[0] or p[1]
        cands = sorted(h for h in allhex if h.startswith(p))
        desc = []
        for h in cands:
            desc += where(h) or ['(value known only to a manifest)']
        print('L%d %s -> %d match(es): %s' % (i, p, len(cands), '; '.join(desc) if desc else 'UNRESOLVED in archive'))
print('== counts by section/state')
for k, v in sorted(counts.items()):
    print(k, v)
