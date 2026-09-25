#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Require new capture measurements when their census or clock inputs change.

Runs without a target compiler, simulator or LiteX installation. The builder
regenerates each shape's tables in a temporary directory. The explicit clock
override follows the bare-metal contract; the yaml clock is also pinned until
#565 reconciles it. This gate does not establish physical timing closure.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

import yaml

from nvm_contract import REC_HDR, Shape
import nvm_shape

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / 'tb/verilator/nvm_capture_cpu'
sys.path.insert(0, str(HARNESS))
import recipe  # noqa: E402
import run as capture  # noqa: E402


def current_inputs() -> dict:
    """Recompute all closed records, independent of materialized contents."""
    result = {}
    with tempfile.TemporaryDirectory(prefix='nvm-capture-census-') as tmp:
        for name in recipe.SHAPES:
            cfg = ROOT / 'configs' / (name + '.yaml')
            names, dc, spi, spo = nvm_shape.build(cfg, Path(tmp))
            shape = Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo)
            records = nvm_shape.inventory(shape, nvm_shape.binding_base())
            if any(record[2] is None for record in records):
                raise RuntimeError(f'{name}: record allocation overflow')
            clocks = yaml.safe_load(cfg.read_text())['board']['constraints']
            result[name] = dict(raw_bytes=sum(REC_HDR + row[3] for row in records),
                                records=len(records), cpu_hz=recipe.CPU_HZ,
                                configured_cpu_hz=clocks['milan_clk_hz'],
                                sys_hz=clocks['sys_clk_hz'])
    return result


def check_inputs(actual: dict, measured: dict) -> None:
    """Fail on any difference, including a smaller copy or a faster clock."""
    if actual != measured:
        raise RuntimeError('capture inputs changed; remeasure both arms: '
                           f'current={actual}, measured-for={measured}')


def check_receipt(receipt: dict, actual: dict) -> None:
    """Regrade every recorded capture and recompute each published maximum."""
    check_inputs(actual, receipt['measured_for'])
    firmware = ROOT / 'sw/firmware/milan_baremetal/milan_baremetal.c'
    if hashlib.sha256(firmware.read_bytes()).hexdigest() != receipt['product_firmware_sha256']:
        raise RuntimeError('product firmware changed; remeasure the copy')
    harness_hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in HARNESS.iterdir() if path.suffix in ('.py', '.cpp')}
    if harness_hashes != receipt['harness_sha256']:
        raise RuntimeError('measurement harness changed; refresh measured evidence')
    expected = {(shape, recipe.CPU_HZ, arm) for shape in recipe.SHAPES for arm in ('on', 'off')}
    expected.update((recipe.SHAPES[0], 100_000_000, arm) for arm in ('on', 'off'))
    arms = receipt['measurements']
    keys = [(arm['shape'], arm['cpu_hz'], arm['traffic']) for arm in arms]
    if len(keys) != len(expected) or set(keys) != expected:
        raise RuntimeError('receipt must contain exactly both arms at every required point')
    for arm in arms:
        source = actual[arm['shape']]
        if (arm['captures'] != 16 or arm['sys_hz'] != source['sys_hz']
                or arm['configured_cpu_hz'] != source['configured_cpu_hz']
                or arm['phase'] != 'aligned rising edges'):
            raise RuntimeError('receipt has an unmeasured clock, phase or capture count')
        summary = capture.grade_rows(arm['rows'], arm)
        for key, value in summary.items():
            if arm[key] != value:
                raise RuntimeError(f'receipt summary differs from rows: {key}')
        if any((row['raw'], row['records']) != (source['raw_bytes'], source['records'])
               for row in arm['rows']):
            raise RuntimeError('receipt rows differ from the generated census')
    maxima = []
    for shape, clock in sorted({key[:2] for key in keys}):
        group = [arm for arm in arms if (arm['shape'], arm['cpu_hz']) == (shape, clock)]
        worst = capture.maximum_ms(group)
        maxima.append(dict(shape=shape, cpu_hz=clock, maximum_ms=worst,
                           margin=recipe.HOLD_FLOOR_MS / worst))
    if receipt['maxima'] != maxima:
        raise RuntimeError('published maximum must include every traffic arm')


def timing_controls() -> None:
    """A slower OFF arm must set the maximum and must obey the time limit."""
    row = dict(index=0, ok=1, sys_cycles=2_400_000, raw=12634, records=156,
               mismatches=0, open=0, requests=1, responses=1, reads=1)
    spec = dict(shape=recipe.SHAPES[0], captures=1, sys_hz=100_000_000,
                cpu_hz=recipe.CPU_HZ, configured_cpu_hz=100_000_000,
                phase='aligned rising edges', traffic='on')
    on = capture.grade_rows([row], spec)
    off_row = dict(row, sys_cycles=2_440_000, requests=0, responses=0, reads=0)
    off_spec = dict(spec, traffic='off')
    off = capture.grade_rows([off_row], off_spec)
    if abs(capture.maximum_ms([on, off]) - 24.4) > 1e-9:
        raise RuntimeError('OFF timing omitted from maximum')
    # Exactly half the floor passes; one more system tick must fail.
    capture.grade_rows([dict(off_row, sys_cycles=2_450_000)], off_spec)
    try:
        capture.grade_rows([dict(off_row, sys_cycles=2_450_001)], off_spec)
    except RuntimeError as exc:
        if 'half the 49 ms' not in str(exc):
            raise
    else:
        raise RuntimeError('OFF timing limit was ignored')


def selftest(actual: dict) -> None:
    """Named controls alter each live input before the real comparison."""
    for name, field in (('bytes', 'raw_bytes'), ('records', 'records'),
                        ('clock', 'cpu_hz'), ('configured-clock', 'configured_cpu_hz'),
                        ('system-clock', 'sys_hz')):
        changed = deepcopy(actual)
        changed[recipe.SHAPES[0]][field] += 1
        try:
            check_inputs(changed, actual)
        except RuntimeError:
            print(f'CONTROL {name}: detected')
        else:
            raise RuntimeError(f'input control escaped: {name}')
    timing_controls()
    with patch.object(capture, 'maximum_ms', side_effect=ignore_off_timing):
        try:
            timing_controls()
        except RuntimeError as exc:
            if str(exc) != 'OFF timing omitted from maximum':
                raise
            print('CONTROL ignore-off-timing: detected planted grading change')
        else:
            raise RuntimeError('planted grading change escaped')
    print('CONTROL off-time-limit: boundary and one-tick-over detected')


def ignore_off_timing(arms: list[dict]) -> float:
    """Deliberately wrong grader, exercised only as a failing control."""
    return max(row['sys_cycles'] / arm['sys_hz'] * 1000
               for arm in arms if arm['traffic'] == 'on' for row in arm['rows'])


def main() -> int:
    """Run input and grading controls before checking the measured receipt."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutation', choices=['bytes', 'records', 'clock', 'ignore-off-timing'])
    args = parser.parse_args()
    try:
        actual = current_inputs()
        selftest(actual)
        if args.mutation == 'ignore-off-timing':
            with patch.object(capture, 'maximum_ms', side_effect=ignore_off_timing):
                timing_controls()
        elif args.mutation:
            field = {'bytes': 'raw_bytes', 'records': 'records', 'clock': 'cpu_hz'}[args.mutation]
            actual[recipe.SHAPES[0]][field] += 1
        receipt = json.loads((HARNESS / 'measurements.json').read_text())
        check_receipt(receipt, actual)
    except (RuntimeError, KeyError, ValueError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print('PASS: capture census, clocks, both timing arms and receipt agree')
    return 0


if __name__ == '__main__':
    sys.exit(main())
