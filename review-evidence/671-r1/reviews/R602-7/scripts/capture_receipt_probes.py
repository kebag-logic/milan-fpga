#!/usr/bin/env python3
"""Fault probes on the saved-state capture receipt gate, run in a disposable tree.

Usage: capture_receipt_probes.py <clone> <disposable-tree>

<clone> is the review clone at the head (read only; used for `git show`).
<disposable-tree> is an export of the head with its submodule trees; each
probe rewrites one file there, runs scripts/check_nvm_capture.py, and restores
the file. Each probe must exit nonzero with its named reason; the head itself
must pass.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

clone, tree = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
RECEIPT = 'tb/verilator/nvm_capture_cpu/measurements.json'
FIRMWARE = 'sw/firmware/milan_baremetal/milan_baremetal.c'
env = dict(os.environ, PYTHONHASHSEED='0')


def show(rev: str, path: str) -> bytes:
    return subprocess.run(['git', '-C', str(clone), 'show', f'{rev}:{path}'],
                          check=True, capture_output=True).stdout


def gate() -> tuple[int, str]:
    run = subprocess.run([sys.executable, 'scripts/check_nvm_capture.py'], cwd=tree,
                         capture_output=True, text=True, env=env)
    lines = [x for x in (run.stdout + run.stderr).splitlines() if not x.startswith('CONTROL')]
    return run.returncode, (lines[-1] if lines else '')


def probe(name: str, path: str, data: bytes, want_rc_zero: bool, want_words: str) -> bool:
    target = tree / path
    original = target.read_bytes()
    target.write_bytes(data)
    try:
        rc, last = gate()
    finally:
        target.write_bytes(original)
    ok = (rc == 0) == want_rc_zero and want_words in last
    print(f"{'OK  ' if ok else 'FAIL'} {name}: rc={rc} last={last[:160]!r}")
    return ok


head = json.loads(show('9b32002c', RECEIPT))
results = []
results.append(probe('head receipt at head', RECEIPT, show('9b32002c', RECEIPT), True, 'PASS'))
results.append(probe('round-5 receipt (c7d0ad63) at the head tree', RECEIPT,
                     show('c7d0ad63', RECEIPT), False, 'measurement harness changed'))
results.append(probe('dev receipt (c6bd08c6) at the head tree', RECEIPT,
                     show('c6bd08c6', RECEIPT), False, 'product firmware changed'))

over = json.loads(json.dumps(head))
arm = next(a for a in over['measurements']
           if a['shape'] == 'endstation_ax7101_8x8' and a['cpu_hz'] == 50_000_000 and a['traffic'] == 'off')
arm['rows'][0]['sys_cycles'] = 2_450_001
results.append(probe('8x8/50 OFF row one tick over half the floor', RECEIPT,
                     (json.dumps(over, indent=2) + '\n').encode(), False, 'half the 49 ms'))

edited = json.loads(json.dumps(head))
arm = next(a for a in edited['measurements']
           if a['shape'] == 'endstation_ax7101_1x1_tdm8' and a['traffic'] == 'on')
worst = max(range(len(arm['rows'])), key=lambda i: arm['rows'][i]['sys_cycles'])
arm['rows'][worst]['sys_cycles'] += 1
results.append(probe('1x1 ON worst row edited by one cycle, summary kept', RECEIPT,
                     (json.dumps(edited, indent=2) + '\n').encode(), False, 'receipt summary differs'))

fw = (tree / FIRMWARE).read_bytes()
results.append(probe('firmware one byte appended', FIRMWARE, fw + b'\n', False,
                     'product firmware changed'))

# The 96 captures of the head receipt against the round-5 receipt.
old = json.loads(show('c7d0ad63', RECEIPT))
key = lambda a: (a['shape'], a['cpu_hz'], a['traffic'])
pairs = {key(a): a for a in old['measurements']}
same = sum(r == s for a in head['measurements'] for r, s in zip(a['rows'], pairs[key(a)]['rows']))
total = sum(len(a['rows']) for a in head['measurements'])
cycles_same = all([r['sys_cycles'] for r in a['rows']] == [r['sys_cycles'] for r in pairs[key(a)]['rows']]
                  for a in head['measurements'])
print(f"rows identical to round-5 receipt: {same}/{total}; sys_cycles identical in every arm: {cycles_same}")
results.append(total == 96 and cycles_same)

# Section 18 figures regenerated from the head receipt.
doc = (tree / 'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md').read_text()
label = {'endstation_ax7101_1x1_tdm8': '1x1', 'endstation_ax7101_8x8': '8x8'}
missing = []
for a in head['measurements']:
    ms = [r['sys_cycles'] * 1000 / a['sys_hz'] for r in a['rows']]
    basis = 'contract' if a['cpu_hz'] == 50_000_000 else 'non-contract'
    row = (f"| {label[a['shape']]} | {a['cpu_hz'] // 1_000_000} / {a['sys_hz'] // 1_000_000}, {basis} | "
           f"{a['traffic'].upper()} | {min(ms):.5f} to {max(ms):.5f} | {49 / max(ms):.4f}x |")
    print('table row', 'present' if row in doc else 'MISSING', row)
    if row not in doc:
        missing.append(row)
for m in head['maxima']:
    print('maximum', label[m['shape']], m['cpu_hz'], f"{m['maximum_ms']:.5f}", f"ratio {m['margin']:.4f}x",
          f"margin-to-24.5 {24.5 - m['maximum_ms']:.5f}")
w = next(m for m in head['maxima'] if m['shape'] == 'endstation_ax7101_8x8' and m['cpu_hz'] == 50_000_000)
for text in (f"**The worst 8x8 measurement is {w['maximum_ms']:.5f} ms.**",
             f"Its floor ratio is {w['margin']:.4f}x.",
             f"The margin to 24.5 ms is {24.5 - w['maximum_ms']:.5f} ms.",
             f"Measured tree: `{head['tree']}`.", f"Measured commit: `{head['base']}`.",
             f"Firmware SHA-256: `{head['product_firmware_sha256']}`.",
             f"gPTP-processor pin: `{head['processor_pins']['gptp-processor']}`.",
             f"Protocol-processor pin: `{head['processor_pins']['protocol-processor']}`."):
    present = text in doc
    print('doc line', 'present' if present else 'MISSING', text)
    if not present:
        missing.append(text)
results.append(not missing)
print('ALL PROBES OK' if all(results) else 'SOME PROBE FAILED')
sys.exit(0 if all(results) else 1)
