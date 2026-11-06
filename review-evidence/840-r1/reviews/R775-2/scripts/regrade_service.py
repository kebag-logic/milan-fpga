#!/usr/bin/env python3
"""Regrade the published service-budget receipts with the head's own grader.

Usage: regrade_service.py <repo> <receipt-json-dir> <own-build-root>
Prints, per receipt: log binding, findings, T, P, own charge, worst publication
bound, and the worst bound under the shape-wide charge; then compares each
receipt's build hashes with a build made at the reviewed head.
"""
import hashlib
import json
import pathlib
import re
import sys

repo, jdir, own = map(pathlib.Path, sys.argv[1:4])
sys.path.insert(0, str(repo / 'tb/verilator/fw_service_budget'))
sys.dont_write_bytecode = True
import run  # noqa: E402

rows = []
for f in sorted(jdir.glob('*.json')):
    d = json.loads(f.read_text())
    raw = d['raw_log']
    bound = hashlib.sha256(raw.encode()).hexdigest() == d['log_sha256']
    saved = d.get('service_findings')
    fresh = run.service_findings(d, raw)
    phy = d['phy']
    worst = max((r['phy_publication_bound_ms'], r['duty']) for r in d['rows'] if 'phy_publication_bound_ms' in r)
    rows.append(dict(file=f.name, shape=d['shape'], plan=d['media']['plan'], bound=bound, saved=saved,
                     fresh=fresh, T=phy['max_transaction_sys_cycles'], P=phy['max_poll_sys_cycles'],
                     tx=phy['transactions'], charge=phy['scheduling_charge_sys_cycles'] / 1e5,
                     worst=worst, data=d))
for shape in sorted({r['shape'] for r in rows}):
    group = [r for r in rows if r['shape'] == shape]
    t = max(r['T'] for r in group)
    p = max(r['P'] for r in group)
    wide = (p + 16 * t) / 1e5
    print(f'{shape}: shape-wide T {t} P {p} charge {wide:.5f} ms (from the receipts with JSON)')
    for r in group:
        print(f"  {r['plan']:16} log-bound={r['bound']} tx={r['tx']} T={r['T']} P={r['P']} own={r['charge']:.5f}"
              f" worst={r['worst'][0]:.5f} ({r['worst'][1]}) at-wide-charge={r['worst'][0] - r['charge'] + wide:.5f}"
              f" saved_findings={r['saved']} fresh_findings={r['fresh']}")
    spec = json.loads((own / ('fw-' + shape.removeprefix('endstation_ax7101_')) / 'service_spec.json').read_text())
    for r in group:
        theirs = r['data']['build_hashes']
        mine = spec['build_hashes']
        diff = sorted(k for k in set(theirs) | set(mine) if theirs.get(k) != mine.get(k))
        print(f"  {r['plan']:16} build-hash keys {len(theirs)} differing {len(diff)}: {diff[:12]}")
heads = {json.dumps(r['data']['input_hashes'], sort_keys=True) for r in rows}
print('distinct input-hash sets in receipts:', len(heads))
now = run.inputs()
for h in heads:
    h = json.loads(h)
    print('input keys differing from the head:', sorted(k for k in set(h) | set(now) if h.get(k) != now.get(k)))
