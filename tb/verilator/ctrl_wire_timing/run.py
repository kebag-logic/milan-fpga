#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The split placement's wire timing in simulation (#665 S8, #868): build or reuse, run the draws, grade offline.

  run.py --point 1x1 --build-dir DIR [--draws N] [--reuse-build]
  run.py --build-dir DIR --regrade [--draws N]
  run.py --self-test

The build (wire_build.py) is once per point; every run reuses it. The run
writes the stimulus (wire_scenario.py) to DIR/results/wire.txt, runs the
native model with its log in DIR/results/wire.log and its exit status in
DIR/results/wire.status, and grades the log (wire_grade.py) into
DIR/results/results.json and table.md. --regrade grades the log a run left.
--self-test runs the grader's controls on synthetic logs, with no build.
Exit 0 is a pass, 1 a finding and 2 a refusal.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
#: The draws a run makes by default (each a bind, its probe and an unbind).
DRAWS = 16


def arguments() -> argparse.Namespace:
    """The command line (see the module's docstring)."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--point', choices=('1x1',))
    parser.add_argument('--build-dir', type=Path)
    parser.add_argument('--draws', type=int, default=DRAWS)
    parser.add_argument('--reuse-build', action='store_true')
    parser.add_argument('--regrade', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    return parser.parse_args()


def run_model(build_dir: Path, spec: dict, draws: int) -> Path:
    """The stimulus, the native model's run, its exit status saved beside its log."""
    import wire_scenario
    out = build_dir / 'results'
    out.mkdir(parents=True, exist_ok=True)
    point = wire_scenario.identity(spec)
    (out / 'wire.txt').write_text(wire_scenario.script(point, draws))
    log = out / 'wire.log'
    with log.open('w') as sink:
        status = subprocess.run([str(build_dir / 'native/Vsim'), str(out / 'wire.txt'), str(out / 'uart.txt'),
                                 str(wire_scenario.limit_ms(draws))], stdout=sink, stderr=subprocess.STDOUT,
                                check=False, cwd=build_dir / 'soc/gateware').returncode   # its ROM .init files
    (out / 'wire.status').write_text(f'{status}\n')
    return log


def main() -> int:
    """Build or reuse, run and grade one point; regrade a run; or the self-test."""
    args = arguments()
    if args.self_test:
        import wire_selftest
        return wire_selftest.main()
    if not args.build_dir:
        print('REFUSED: --build-dir is required')
        return 2
    build_dir = args.build_dir.resolve()
    if build_dir == ROOT or ROOT in build_dir.parents:
        print('REFUSED: use a build directory outside the checkout')
        return 2
    os.environ.setdefault('PYTHONHASHSEED', '0')
    import wire_build
    import wire_grade
    try:
        if args.reuse_build or args.regrade:
            spec = wire_build.reused(build_dir)
        elif not args.point:
            print('REFUSED: --point is required to build')
            return 2
        else:
            spec = wire_build.build(build_dir, args.point)
    except (RuntimeError, OSError, KeyError, ValueError) as error:
        print(f'REFUSED: {error}')
        return 2
    log = build_dir / 'results/wire.log'
    if args.regrade:
        if not log.is_file() or not (build_dir / 'results/wire.status').is_file():
            print('REFUSED: no log and saved status to regrade')
            return 2
    else:
        log = run_model(build_dir, spec, args.draws)
    status = int((build_dir / 'results/wire.status').read_text())
    if status:
        print(f'REFUSED: the native model exited {status}; see {log}')
        return 2
    return wire_grade.main([str(log), str(spec['sys_hz']), str(args.draws), str(spec['interfaces']),
                            str(build_dir / 'results/results.json')])


if __name__ == '__main__':
    raise SystemExit(main())
