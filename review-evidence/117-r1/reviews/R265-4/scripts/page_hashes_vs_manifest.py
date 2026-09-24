#!/usr/bin/env python3
"""Resolve every SHA-256 on the #117 findings page against the pinned evidence archive.

usage: page_hashes_vs_manifest.py <page.md> <archive-root: .../review-evidence/117-r1>
Prints, per full 64-hex hash: page line, row label, MANIFEST.json entry (original/published,
redaction flags) and whether the named file's published bytes hash to published_sha256.
Then resolves each abbreviated `xxxxxxxx...` hash against the packets' MANIFEST.sha256 files
and MANIFEST.json originals. Read-only.
"""
import hashlib, json, os, re, sys

page, root = sys.argv[1], sys.argv[2]
man = json.load(open(os.path.join(root, 'MANIFEST.json')))
by_orig = {}
for e in man:
    by_orig.setdefault(e['original_sha256'], []).append(e)
sha_lists = {}
for pk in ('bench-a200', 'bench-a202'):
    for ln in open(os.path.join(root, pk, 'MANIFEST.sha256')):
        ln = ln.rstrip('\n')
        if not ln.strip():
            continue
        h, _, f = ln.partition('  ')
        sha_lists.setdefault(h, []).append(pk + '/' + f.lstrip('*'))

full = re.compile(r'`([0-9a-f]{64})`')
abbr = re.compile(r'`([0-9a-f]{8})\.\.\.`')
n_full = n_red = n_unres = 0
lines = open(page, encoding='utf-8').read().splitlines()
print('== full hashes')
for i, ln in enumerate(lines, 1):
    for h in full.findall(ln):
        n_full += 1
        label = ln.split('|')[1].strip() if ln.startswith('|') else ln[:60]
        ents = by_orig.get(h, [])
        if not ents:
            n_unres += 1
            print(f'{i}\t{h[:12]}\tUNRESOLVED-IN-MANIFEST.json\t{label}')
            continue
        for e in ents:
            p = os.path.join(root, e['file'])
            ok = os.path.exists(p) and hashlib.sha256(open(p, 'rb').read()).hexdigest() == e['published_sha256']
            red = e['original_sha256'] != e['published_sha256']
            n_red += red
            flags = ('REDACTED' if red else 'as-recorded') + (' identity' if e.get('identity_redacted') else '') + (' path' if e.get('path_redacted') else '')
            print(f"{i}\t{h[:12]}\t{e['file']}\t{flags}\tpublished-bytes-ok={ok}\t{label}")
print(f'full hashes: {n_full}; unresolved: {n_unres}; manifest entries matched that are redacted: {n_red}')
print('== abbreviated hashes')
seen = set()
for i, ln in enumerate(lines, 1):
    for a in abbr.findall(ln):
        hits = sorted({f for h, fs in sha_lists.items() if h.startswith(a) for f in fs})
        mj = sorted({e['file'] + (' (REDACTED published)' if e['original_sha256'] != e['published_sha256'] else '') for h, es in by_orig.items() if h.startswith(a) for e in es})
        print(f'{i}\t{a}\tMANIFEST.sha256: {hits or "-"}\tMANIFEST.json: {mj or "-"}')
