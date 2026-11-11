#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The split placement's wire timing in simulation (#665 S8, #868): build or reuse, run the draws, grade offline.

  run.py --point {1x1,8x8} --build-dir DIR [--draws N] [--seed S] [--load {none,composed}]
         [--announces K] [--out DIR] [--reuse-build]
  run.py --build-dir DIR --regrade [--out DIR]
  run.py --ci --build-dir DIR [--reuse-build]
  run.py --campaign --build-dir DIR --seed S --load {none,composed} --out DIR
  run.py --self-test

The build (wire_build.py) is once per point; every run reuses it. A run
writes the stimulus (wire_scenario.py) to OUT/wire.txt, runs the native model
with its log in OUT/wire.log and its exit status in OUT/wire.status, grades
the log (wire_grade.py) into OUT/results.json and table.md, and then grades
two planted copies of it, each of which must fail by its own words
(wire_selftest.plants): the log with one MAAP frame's egress delayed past the
11 ms reserve, and the log graded at a shifted clock (#868 item 4). OUT is
DIR/results/<load>-s<seed> unless given. --regrade grades the log a run left.

--ci is the CI step (#868 item 5): the grader's self-test, the 1x1 build, and
two runs at once, without load and with the composed load (CI_DRAWS draws
each, to the first ANNOUNCE: one acquisition's three probe intervals, its
ANNOUNCE's egress, the AECP response times and the ACMP round trips), each
graded with its plants; it prints the wall time. --campaign is one unit of
the local campaign: CAMPAIGN_DRAWS draws to the second ANNOUNCE, so one
B.3.4.1 announce interval and the Table 5.50 advertise periods inside it.
--self-test runs the grader's controls on synthetic logs, with no build.
Exit 0 is a pass, 1 a finding and 2 a refusal.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
#: The draws a run makes by default (each a bind, its probe, an unbind and an AEM command); the CI run's.
DRAWS = 16
CI_DRAWS = DRAWS


def arguments() -> argparse.Namespace:
    """The command line (see the module's docstring)."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--point', choices=('1x1', '8x8'))
    parser.add_argument('--build-dir', type=Path)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--draws', type=int)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--load', choices=('none', 'composed'), default='none')
    parser.add_argument('--announces', type=int)
    parser.add_argument('--reuse-build', action='store_true')
    parser.add_argument('--regrade', action='store_true')
    parser.add_argument('--ci', action='store_true')
    parser.add_argument('--campaign', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    return parser.parse_args()


def start_model(build_dir: Path, spec: dict, out: Path, run: dict) -> subprocess.Popen:
    """The stimulus and its parameters written, the native model started with its log in out/wire.log."""
    import wire_scenario
    out.mkdir(parents=True, exist_ok=True)
    point = wire_scenario.identity(spec)
    text = wire_scenario.script(point, run['draws'], run['seed'], run['load'] == 'composed', run['announces'])
    clash = wire_scenario.deadline_loads_clear(text)
    if clash:
        raise ValueError(f'the stimulus is refused: {clash[0]}')
    (out / 'run.json').write_text(json.dumps(run, indent=1) + '\n')
    (out / 'wire.txt').write_text(text)
    sink = (out / 'wire.log').open('w')
    return subprocess.Popen([str(build_dir / 'native/Vsim'), str(out / 'wire.txt'), str(out / 'uart.txt'),
                             str(wire_scenario.limit_ms(run['draws'], run['announces']))],
                            stdout=sink, stderr=subprocess.STDOUT, cwd=build_dir / 'soc/gateware')   # its ROM files


def finish_model(model: subprocess.Popen, out: Path) -> None:
    """The model's exit status saved beside its log."""
    (out / 'wire.status').write_text(f'{model.wait()}\n')


def graded(spec: dict, out: Path) -> int:
    """One run's grade and its plants: 0 a pass, 1 a finding or an escaped plant, 2 a refusal."""
    import wire_grade
    import wire_selftest
    status = int((out / 'wire.status').read_text())
    if status:
        print(f'REFUSED: the native model exited {status}; see {out / "wire.log"}')
        return 2
    run = json.loads((out / 'run.json').read_text())
    args = [str(spec['sys_hz']), str(run['draws']), str(spec['interfaces']), str(run['announces'])]
    print(f"== {out.name}: point {run['point']}, load {run['load']}, seed {run['seed']}, {run['draws']} draws, "
          f"to ANNOUNCE {run['announces']}")
    code = wire_grade.main([str(out / 'wire.log'), *args, str(out / 'results.json')])
    result = json.loads((out / 'results.json').read_text()) if (out / 'results.json').is_file() else None
    if result is not None:
        (out / 'table.md').write_text(wire_grade.table(result))
    escaped = wire_selftest.plants((out / 'wire.log').read_text(), spec['sys_hz'], run['draws'], spec['interfaces'],
                                   run['announces'])
    return code or (1 if escaped else 0)


def run_one(build_dir: Path, spec: dict, out: Path, run: dict) -> int:
    """One run: the model, then its grade."""
    model = start_model(build_dir, spec, out, run)
    finish_model(model, out)
    return graded(spec, out)


def built(build_dir: Path, point: str | None, reuse: bool) -> dict:
    """The build, made or reused."""
    import wire_build
    if reuse:
        return wire_build.reused(build_dir)
    if not point:
        raise ValueError('--point is required to build')
    return wire_build.build(build_dir, point)


def ci(build_dir: Path, reuse: bool) -> int:
    """The CI step (see the module's docstring)."""
    import wire_scenario
    import wire_selftest
    begun = time.monotonic()
    code = wire_selftest.main()
    spec = built(build_dir, '1x1', reuse)
    print(f'ctrl_wire_timing CI: build ready after {time.monotonic() - begun:.0f} s')
    runs = {load: dict(point='1x1', draws=CI_DRAWS, seed=0, load=load, announces=wire_scenario.CI_ANNOUNCES)
            for load in ('none', 'composed')}
    models = {load: start_model(build_dir, spec, build_dir / 'results' / f'ci-{load}', run)
              for load, run in runs.items()}
    for load, model in models.items():
        finish_model(model, build_dir / 'results' / f'ci-{load}')
    for load in runs:
        code = max(code, graded(spec, build_dir / 'results' / f'ci-{load}'))
    print(f'ctrl_wire_timing CI: {"PASS" if code == 0 else "FAIL"}, wall {time.monotonic() - begun:.0f} s')
    return code


def main() -> int:
    """Build or reuse, run and grade; regrade a run; the CI step; a campaign unit; or the self-test."""
    args = arguments()
    if args.self_test:
        import wire_selftest
        return wire_selftest.main()
    if not args.build_dir:
        print('REFUSED: --build-dir is required')
        return 2
    build_dir = args.build_dir.resolve()
    out_dirs = [build_dir] + ([args.out.resolve()] if args.out else [])
    if any(d == ROOT or ROOT in d.parents for d in out_dirs):
        print('REFUSED: use build and output directories outside the checkout')
        return 2
    os.environ.setdefault('PYTHONHASHSEED', '0')
    import wire_scenario
    try:
        if args.ci:
            return ci(build_dir, args.reuse_build)
        spec = built(build_dir, args.point, args.reuse_build or args.regrade or args.campaign)
    except (RuntimeError, OSError, KeyError, ValueError) as error:
        print(f'REFUSED: {error}')
        return 2
    if args.campaign:
        if not args.out:
            print('REFUSED: a campaign unit needs --out')
            return 2
        run = dict(point=spec['point'], draws=wire_scenario.CAMPAIGN_DRAWS, seed=args.seed, load=args.load,
                   announces=wire_scenario.CAMPAIGN_ANNOUNCES)
        return refusing(lambda: run_one(build_dir, spec, args.out.resolve(), run))
    out = args.out.resolve() if args.out else build_dir / 'results' / f'{args.load}-s{args.seed}'
    if args.regrade:
        if not (out / 'wire.log').is_file() or not (out / 'wire.status').is_file() or not (out / 'run.json').is_file():
            print(f'REFUSED: no log, saved status and run parameters to regrade in {out}')
            return 2
        return refusing(lambda: graded(spec, out))
    run = dict(point=spec['point'], draws=args.draws if args.draws is not None else DRAWS, seed=args.seed,
               load=args.load,
               announces=args.announces if args.announces is not None else wire_scenario.CI_ANNOUNCES)
    return refusing(lambda: run_one(build_dir, spec, out, run))


def refusing(step: Callable[[], int]) -> int:
    """A run or a regrade, its refusal (a stimulus refused, a log the grader cannot read) exit 2 on every path."""
    import wire_grade
    try:
        return step()
    except (ValueError, wire_grade.Refused) as error:
        print(f'REFUSED: {error}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
