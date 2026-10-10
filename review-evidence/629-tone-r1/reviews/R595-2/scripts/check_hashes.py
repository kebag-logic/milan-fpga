#!/usr/bin/env python3
"""Check the B15 doc's hash tables against the published evidence tree.
usage: check_hashes.py <doc.md> <review-evidence/629-tone-r1 dir>"""
import hashlib, json, os, re, sys
doc, ev = sys.argv[1], sys.argv[2]
text = open(doc, encoding='utf-8').read()
sec = text[text.index('### B15: artifact hashes'):]
man = {e['file']: e for e in json.load(open(os.path.join(ev, 'MANIFEST.json')))}
red = json.load(open(os.path.join(ev, 'author/redaction.json')))['files']
raw = json.load(open(os.path.join(ev, 'author/RAW-ARTIFACTS.json')))
rawtxt = json.dumps(raw)
fail = 0
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
# manifest self-consistency
for f, e in man.items():
    p = os.path.join(ev, f)
    if not os.path.exists(p): print('MISSING', f); fail += 1; continue
    h = sha(p)
    if h != e['published_sha256']: print('MANIFEST-MISMATCH', f); fail += 1
    if e['original_sha256'] != e['published_sha256']: print('MASKED', f, 'orig', e['original_sha256'][:12], 'pub', h[:12])
files = set(os.path.relpath(os.path.join(d, n), ev) for d, _, ns in os.walk(ev) for n in ns)
print('files on disk', len(files), 'manifest rows', len(man), 'unlisted', sorted(files - set(man) - {'MANIFEST.json'}))
# evidence rows
for m in re.finditer(r'^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$', sec, re.M):
    name, size, h = m.group(1), int(m.group(2).replace(',', '')), m.group(3)
    p = os.path.join(ev, 'author', name)
    if os.path.exists(p):
        ok = (sha(p) == h and os.path.getsize(p) == size)
        e = man.get('author/' + name, {})
        print('EVID', 'OK' if ok else 'FAIL', name, size, h[:12], 'orig==pub' if e.get('original_sha256') == e.get('published_sha256') else 'orig!=pub',
              'in-redaction.json' if name in red else '')
        fail += not ok
    else:
        inraw = h in rawtxt
        print('RAW', 'OK' if inraw else 'FAIL', name, size, h[:12], 'size-in-raw' if str(size) in rawtxt else 'size-not-in-raw')
        fail += not inraw
print('FAILS', fail)
sys.exit(1 if fail else 0)
