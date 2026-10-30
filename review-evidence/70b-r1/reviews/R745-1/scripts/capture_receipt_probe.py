#!/usr/bin/env python3
"""Recompute per-arm extrema of the capture receipt at HEAD and count captures whose
sys_cycles repeat the receipt at a base commit. Usage: capture_receipt_probe.py REPO BASE"""
import json, subprocess, sys
repo, base = sys.argv[1], sys.argv[2]
path = 'tb/verilator/nvm_capture_cpu/measurements.json'
head = json.load(open(f'{repo}/{path}'))
old = json.loads(subprocess.run(['git', '-C', repo, 'show', f'{base}:{path}'], capture_output=True, text=True, check=True).stdout)
def arms(d):
    return {(a['shape'], a['cpu_hz'], a['traffic']): a for a in d['measurements']}
h, o = arms(head), arms(old)
same = total = 0
for k, a in sorted(h.items()):
    ms = [r['sys_cycles'] / (a['sys_hz'] / 1000) for r in a['rows']]
    print(k, 'rows', len(a['rows']), 'ok', all(r['ok'] == 1 and r['mismatches'] == 0 and r['open'] == 0 for r in a['rows']),
          'min_ms', a['minimum_ms'], 'max_ms', a['maximum_ms'], 'recomputed', round(min(ms), 5), round(max(ms), 5),
          'hold_floor', a['hold_floor_ms'], 'margin', a['margin'])
    oc = [r['sys_cycles'] for r in o[k]['rows']]
    for r, c in zip(a['rows'], oc):
        total += 1; same += r['sys_cycles'] == c
print('repeat sys_cycles vs base:', same, 'of', total)
print('maxima', head['maxima'])
print('contract 8x8 max', max(m['maximum_ms'] for m in head['maxima'] if m['shape'].endswith('8x8') and m['cpu_hz'] == 50_000_000), 'limit 24.5')
