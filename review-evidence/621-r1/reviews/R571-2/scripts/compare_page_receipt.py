#!/usr/bin/env python3
"""Compare SAVED_STATE_SNAPSHOT_OWNERSHIP.md section 18 / limits item 6 with measurements.json.

Usage: compare_page_receipt.py <repo-root> [page-override]
Every expected string is derived from the receipt; the page must contain it.
Exit 0 when every comparison holds, 1 otherwise.
"""
import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
r = json.loads((root / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
page = Path(sys.argv[2] if len(sys.argv) > 2 else root / 'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md').read_text()
start = page.index('\nTiming. MEASURED on')
sec18 = page[start:page.index('\nMeasurements retire', start)]
lim6 = page[page.index('\n6. Physical timing remains unmeasured'):]
lim6 = lim6[:lim6.index('\n\n')]
fails = []


def need(where, text, label):
    ok = text in where
    print(('OK  ' if ok else 'FAIL'), label, repr(text))
    if not ok:
        fails.append(label)


tree = subprocess.run(['git', '-C', str(root), 'rev-parse', r['base'] + '^{tree}'],
                      capture_output=True, text=True, check=True).stdout.strip()
print('receipt base tree from git:', tree, 'receipt tree:', r['tree'], 'equal:', tree == r['tree'])
if tree != r['tree']:
    fails.append('tree')
need(sec18, f"MEASURED on {r['date']}", 'date')
need(sec18, f"Measured commit: `{r['base']}`", 'measured commit')
need(sec18, f"Measured tree: `{r['tree']}`", 'measured tree')
need(sec18, f"Firmware SHA-256: `{r['product_firmware_sha256']}`", 'firmware')
need(sec18, f"Protocol-processor pin: `{r['processor_pins']['protocol-processor']}`", 'pp pin')
need(sec18, f"gPTP-processor pin: `{r['processor_pins']['gptp-processor']}`", 'gptp pin')
need(sec18, r['remeasurement_assignment'], 'remeasurement assignment')
need(sec18, r['assignment'], 'capture procedure')
FLOOR, LIMIT = r['hold_floor_ms'], r['hold_floor_ms'] / 2
need(sec18, f"acceptance limit is therefore {LIMIT} ms", 'limit')
maxima = {(m['shape'], m['cpu_hz']): m for m in r['maxima']}
m8 = maxima[('endstation_ax7101_8x8', 50_000_000)]
m1 = maxima[('endstation_ax7101_1x1_tdm8', 50_000_000)]
m8f = maxima[('endstation_ax7101_8x8', 100_000_000)]
worst8 = max(m8['maximum_ms'], m8f['maximum_ms'])
for where, name in ((sec18, 'sec18'), (lim6, 'limits6')):
    need(where, f"{m8['maximum_ms']:.5f} ms", f'{name} worst 8x8')
    need(where, f"{m8['margin']:.4f}x", f'{name} 8x8 ratio')
    need(where, f"{LIMIT - m8['maximum_ms']:.5f} ms", f'{name} 24.5 margin')
    need(where, f"1x1 maximum is {m1['maximum_ms']:.5f} ms ({m1['margin']:.4f}x floor ratio)", f'{name} 1x1')
    m = r['measured_for']
    need(where, f"{m['endstation_ax7101_8x8']['raw_bytes']:,} bytes", f'{name} 8x8 bytes')
need(lim6, f"non-contract: {m8f['maximum_ms']:.5f} ms maximum", 'limits6 100 MHz')
print('worst 8x8 across clocks is the 50 MHz point:', worst8 == m8['maximum_ms'])
names = {'endstation_ax7101_1x1_tdm8': '1x1', 'endstation_ax7101_8x8': '8x8'}
rows = 0
for a in r['measurements']:
    basis = 'contract' if a['clock_role'] == 'contract' else 'non-contract'
    row = (f"| {names[a['shape']]} | {a['cpu_hz'] // 1_000_000} / {a['sys_hz'] // 1_000_000}, {basis} | "
           f"{a['traffic'].upper()} | {a['minimum_ms']:.5f} to {a['maximum_ms']:.5f} | {a['margin']:.4f}x |")
    need(sec18, row, 'table row')
    rows += 1
table_rows = [line for line in sec18.splitlines() if line.startswith('| 1x1') or line.startswith('| 8x8')]
print('page table rows:', len(table_rows), 'receipt arms:', rows)
if len(table_rows) != rows:
    fails.append('row count')
stale = ['a2f1734283f367d0d522c8c7cda09b79aff60d06', 'c28595df81fb96ae7cb554216c76a23917105169',
         'b2db3a970cedbbff2f8ba813acb96122c442bc58', '13.86484', '3.5341x', '10.63516', '13.84836',
         '13.67682']
for token in stale:
    if token in page:
        print('FAIL stale token still present:', token)
        fails.append('stale ' + token)
print('stale tokens absent:', not any(t in page for t in stale))
print('RESULT:', 'PASS' if not fails else f'FAIL {fails}')
sys.exit(1 if fails else 0)
