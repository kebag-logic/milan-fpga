#!/usr/bin/env python3
"""Check the B7 hash tables of the findings page against the published packet.

usage: check_page_hashes.py <page.md> <evidence-root: review-evidence/629-b7-r1 at the pinned commit>
Raw-file rows: against runs/<case>/events.jsonl raw-file records and author/RAW-ARTIFACTS.json.
Evidence-file rows: against MANIFEST.json published_sha256 (and the file bytes), or for a
masked tool against redaction.json original_sha256.
"""
import hashlib, json, os, re, sys
page, root = sys.argv[1], sys.argv[2]
txt = open(page).read()
sec = txt[txt.index('### B7: artifact hashes'):]
rows = re.findall(r'^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$', sec, re.M)
tone = re.search(r'^\| Tone loop \(`b6_tone.py`\) \| ([\d,]+) \| `([0-9a-f]{64})` \|$', sec, re.M)
A = os.path.join(root, 'author')
ev = {}
for case in os.listdir(os.path.join(A, 'runs')):
    p = os.path.join(A, 'runs', case, 'events.jsonl')
    if os.path.isfile(p):
        for l in open(p):
            x = json.loads(l)
            if x.get('kind') == 'raw-file':
                ev[(case, x['file'])] = (x.get('bytes'), x.get('sha256'))
ra = json.load(open(os.path.join(A, 'RAW-ARTIFACTS.json')))
raf = ra['files']
def raw_lookup(name):
    hits = {k: v for k, v in (raf.items() if isinstance(raf, dict) else [(f.get('file') or f.get('path'), f) for f in raf]) if k and k.endswith(name)}
    return hits
man = {e['file']: e for e in json.load(open(os.path.join(root, 'MANIFEST.json')))}
red = json.load(open(os.path.join(A, 'redaction.json')))['files']
bad = 0
n_ev = 0
print('tone row', tone.groups())
for k, v in ev.items():
    if k[1] == 'serve/tone.raw':
        ok = (v[0] == int(tone.group(1).replace(',', '')) and v[1] == tone.group(2))
        print('  tone in', k[0], 'events.jsonl', 'OK' if ok else 'MISMATCH', v); bad += not ok
for name, b, h in rows:
    b = int(b.replace(',', ''))
    if '/' in name and name.split('/')[0] in ('a0', 'a1', 'a2', 'b0', 'bcrf', 'baaf'):
        case, f = name.split('/', 1)
        e = ev.get((case, f))
        hits = raw_lookup(name)
        rav = list(hits.values())
        ra_ok = any((str(h) in json.dumps(x)) and (str(b) in json.dumps(x)) for x in rav)
        if e:
            n_ev += 1
            ok = e == (b, h)
            print(f'RAW  {name:34s} events.jsonl {"OK" if ok else "MISMATCH " + str(e)}  RAW-ARTIFACTS {"OK" if ra_ok else "MISSING/MISMATCH"}')
            bad += (not ok) + (not ra_ok)
        else:
            print(f'RAW  {name:34s} events.jsonl ABSENT  RAW-ARTIFACTS {"OK" if ra_ok else "MISSING/MISMATCH"}')
            bad += not ra_ok
    else:
        key = 'author/' + name
        m = man.get(key)
        path = os.path.join(root, key)
        actual = hashlib.sha256(open(path, 'rb').read()).hexdigest() if os.path.isfile(path) else None
        size = os.path.getsize(path) if os.path.isfile(path) else None
        rd = red.get(name)
        if m and m['published_sha256'] == h:
            src = 'MANIFEST published_sha256'
            ok = actual == h and size == b
        elif rd and rd['original_sha256'] == h:
            src = 'redaction.json original_sha256 (as run)'
            ok = True
        else:
            src = 'NO SOURCE'; ok = False
        extra = ''
        if rd:
            extra = f' [masked: retained {rd["retained_sha256"][:8]}, published {m["published_sha256"][:8] if m else None}, manifest original {m["original_sha256"][:8] if m else None}]'
        print(f'EVID {name:34s} {"OK" if ok else "FAIL"} via {src}; bytes page {b} file {size}{extra}')
        bad += not ok
print('raw rows sourced from events.jsonl:', n_ev, '(+ tone loop row)')
print('RESULT', 'PASS' if bad == 0 else f'FAIL {bad}')
