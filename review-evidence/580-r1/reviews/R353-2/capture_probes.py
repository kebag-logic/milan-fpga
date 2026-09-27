#!/usr/bin/env python3
"""Receipt mutation probes for scripts/check_nvm_capture.py on a disposable tree.

Usage: capture_probes.py <disposable-tree>
Each probe edits tb/verilator/nvm_capture_cpu/measurements.json, runs the
checker, records rc, and restores the original bytes before the next probe.
"""
import json
import subprocess
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
path = tree / 'tb/verilator/nvm_capture_cpu/measurements.json'
original = path.read_bytes()


def arm(d, shape, hz, traffic):
    return next(a for a in d['measurements']
                if (a['shape'], a['cpu_hz'], a['traffic']) == (shape, hz, traffic))


def over_bar(d):
    row = arm(d, 'endstation_ax7101_8x8', 50_000_000, 'on')['rows'][0]
    row['sys_cycles'] = 2_450_001


def at_bar(d):
    a = arm(d, 'endstation_ax7101_8x8', 50_000_000, 'on')
    a['rows'][0]['sys_cycles'] = 2_450_000


def pins(d):
    d['processor_pins']['protocol-processor'] = '0' * 40


def provenance(d):
    d['base'] = '0' * 40
    d['tree'] = '0' * 40


def maxima(d):
    d['maxima'][1]['maximum_ms'] = 24.0


def drop_row(d):
    arm(d, 'endstation_ax7101_8x8', 50_000_000, 'off')['rows'].pop()


PROBES = [('unmodified', None, 0), ('processor-pins-bogus', pins, None),
          ('base-and-tree-bogus', provenance, None), ('row-over-24.5ms', over_bar, 1),
          ('row-at-24.5ms-summary-stale', at_bar, 1), ('maximum-edited', maxima, 1),
          ('off-row-dropped', drop_row, 1)]
failed = False
try:
    for name, edit, want in PROBES:
        data = json.loads(original)
        if edit:
            edit(data)
            path.write_text(json.dumps(data, indent=2) + '\n')
        proc = subprocess.run([sys.executable, '-B', 'scripts/check_nvm_capture.py'], cwd=tree,
                              capture_output=True, text=True)
        path.write_bytes(original)
        tail = (proc.stdout + proc.stderr).strip().splitlines()[-1]
        verdict = 'observed' if want is None else ('as-expected' if (proc.returncode != 0) == bool(want) else 'UNEXPECTED')
        failed |= verdict == 'UNEXPECTED'
        print(f'{name}: rc={proc.returncode} {verdict}: {tail}')
finally:
    path.write_bytes(original)
sys.exit(1 if failed else 0)
