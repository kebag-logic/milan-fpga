#!/usr/bin/env python3
"""Independently recompute the capture receipt's summaries and compare revisions.

Usage: receipt_audit.py <repo> <old-rev> <new-rev>
Prints per-arm extrema, margins, the doc figures derived from them, and which
rows changed between the two receipt revisions.
"""
import json
import subprocess
import sys

repo, old_rev, new_rev = sys.argv[1:4]
PATH = 'tb/verilator/nvm_capture_cpu/measurements.json'


def load(rev):
    return json.loads(subprocess.check_output(['git', '-C', repo, 'show', f'{rev}:{PATH}']))


old, new = load(old_rev), load(new_rev)
print('new product_firmware_sha256', new['product_firmware_sha256'])
fw = subprocess.check_output(['git', '-C', repo, 'show',
                              f'{new_rev}:sw/firmware/milan_baremetal/milan_baremetal.c'])
import hashlib
print('head milan_baremetal.c sha256', hashlib.sha256(fw).hexdigest())
key = lambda a: (a['shape'], a['cpu_hz'], a['traffic'])
old_arms = {key(a): a for a in old['measurements']}
groups = {}
for arm in new['measurements']:
    ms = [r['sys_cycles'] / arm['sys_hz'] * 1000 for r in arm['rows']]
    assert len(arm['rows']) == 16 == arm['captures'], key(arm)
    assert [r['index'] for r in arm['rows']] == list(range(16))
    bad = [r for r in arm['rows'] if r['ok'] != 1 or r['mismatches'] or r['open']]
    counts_ok = all((all(r[k] > 0 for k in ('requests', 'responses', 'reads')) if arm['traffic'] == 'on'
                     else not any(r[k] for k in ('requests', 'responses', 'reads'))) for r in arm['rows'])
    o = old_arms[key(arm)]
    changed = [i for i, (a, b) in enumerate(zip(o['rows'], arm['rows'])) if a != b]
    print(f"{key(arm)} min={min(ms):.5f} max={max(ms):.5f} recorded=({arm['minimum_ms']},{arm['maximum_ms']}) "
          f"margin={49/max(ms):.4f} bad={len(bad)} traffic_counts_ok={counts_ok} phase={arm['phase']} "
          f"rows_changed_vs_old={changed}")
    groups.setdefault(key(arm)[:2], {})[arm['traffic']] = max(ms)
for (shape, hz), arms in sorted(groups.items()):
    worst = max(arms.values())
    print(f"MAX {shape} {hz}: {worst:.5f} ms margin {49/worst:.4f} below24.5={24.5-worst:.5f} "
          f"on-off={arms['on']-arms['off']:.5f} ({(arms['on']-arms['off'])/arms['off']*100:.3f}%)")
print('maxima block', json.dumps(new['maxima']))
print('top-level keys changed:', sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k)))
