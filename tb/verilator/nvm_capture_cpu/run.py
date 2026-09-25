#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build and measure the product CPU capture under continuous controller traffic."""
import argparse
import json
from pathlib import Path
import re
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[3]


def _compile(build_dir: Path, spec: dict) -> None:
    header = build_dir / 'probe_config.hpp'
    header.write_text('#pragma once\n#include <cstdint>\n' + ''.join(
        f'constexpr std::uint64_t {name} = {value};\n' for name, value in (
            ('sys_hz', spec['sys_hz']), ('cpu_hz', spec['cpu_hz']), ('tdm_hz', spec['tdm_hz']))))
    argv = ['verilator', '--cc', '--exe', '--build', '-j', '8', '-Wno-fatal', '-Werror-USERERROR',
            '-Wno-BLKANDNBLK', '-Wno-WIDTH', '-Wno-COMBDLY', '-Wno-CASEINCOMPLETE',
            '--top-module', 'sim', '--Mdir', str(build_dir / 'native'), '-O3',
            '--output-split', '5000', '--output-split-cfuncs', '500',
            '-CFLAGS', f'-O3 -std=c++17 -Wall -Wextra -I{ROOT}/tb/common -I{build_dir}',
            *['-I' + str(i) for i in spec['includes']], *spec['sources'],
            str(Path(__file__).with_name('sim_main.cpp'))]
    print('COMMAND', shlex.join(argv), flush=True)
    subprocess.run(argv, cwd=build_dir / 'gateware', check=True)


def _grade(build_dir: Path, spec: dict, returncode: int) -> None:
    raw = (build_dir / 'capture.log').read_text()
    rows = [dict((key, int(value)) for key, value in re.findall(r'(\w+)=(\d+)', line))
            for line in raw.splitlines() if line.startswith('CAPTURE index=')]
    if len(rows) != spec['captures'] or 'CAPTURE_DONE' not in raw:
        raise RuntimeError('not every requested capture completed')
    if spec['mutation'] != 'none':
        _grade_mutation(rows, spec['mutation'], returncode)
        return
    if returncode:
        raise RuntimeError(f'simulator exited {returncode}')
    expected = (12634, 156) if spec['shape'] == 'endstation_ax7101_8x8' else (3218, 53)
    for index, row in enumerate(rows):
        if (row['index'] != index or row['ok'] != 1 or row['mismatches'] or row['open']
                or (row['raw'], row['records']) != expected
                or not all(row[key] > 0 for key in ('sys_cycles', 'requests', 'responses', 'reads'))):
            raise RuntimeError(f'capture or concurrent traffic failed: {row}')
    elapsed = [row['sys_cycles'] / spec['sys_hz'] * 1000 for row in rows]
    summary = dict(shape=spec['shape'], captures=len(rows), sys_hz=spec['sys_hz'],
                   cpu_hz=spec['cpu_hz'], traffic='continuous READ_DESCRIPTOR ENTITY, MAC AXIS',
                   minimum_ms=min(elapsed), maximum_ms=max(elapsed),
                   hold_ms=50, margin=50 / max(elapsed), rows=rows)
    (build_dir / 'measurement.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2), flush=True)
    if max(elapsed) > 25:
        raise RuntimeError('worst measured copy exceeds half the 50 ms hold')


def _grade_mutation(rows: list[dict], mutation: str, returncode: int) -> None:
    for row in rows:
        if row['ok'] != 1 or row['open'] or row['sys_cycles'] <= 0:
            raise RuntimeError(f'mutation failed for an unrelated reason: {row}')
        if mutation == 'skip-copy':
            caught = row['mismatches'] == row['raw'] and returncode == 1
            caught = caught and all(row[key] > 0 for key in ('requests', 'responses', 'reads'))
        else:
            caught = not any(row[key] for key in ('requests', 'responses', 'reads', 'mismatches'))
            caught = caught and returncode == 0
        if not caught:
            raise RuntimeError(f'mutation escaped its named oracle: {row}')
    print(f'MUTATION {mutation}: caught by destination-byte or concurrent-traffic oracle; {len(rows)} captures')


def main() -> None:
    """Run in the existing product environment; install or download nothing."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shape', choices=['endstation_ax7101_8x8', 'endstation_ax7101_1x1_tdm8'],
                        required=True)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--captures', type=int, default=16)
    parser.add_argument('--build-only', action='store_true')
    parser.add_argument('--mutation', choices=['none', 'skip-copy', 'no-traffic'], default='none')
    args = parser.parse_args()
    if not 2 <= args.captures <= 256:
        parser.error('--captures must be between 2 and 256')
    args.build_dir = args.build_dir.resolve()
    if args.build_dir == ROOT or ROOT in args.build_dir.parents:
        parser.error('use an external scratch build directory')
    from soc import build
    build(args)
    spec = json.loads((args.build_dir / 'sources.json').read_text())
    _compile(args.build_dir, spec)
    if args.build_only:
        return
    argv = [str(args.build_dir / 'native/Vsim')]
    print('COMMAND', shlex.join(argv), flush=True)
    with (args.build_dir / 'capture.log').open('w') as log:
        result = subprocess.run(argv, cwd=args.build_dir / 'gateware', stdout=log,
                                stderr=subprocess.STDOUT, check=False)
    _grade(args.build_dir, spec, result.returncode)


if __name__ == '__main__':
    main()
