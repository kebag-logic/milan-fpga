#!/usr/bin/env python3
"""From published results.json and stimulus files: (a) how many of each load's MAAP echo records were delivered
(offers x echo items - skipped), and (b) load frames counted in results.json against the frames the testbench
received at the MAC (SUMMARY rx_frames) less the draws' own four frames each.

usage: load_delivery.py <receipts dir>
"""
import json, re, sys
from pathlib import Path
ev = Path(sys.argv[1])
def echo_items(stimulus: Path) -> dict:
    out = {}
    for line in stimulus.read_text().splitlines():
        if line.startswith('defload '):
            w = line.split()
            out[w[1]] = (sum(1 for i in w[2:] if i.split('/')[1] == 'echo'), len(w) - 2)
    return out
runs = [('ci-1x1-composed', ev / 'head/ci-1x1-composed__results.json', ev / 'head/ci-1x1-composed__wire.txt'),
        ('8x8-composed', ev / 'head/8x8-composed__results.json', ev / 'head/8x8-composed__wire.txt'),
        ('campaign-unit2', ev / 'campaign/head-107f3f95de/unit2-results.json', ev / 'head/ci-1x1-composed__wire.txt'),
        ('campaign-unit3', ev / 'campaign/head-107f3f95de/unit3-results.json', ev / 'head/ci-1x1-composed__wire.txt')]
for name, res, stim in runs:
    r = json.loads(res.read_text())
    items = echo_items(stim)
    summ = dict(kv.split('=') for kv in r['summary'].split()[1:])
    print(f'== {name}: draws {r["draws"]}, simulated {r["simulated_ms"]} ms')
    total_load = 0
    for load, t in r['load'].items():
        echoes, n_items = items[load]
        possible = t['offers'] * echoes
        print(f'  load {load}: offers {t["offers"]}, items/offer {n_items} of which MAAP echoes {echoes}; '
              f'echoes possible {possible}, skipped {t["skipped"]}, delivered {possible - t["skipped"]}')
        total_load += t['frames']
    at_mac = int(summ['rx_frames']) + int(summ['bench_rx'])
    print(f'  load frames in results.json {total_load} + draws {4 * r["draws"]} = {total_load + 4 * r["draws"]}; '
          f'received at the MAC and bench {at_mac}; never offered before the end {total_load + 4 * r["draws"] - at_mac}')
