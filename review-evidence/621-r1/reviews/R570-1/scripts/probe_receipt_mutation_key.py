#!/usr/bin/env python3
"""Probe: can a receipt arm opt out of the 24.5 ms production bound in
scripts/check_nvm_capture.py by carrying a 'mutation' key?

Usage: probe_receipt_mutation_key.py <checkout-root> [alternate run.py]
With the optional argument, the gate grades through that run.py instead
(used to grade the same plant with the base revision's grader).
Loads the checkout's receipt in memory (no file is written), plants one
over-bound production capture (25 ms) in the 8x8/50 MHz traffic-on arm with
summaries recomputed consistently, and grades it twice through the gate's
own check_receipt(): once as-is (must be refused) and once with
mutation='byte-only' added to that arm.
"""
import copy, json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'scripts'))
sys.dont_write_bytecode = True
import check_nvm_capture as gate  # noqa: E402
capture, recipe = gate.capture, gate.recipe
if len(sys.argv) > 2:
    import importlib.util
    spec_ = importlib.util.spec_from_file_location('run_alt', sys.argv[2])
    capture = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(capture)
    gate.capture = capture
    print('grader:', sys.argv[2])
receipt = json.loads((root / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
actual = gate.current_inputs()

def plant(with_key):
    r = copy.deepcopy(receipt)
    arm = next(a for a in r['measurements'] if a['shape'] == 'endstation_ax7101_8x8'
               and a['cpu_hz'] == recipe.CPU_HZ and a['traffic'] == 'on')
    arm['rows'][0]['sys_cycles'] = 2_500_000          # 25.0 ms > 24.5 ms
    if with_key:
        arm['mutation'] = 'byte-only'
    src = actual[arm['shape']]
    spec = dict(arm, raw_bytes=src['raw_bytes'], records=src['records'])
    try:
        summary = capture.grade_rows(arm['rows'], spec)
    except RuntimeError as exc:
        return f'refused while building plant: {exc}'
    for k, v in summary.items():
        arm[k] = v
    maxima = []
    keys = [(a['shape'], a['cpu_hz'], a['traffic']) for a in r['measurements']]
    for shape, clock in sorted({k[:2] for k in keys}):
        group = [a for a in r['measurements'] if (a['shape'], a['cpu_hz']) == (shape, clock)]
        worst = capture.maximum_ms(group)
        maxima.append(dict(shape=shape, cpu_hz=clock, maximum_ms=worst,
                           margin=recipe.HOLD_FLOOR_MS / worst))
    r['maxima'] = maxima
    try:
        gate.check_receipt(r, actual)
    except RuntimeError as exc:
        return f'REFUSED: {exc}'
    return f'ACCEPTED: published 8x8/50 MHz maximum {[m for m in maxima if m["cpu_hz"]==recipe.CPU_HZ and "8x8" in m["shape"]][0]["maximum_ms"]} ms'

print('plain over-bound production arm      :', plant(False))
print("same arm carrying mutation='byte-only':", plant(True))
