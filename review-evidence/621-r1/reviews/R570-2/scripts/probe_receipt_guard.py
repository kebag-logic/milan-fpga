#!/usr/bin/env python3
"""Reviewer probe of scripts/check_nvm_capture.py's production-bound guard.

Usage: python3 probe_receipt_guard.py <repo-root>

Loads the gate from its own path (so its ROOT/HARNESS resolve to the repo),
optionally with one in-memory source plant, then:
  * runs the gate's own opt_out_control on the real receipt;
  * grades a reviewer-built plant: the first arm's first capture one tick over
    half the 49 ms floor, summaries and maxima recomputed, with the arm's
    `mutation` key set to each of several values (and absent).
Expected: unplanted gate refuses every reviewer plant for the bound and its
control passes; every guard-removal plant makes the control fail.
Nothing on disk is modified.
"""
import json
import sys
import types
from copy import deepcopy
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
GATE = ROOT / 'scripts/check_nvm_capture.py'
sys.path.insert(0, str(ROOT / 'scripts'))

PLANTS = {
    'none': None,
    # Call site grades the raw arm (the pre-round-2 form).
    'callsite-raw-arm': ('capture.grade_rows(arm[\'rows\'], production_spec(arm, census))',
                         'capture.grade_rows(arm[\'rows\'], dict(arm, **census))'),
    # Spec builder passes the arm's own mutation through.
    'spec-keeps-mutation': ("**census, mutation='none')",
                            "**census, mutation=arm.get('mutation', 'none'))"),
    # Spec builder copies the whole arm.
    'spec-whole-arm': ("return dict({key: arm[key] for key in keys}, **census, mutation='none')",
                       "return dict(arm, **census)"),
}
MUTATION_VALUES = ['byte-only', 'skip-copy', 'no-traffic', 'anything', None]


def load(plant):
    text = GATE.read_text()
    if plant:
        old, new = plant
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    module = types.ModuleType('check_nvm_capture_probe')
    module.__file__ = str(GATE)
    sys.modules[module.__name__] = module
    exec(compile(text, str(GATE), 'exec'), module.__dict__)
    return module


def planted_receipt(gate, receipt, actual, value):
    planted = deepcopy(receipt)
    arm = planted['measurements'][0]
    if value is None:
        arm.pop('mutation', None)
    else:
        arm['mutation'] = value
    arm['rows'][0]['sys_cycles'] = gate.recipe.HOLD_FLOOR_MS * arm['sys_hz'] // 2000 + 1
    source = actual[arm['shape']]
    # Summaries recomputed without the bound, so only the bound can refuse.
    spec = dict(arm, raw_bytes=source['raw_bytes'], records=source['records'], mutation='x')
    arm.update(gate.capture.grade_rows(arm['rows'], spec))
    arms = planted['measurements']
    planted['maxima'] = []
    for shape, clock in sorted({(i['shape'], i['cpu_hz']) for i in arms}):
        worst = gate.capture.maximum_ms([i for i in arms if (i['shape'], i['cpu_hz']) == (shape, clock)])
        planted['maxima'].append(dict(shape=shape, cpu_hz=clock, maximum_ms=worst,
                                      margin=gate.recipe.HOLD_FLOOR_MS / worst))
    return planted


def outcome(fn):
    try:
        fn()
    except RuntimeError as exc:
        return f'REFUSED: {exc}'
    return 'ACCEPTED'


def main() -> int:
    results = {}
    for name, plant in PLANTS.items():
        gate = load(plant)
        actual = gate.current_inputs()
        receipt = json.loads((gate.HARNESS / 'measurements.json').read_text())
        row = {'real-receipt': outcome(lambda: gate.check_receipt(receipt, actual)),
               'gate-control': outcome(lambda: gate.opt_out_control(receipt, actual))}
        for value in MUTATION_VALUES:
            planted = planted_receipt(gate, receipt, actual, value)
            row[f'plant mutation={value}'] = outcome(lambda: gate.check_receipt(planted, actual))
        results[name] = row
        for key, value in row.items():
            print(f'{name:22} {key:28} {value}')
    ok = True
    base = results['none']
    ok &= base['real-receipt'] == 'ACCEPTED' and base['gate-control'] == 'ACCEPTED'
    ok &= all('half the 49 ms' in v for k, v in base.items() if k.startswith('plant'))
    for name in PLANTS:
        if name != 'none':
            ok &= results[name]['gate-control'].startswith('REFUSED: receipt arm escaped')
    print('PROBE VERDICT:', 'EXPECTED' if ok else 'UNEXPECTED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
