#!/usr/bin/env python3
"""Verify the published receipts against MANIFEST.json, then compare round 1 and round 2 runs row by row.
args: evidence root, clone root."""
import hashlib, json, sys, re
from pathlib import Path
ev = Path(sys.argv[1]); root = Path(sys.argv[2])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_hooks'))
man = {m['file']: m for m in json.load(open(ev / 'MANIFEST.json'))}
bad = n = 0
for p in ev.rglob('*'):
    rel = str(p.relative_to(ev))
    if p.is_file() and rel in man:
        n += 1
        if hashlib.sha256(p.read_bytes()).hexdigest() != man[rel]['published_sha256']:
            bad += 1; print('DIGEST MISMATCH', rel)
print(f'manifest: {len(man)} entries; {n} fetched files checked; {bad} mismatches')
total = same = 0
for run in ('1x1-idle', '1x1-ans', '8x8-idle', '8x8-ans'):
    a = json.load(open(ev / f'author/receipts/runs/{run}/results.json'))
    b = json.load(open(ev / f'author-r2/receipts/runs/{run}/results.json'))
    ra = {(r['group'], r['probe']): r for r in a['rows']}
    rb = {(r['group'], r['probe']): r for r in b['rows']}
    assert len(ra) == len(a['rows']) and len(rb) == len(b['rows'])
    diffs = []
    for k, r in ra.items():
        if k not in rb:
            diffs.append((k, 'MISSING')); continue
        d = {f: (r[f], rb[k].get(f)) for f in r if r[f] != rb[k].get(f)}
        if d: diffs.append((k, d))
    new = sorted(k[1] for k in rb if k not in ra)
    notall = [x for x in new if not re.fullmatch(r'counters\.all\.t\d+\.i\d+\.if0', x)]
    total += len(ra); same += len(ra) - len(diffs)
    print(f'{run}: round1 {len(ra)} rows, round2 {len(rb)} rows, differing {len(diffs)}, new {len(new)}, new not per-descriptor {notall}')
    for d in diffs[:6]: print('   DIFF', d)
    fa = sorted(a['findings']); fb = sorted(x for x in b['findings'] if not re.search(r'counters\.all\.t\d+', x))
    print('   findings equal apart from per-descriptor rows:', fa == fb, len(fa), len(fb), 'refusals', len(a['refusals']), len(b['refusals']),
          'checks equal', a['checks'] == b['checks'])
print(f'TOTAL {total} round-1 rows, {same} identical in every field')
