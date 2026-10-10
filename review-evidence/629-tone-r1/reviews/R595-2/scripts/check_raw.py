#!/usr/bin/env python3
"""Check the B15 doc's raw-artifact rows against RAW-ARTIFACTS.json.
usage: check_raw.py <doc.md> <review-evidence/629-tone-r1 dir>"""
import json, os, re, sys
doc, ev = sys.argv[1], sys.argv[2]
sec = open(doc, encoding='utf-8').read()
i0 = sec.index('### B15: artifact hashes'); sec = sec[i0:sec.index('**Where the packet is.**', i0)]
raw = json.load(open(os.path.join(ev, 'author/RAW-ARTIFACTS.json')))
ents = raw if isinstance(raw, list) else raw.get('artifacts', raw.get('files', raw))
flat = json.dumps(raw)
fail = 0
for m in re.finditer(r'^\| ([^|]+) \| `([^`]+)`[^|]*\| ([^|]+) \| `([0-9a-f]{64})` \|$', sec, re.M):
    run, name, size, h = m.group(1).strip(), m.group(2), m.group(3).strip(), m.group(4)
    hit = [e for e in (ents.values() if isinstance(ents, dict) else ents) if isinstance(e, dict) and h in json.dumps(e)]
    sz = None
    if hit:
        e = hit[0]; sz = e.get('bytes', e.get('size'))
    ok = bool(hit) and (size == 'Withheld' or str(sz) == size.replace(',', ''))
    print('RAW', 'OK' if ok else 'FAIL', run, name, size, h[:12], 'raw-entry:', json.dumps(hit[0])[:200] if hit else None)
    fail += not ok
print('FAILS', fail); sys.exit(1 if fail else 0)
