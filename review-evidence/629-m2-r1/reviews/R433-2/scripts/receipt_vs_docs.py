#!/usr/bin/env python3
"""Compare the capture receipt (measurements.json) with the figures printed in
SAVED_STATE_SNAPSHOT_OWNERSHIP.md sections 17/18/20 and the harness README.
Usage: receipt_vs_docs.py <repo>"""
import json, re, sys
from pathlib import Path
repo = Path(sys.argv[1])
rc = json.loads((repo/'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
doc = (repo/'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md').read_text()
readme = (repo/'tb/verilator/nvm_capture_cpu/README.md').read_text()
bad = 0
def chk(label, cond):
    global bad
    print(('OK   ' if cond else 'FAIL ') + label)
    bad += (not cond)
tag = {'endstation_ax7101_1x1_tdm8': '1x1', 'endstation_ax7101_8x8': '8x8'}
for m in rc['measurements']:
    rows = m['rows']
    ms = [r['sys_cycles'] / m['sys_hz'] * 1e3 for r in rows]
    chk(f"{m['shape']} {m['cpu_hz']} {m['traffic']}: min/max recomputed from rows",
        abs(min(ms) - m['minimum_ms']) < 1e-9 and abs(max(ms) - m['maximum_ms']) < 1e-9)
    chk(f"  16 rows, all ok, census {m['rows'][0]['raw']}/{m['rows'][0]['records']}",
        len(rows) == 16 and all(r['ok'] == 1 and r['mismatches'] == 0 and r['open'] == 0 for r in rows)
        and all((r['raw'], r['records']) == (rc['measured_for'][m['shape']]['raw_bytes'], rc['measured_for'][m['shape']]['records']) for r in rows))
    traffic_ok = all(r['requests'] > 0 and r['responses'] > 0 and r['reads'] > 0 for r in rows) if m['traffic'] == 'on' \
        else all(r['requests'] == 0 and r['responses'] == 0 and r['reads'] == 0 for r in rows)
    chk(f"  traffic counters consistent with arm {m['traffic']}", traffic_ok)
    mhz = m['cpu_hz'] // 1_000_000
    basis = 'contract' if mhz == 50 else 'non-contract'
    line = (f"| {tag[m['shape']]} | {mhz} / 100, {basis} | {m['traffic'].upper()} | "
            f"{m['minimum_ms']:.5f} to {m['maximum_ms']:.5f} | {49 / m['maximum_ms']:.4f}x |")
    chk(f"  section 18 row present: {line}", line in doc)
for mx in rc['maxima']:
    print(f"MAXIMUM {mx['shape']} {mx['cpu_hz']} {mx['maximum_ms']:.5f} ms margin-ratio {mx['margin']:.4f}")
m88 = [x for x in rc['maxima'] if x['shape'].endswith('8x8') and x['cpu_hz'] == 50_000_000][0]['maximum_ms']
m11 = [x for x in rc['maxima'] if x['shape'].endswith('tdm8') and x['cpu_hz'] == 50_000_000][0]['maximum_ms']
m100 = [x for x in rc['maxima'] if x['cpu_hz'] == 100_000_000][0]['maximum_ms']
chk('8x8 max <= 24.5 ms', m88 <= 24.5)
for s in [f"**The worst 8x8 measurement is {m88:.5f} ms.**", f"Its floor ratio is {49/m88:.4f}x.",
          f"The margin to 24.5 ms is {24.5-m88:.5f} ms.", f"The 1x1 maximum is {m11:.5f} ms ({49/m11:.4f}x floor ratio).",
          f"The worst 8x8 copy is {m88:.5f} ms across both arms.", f"The 24.5 ms margin is {24.5-m88:.5f} ms.",
          f"non-contract: {m100:.5f} ms maximum.", f"Measured commit: `{rc['base']}`.", f"Measured tree: `{rc['tree']}`.",
          f"Firmware SHA-256: `{rc['product_firmware_sha256']}`.",
          f"Protocol-processor pin: `{rc['processor_pins']['protocol-processor']}`."]:
    chk('doc has: ' + s, s in doc)
c88 = rc['measured_for']['endstation_ax7101_8x8']; c11 = rc['measured_for']['endstation_ax7101_1x1_tdm8']
for s in [f"The full 8x8 copy covers {c88['raw_bytes']:,} bytes and {c88['records']} records.",
          f"The 1x1 copy covers {c11['raw_bytes']:,} bytes and {c11['records']} records."]:
    chk('README has: ' + s, s in readme)
for s in [f"The full closed-record census is {c11['raw_bytes']:,} bytes / {c11['records']} records at 1x1.",
          f"At 8x8 it is {c88['raw_bytes']:,} bytes / {c88['records']} records.",
          f"It covers {c88['raw_bytes']:,} bytes and {c88['records']} records, including output maps."]:
    chk('doc has: ' + s, s in doc)
print('RESULT', 'PASS' if not bad else f'FAIL ({bad})')
sys.exit(1 if bad else 0)
