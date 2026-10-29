#!/usr/bin/env python3
"""Scratch: per composed window of prof.py's JSON, the functions that hold it (own cycles with their refill waits,
helpers charged where the variant charged them), grouped by module family, and lwSRP's share.
usage: holders7.py PROF_JSON [RUN_LABEL ...]"""
import json
import sys
from collections import defaultdict

LWSRP = ('mrp_mad', 'mrp_pdu', 'msrp', 'mvrp', 'mrp_timer', 'mrp_app', 'mrp_port', 'shlan', 'timer')
FAMILY = {'mbx': 'mailbox driver', 'mbx_plat_mmio': 'mailbox driver', 'ctrl_loop': 'service loop',
          'ctrl_mem': 'memory primitives', 'rt_lshrdi3': 'compiler runtime'}


def family(name: str) -> str:
    obj = name.split(':', 1)[0]
    if obj in FAMILY:
        return FAMILY[obj]
    if obj.startswith(LWSRP):
        return 'lwSRP'
    if obj.startswith(('aecp', 'ctrl_app_aecp', 'ctrl_aecp_image', 'nvm')):
        return 'AECP'
    if obj.startswith(('acmp', 'ctrl_app_srp')) and not obj.startswith('acmp_'):
        return 'ACMP core' if obj == 'acmp' else 'apps'
    if obj.startswith('acmp_'):
        return 'ACMP adapter'
    if obj.startswith('srp_mbx'):
        return 'SRP adapter'
    if obj.startswith(('adp', 'maap')):
        return 'ADP/MAAP'
    return obj


runs = json.load(open(sys.argv[1]))
want = set(sys.argv[2:])
for r in runs:
    if want and r['label'] not in want:
        continue
    if r['window_ms'] > 40:
        continue
    fam = defaultdict(float)
    for f in r['funcs']:
        fam[family(f['name'])] += f['ms']
    total = sum(f['ms'] for f in r['funcs'])
    top = sorted(fam.items(), key=lambda kv: -kv[1])
    print(f"| {r['label']} | {r['group']} | {r['probe'].split('.')[2]} | {r['window_ms']:.2f} | "
          + ', '.join(f'{k} {v:.2f}' for k, v in top[:6]) + f" | {fam['lwSRP']:.2f} ({100 * fam['lwSRP'] / total:.0f} %) | "
          + ', '.join(f"`{f['name']}` {f['ms']:.2f}" for f in r['funcs'][:3]) + ' |')
