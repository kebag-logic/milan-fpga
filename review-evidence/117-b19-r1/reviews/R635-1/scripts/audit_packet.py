#!/usr/bin/env python3
"""Offline checks of the pinned public packet. Prints no private identities.

Usage: python3 audit_packet.py PACKET_ROOT SOURCE_ROOT
PACKET_ROOT contains MANIFEST.json and author/.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

packet, source = map(Path, sys.argv[1:])
author = packet / 'author'
def read(path):
    return json.loads(path.read_text())
def bracket(lo, hi, event):
    return lo <= event <= hi

assert bracket(1, 2, 1) and bracket(1, 2, 2)
assert not bracket(1, 2, .99) and not bracket(1, 2, 2.01)
print('Bracket boundary and outside controls: PASS')
manifest = read(packet / 'MANIFEST.json')
bad = [x['file'] for x in manifest
       if hashlib.sha256((packet / x['file']).read_bytes()).hexdigest() != x['published_sha256']]
print('Published manifest:', len(manifest), 'files;', len(bad), 'hash failures')
assert not bad
raw = read(author / 'RAW-ARTIFACTS.json')
print('Raw-index structure:', type(raw).__name__)
for part in ('identity', 'identity-end'):
    text = (author / part / 'identity-verdict.txt').read_text()
    rows = [json.loads(s) for s in text.splitlines() if s.startswith('{')]
    assert len(rows) == 11 and all(r['result'] == 'PASS' for r in rows)
    print(part, '11/11 PASS; terminal PASS present:', 'IDENTITY GATE: PASS' in text)
power = []
for path in sorted((author / 'bench').glob('*/events.jsonl')):
    events = [json.loads(s) for s in path.read_text().splitlines()]
    cmds = [e for e in events if e['kind'] == 'power-command']
    if cmds:
        assert len(cmds) == 2 and [e['value'] for e in cmds] == ['off', 'on']
        power.append((path.parent.name, cmds[0]['outlet']))
print('Power cycles:', power)
assert sum(v == 0 for _, v in power) == 1
assert sum(v == 4 for _, v in power) == 6

for i in range(1, 7):
    c = read(author / f'bench/cycle{i:02}/correlation.json')
    e, w = c['edges'], c['wire']
    recovery = e['tu'][-1]['first_after'] - w['switch_announces_after_return'][0][0]
    print(f'Cycle {i}: recovery={recovery:.4f}s; bound_5s={recovery <= 5}')
    for name, key, timeout in [('sync', 'switch_last_sync', .375),
                                ('gm', 'switch_last_announce', 3),
                                ('asCapable', 'switch_last_pdelay_resp', 5)]:
        b = e[name][0]
        cause = w[key] + timeout
        print(f'  {name} loss bracket=[{b["last_before"]:.4f},{b["first_after"]:.4f}] '
              f'timeout={cause:.4f} inside={bracket(b["last_before"], b["first_after"], cause)}')
    b = e['gm'][-1]
    eligible = [r[0] for r in w['switch_announces_after_return']
                if r[0] >= e['asCapable'][-1]['last_before'] and r[0] <= b['first_after']]
    cause = eligible[-1]
    print(f'  GM return bracket=[{b["last_before"]:.4f},{b["first_after"]:.4f}] '
          f'Announce={cause:.4f}; inside={bracket(b["last_before"], b["first_after"], cause)}; '
          f'first_sample_minus_cause={b["first_after"]-cause:.4f}s')
    if i <= 3:
        rise = [x for x in c['crf_tu_vs_csr'] if x['wire']['to'] == 1]
        assert len(rise) == 1 and rise[0]['wire_inside']
        print('  First CRF tu=1 is inside the reported console bracket: PASS')

s = read(author / 'summary/gm-steps.json')
mismatches = []
for row in s['edges']:
    a = read(author / 'bench' / row['run'] / 'analysis.json')
    lo, hi = (-9, 27) if row['edge'] == 'takeover' else (27, 200)
    h = [x for x in a['health'] if lo <= x[0] < hi]
    first = next(t for t, v in h if v.endswith('tu1'))
    clear = next(t for t, v in h if t > first and v.endswith('tu0'))
    print(f'{row["run"]} {row["edge"]}: first_tu_sample={first:.3f}; '
          f'published_tu_set={row["tu_set"]:.3f}; clear_sample={clear:.3f}; '
          f'published_steady_clear={row["tu_steady_clear"]:.3f}; six_grades={row["pass"]}')
    if first != row['tu_set']:
        mismatches.append((row['run'], row['edge']))
print('First-tu-sample mismatches:', len(mismatches), mismatches)
assert len(mismatches) == 4

doc = source / 'docs/findings/387_SOFTWARE_GM_STEP.md'
for n, line in enumerate(doc.read_text().splitlines(), 1):
    if n > 358 and 'takeover Announce named' in line:
        found = bool(re.search(r'`[0-9a-f]{16}`', line))
        print(f'Privacy: {doc.relative_to(source)}:{n}: literal controller clock identity present={found}; value withheld')
        assert found
print('Audit completed; discrepancies are findings, not a packet integrity failure.')
