#!/usr/bin/env python3
"""Compare SAVED_STATE_SNAPSHOT_OWNERSHIP.md section 18 and limits item 6
with tb/verilator/nvm_capture_cpu/measurements.json.

Usage: python3 -I compare_page_receipt.py <repo-root>
Prints one line per compared figure or identity; exit 1 on any difference.
Read-only.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PAGE = (ROOT / 'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md').read_text()
REC = json.loads((ROOT / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
FLOOR = REC['hold_floor_ms']
BAD = 0


def same(label, page_value, receipt_value):
    global BAD
    ok = page_value == receipt_value
    BAD += not ok
    print(f"{'EQUAL' if ok else 'DIFF '} {label}: page={page_value!r} receipt={receipt_value!r}")


def one(pattern, text=PAGE):
    found = re.findall(pattern, text)
    if len(found) != 1:
        raise SystemExit(f'pattern not unique ({len(found)}): {pattern}')
    return found[0]


def ms(value):
    return f'{value:.5f}'


def ratio(value):
    return f'{FLOOR / value:.4f}x'


sec_start = PAGE.index('Timing. MEASURED on')
sec = PAGE[sec_start:PAGE.index('Measurements retire the six-instructions')]
lim_start = PAGE.index("gives the current receipt's identities and six maxima")
lim = PAGE[lim_start:lim_start + 1200]

arms = {(a['shape'], a['cpu_hz'], a['traffic']): a for a in REC['measurements']}
mx = {(m['shape'], m['cpu_hz']): m for m in REC['maxima']}
S8, S1 = 'endstation_ax7101_8x8', 'endstation_ax7101_1x1_tdm8'

# Identities.
same('date', one(r'MEASURED on (\d{4}-\d\d-\d\d)', sec), REC['date'])
same('ruling', one(r'#621 final ruling\]\((\S+?)\)', sec), REC['remeasurement_assignment'])
same('measured commit', one(r'Measured commit: `([0-9a-f]{40})`', sec), REC['base'])
same('measured tree', one(r'Measured tree: `([0-9a-f]{40})`', sec), REC['tree'])
tree = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', REC['base'] + '^{tree}'],
                      capture_output=True, text=True, check=True).stdout.strip()
same('receipt tree is the measured commit tree', REC['tree'], tree)
same('firmware sha256', one(r'Firmware SHA-256: `([0-9a-f]{64})`', sec), REC['product_firmware_sha256'])
same('protocol pin', one(r'Protocol-processor pin: `([0-9a-f]{40})`', sec),
     REC['processor_pins']['protocol-processor'])
same('gptp pin', one(r'gPTP-processor pin: `([0-9a-f]{40})`', sec),
     REC['processor_pins']['gptp-processor'])
gptp_pin = subprocess.run(['git', '-C', str(ROOT), 'ls-tree', REC['base'], 'gptp-processor'],
                          capture_output=True, text=True, check=True).stdout.split()[2]
same('receipt gptp pin is the measured commit gitlink', REC['processor_pins']['gptp-processor'], gptp_pin)
pp_pin = subprocess.run(['git', '-C', str(ROOT), 'ls-tree', REC['base'], 'protocol-processor'],
                        capture_output=True, text=True, check=True).stdout.split()[2]
same('receipt protocol pin is the measured commit gitlink', REC['processor_pins']['protocol-processor'], pp_pin)

# Section 18 headline figures.
w8 = mx[(S8, 50_000_000)]['maximum_ms']
same('s18 worst 8x8', one(r'worst 8x8 measurement is ([\d.]+) ms', sec), ms(w8))
same('s18 floor ratio', one(r'Its floor ratio is ([\d.]+x)', sec), ratio(w8))
same('s18 margin to 24.5', one(r'margin to 24\.5 ms is ([\d.]+) ms', sec), ms(FLOOR / 2 - w8))
w1 = mx[(S1, 50_000_000)]['maximum_ms']
same('s18 1x1 maximum', one(r'1x1 maximum is ([\d.]+) ms \(([\d.]+x)', sec), (ms(w1), ratio(w1)))
same('s18 capture count', one(r'contains all (\d+) captures', sec),
     str(sum(len(a['rows']) for a in REC['measurements'])))

# Table rows.
rows = re.findall(r'^\| (1x1|8x8) \| (\d+) / 100, [^|]+\| (ON|OFF) \| ([\d.]+) to ([\d.]+) \| ([\d.]+x) \|$',
                  sec, re.M)
same('table row count', len(rows), 6)
for shape, cpu, traffic, lo, hi, rat in rows:
    arm = arms[(S1 if shape == '1x1' else S8, int(cpu) * 1_000_000, traffic.lower())]
    times = [r['sys_cycles'] / arm['sys_hz'] * 1000 for r in arm['rows']]
    same(f'row {shape} {cpu} {traffic}', (lo, hi, rat),
         (ms(min(times)), ms(max(times)), ratio(max(times))))
    same(f'row {shape} {cpu} {traffic} arm summary', (lo, hi),
         (ms(arm['minimum_ms']), ms(arm['maximum_ms'])))

# Census.
mf = REC['measured_for']
same('census 8x8', one(r'At 8x8 it is ([\d,]+) bytes / (\d+) records', sec),
     (f"{mf[S8]['raw_bytes']:,}", str(mf[S8]['records'])))
same('census 1x1', one(r'is ([\d,]+) bytes / (\d+) records at 1x1', sec),
     (f"{mf[S1]['raw_bytes']:,}", str(mf[S1]['records'])))

# Limits item 6.
same('limits worst 8x8', one(r'worst 8x8 copy is ([\d.]+) ms', lim), ms(w8))
same('limits bytes/records', one(r'covers ([\d,]+) bytes and (\d+) records', lim),
     (f"{mf[S8]['raw_bytes']:,}", str(mf[S8]['records'])))
same('limits floor ratio', one(r'guaranteed 49 ms floor is ([\d.]+x)', lim), ratio(w8))
same('limits margin', one(r'24\.5 ms margin is ([\d.]+) ms', lim), ms(FLOOR / 2 - w8))
same('limits 1x1 maximum', one(r'1x1 maximum is ([\d.]+) ms \(([\d.]+x)', lim), (ms(w1), ratio(w1)))

# No stale identities anywhere on the page.
for stale in ('a2f1734283f367d0d522c8c7cda09b79aff60d06', 'c28595df81fb96ae7cb554216c76a23917105169',
              'b2db3a970cedbbff2f8ba813acb96122c442bc58', '13.86484', '3.5341x', '10.63516',
              '13.84836', '13.67682'):
    same(f'stale token absent: {stale}', PAGE.count(stale), 0)

print('RESULT:', 'ALL EQUAL' if BAD == 0 else f'{BAD} DIFFERENCES')
sys.exit(1 if BAD else 0)
