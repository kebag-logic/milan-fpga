#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The split CPU budget (#665 S2, #397 re-opened): measured cycles of every service path.

The test SoC (split_soc.py) runs the linked split image unmodified on the
shipping cacheless core, and sim_main.cpp drives its mailbox. Each group is
one boot and one stimulus script (scenario.py); grade.py reads the log. The
default refuses a probe that misses T_svc unless --record-budget-findings is
given; that option records the misses and still requires every probe to be
measured, so a missing or malformed observation always fails.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
POINTS = {'1x1': ('endstation_ax7101_1x1_tdm8', 1), '8x8': ('endstation_ax7101_8x8', 2)}


def run_group(build_dir: Path, out: Path, group: object, flash: str) -> Path:
    """One boot of the native model on the group's script; its whole output is the log."""
    script = out / f'{group.name}.txt'
    script.write_text(group.script())
    log = out / f'{group.name}.log'
    argv = [str(build_dir / 'native/Vsim'), str(script), flash]
    print('COMMAND', shlex.join(argv), flush=True)
    with log.open('w') as sink:
        subprocess.run(argv, cwd=build_dir / 'gateware', stdout=sink, stderr=subprocess.STDOUT, check=False)
    return log


def table(results: list[dict], point: str) -> str:
    """The Markdown rows of every probe, then the pass and access figures."""
    lines = [f'### {point}', '',
             '| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles '
             '| Mailbox accesses (model) | Fetch share |',
             '|---|---|---:|---:|---:|---:|---|---:|---:|---:|']
    for group in results:
        for r in group['probes']:
            if r['status'] != 'measured':
                cells = f"| {r['row']} | `{r['probe']}` | - | - | - | - | {r['status']}: {r['reason']} |"
                lines.append(cells + ' - | - | - |')
                continue
            verdict = 'fits' if r['within_t_svc'] else 'MISS T_svc' if r['within_ceiling'] else 'MISS ceiling'
            model = f" ({r['model_accesses']})" if 'model_accesses' in r else ''
            lines.append(f"| {r['row']} | `{r['probe']}` | {r['cpu_cycles']:,} | {r['ms']:.3f} | {r['t_svc_ms']:g} | "
                         f"{r['ceiling_ms']:g} | {verdict} | {r.get('pass_cycles', 0):,} | "
                         f"{r.get('pass_mbx_accesses', '-')}{model} | {r.get('pass_fetch_share', 0):.3f} |")
    return '\n'.join(lines) + '\n'


def arguments() -> tuple[argparse.ArgumentParser, argparse.Namespace]:
    """The command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--point', choices=sorted(POINTS))
    parser.add_argument('--build-dir', type=Path)
    parser.add_argument('--reuse-build', action='store_true')
    parser.add_argument('--groups', help='comma-separated group names; default every group')
    parser.add_argument('--out', type=Path, help='results directory; default <build-dir>/results')
    parser.add_argument('--jobs', type=int, default=8)
    parser.add_argument('--cpu-regions', choices=('cover', 'as-built'), default='cover')
    parser.add_argument('--record-budget-findings', action='store_true')
    parser.add_argument('--mutation', choices=('none', 'slow-adp-rx'), default='none',
                        help='build a planted firmware defect; only its control group runs and must be caught')
    parser.add_argument('--variant', choices=('none', 'answering-ports'), default='none',
                        help="the labelled second arm: the fixture's observation callbacks answer")
    parser.add_argument('--regrade', action='store_true',
                        help='grade the logs already in --out; refuse a group whose script '
                        'the scenario no longer makes')
    parser.add_argument('--self-test', action='store_true')
    return parser, parser.parse_args()


def select(parser: argparse.ArgumentParser, args: argparse.Namespace, groups: list) -> list:
    """The groups this run takes: a control's own, or those --groups names."""
    import scenario
    if args.cpu_regions == 'as-built':
        return scenario.boot_fault_groups()
    if args.mutation != 'none':
        if args.groups and args.groups != 'control':
            parser.error('a mutation runs only its control group')
        args.groups = 'control'
    if not args.groups:
        return groups
    wanted = args.groups.split(',')
    unknown = set(wanted) - {g.name for g in groups}
    if unknown:
        parser.error(f'unknown groups {sorted(unknown)}')
    return [g for g in groups if g.name in wanted]


def graded(groups: list, logs: list[Path], spec: dict, out: Path) -> tuple[list, list, list]:
    """Every group's grade, the refusals and the T_svc misses; each grade is written beside its log."""
    import grade
    results, refusals, misses = [], [], []
    for group, log in zip(groups, logs):
        try:
            result = grade.grade(log.read_text(), group, spec['sys_hz'], spec['cpu_hz'])
        except grade.Refusal as error:
            refusals.append(str(error))
            continue
        (out / f'{group.name}.json').write_text(json.dumps(result, indent=1) + '\n')
        results.append(result)
        for r in result['probes']:
            if r['status'] != 'measured':
                refusals.append(f"{r['probe']}: {r['status']}: {r['reason']}")
            elif not r['within_t_svc']:
                misses.append(f"{r['probe']}: {r['ms']:.3f} ms over T_svc {r['t_svc_ms']:g} ms")
    return results, refusals, misses


def verdict(args: argparse.Namespace, groups: list, refusals: list, misses: list) -> int:
    """The run's exit status: a control must be caught by name; a measurement must be complete."""
    if args.cpu_regions == 'as-built':
        caught = [r for r in refusals if 'trapped' in r and re.search(r'TRAP \d+ 0 1 ', r)]
        print(f'CONTROL as-built {"caught" if caught else "ESCAPED"}: an instruction access fault (cause 1)')
        return 0 if caught else 1
    if args.mutation != 'none':
        paths = [p.name for p in groups[0].probes if p.name.startswith('control.')]
        caught = [m for m in misses if m.split(':')[0] in paths]
        if refusals or not paths or len(caught) != len(paths):
            print(f'CONTROL {args.mutation} ESCAPED: {len(caught)} of {len(paths)} control paths missed T_svc')
            return 1
        print(f'CONTROL {args.mutation} caught: every control path missed T_svc')
        return 0
    if refusals:
        return 1
    return 1 if misses and not args.record_budget_findings else 0


def main() -> int:
    """Build or reuse a point, run its groups, grade them and write the tables."""
    parser, args = arguments()
    if args.self_test:
        import selftest
        return selftest.main([])
    if not args.point or not args.build_dir:
        parser.error('--point and --build-dir are required unless --self-test')
    build_dir = args.build_dir.resolve()
    if build_dir == ROOT or ROOT in build_dir.parents:
        parser.error('use an external scratch build directory')
    os.environ.setdefault('PYTHONHASHSEED', '0')
    import build as builder
    import scenario
    shape, n_if = POINTS[args.point]
    if args.reuse_build or args.regrade:
        spec = builder.reused(build_dir)
        if ((spec['shape'], spec['interfaces'], spec['cpu_regions'], spec['mutation'], spec['variant'])
                != (shape, n_if, args.cpu_regions, args.mutation, args.variant)):
            parser.error('the reused build is another point, CPU region set, mutation or variant')
    else:
        spec = builder.build(build_dir, shape, n_if, cpu_regions=args.cpu_regions, mutation=args.mutation,
                             variant=args.variant)
    groups = select(parser, args, scenario.all_groups(scenario.point(args.point, spec), spec))
    out = (args.out or build_dir / 'results').resolve()
    out.mkdir(parents=True, exist_ok=True)
    if args.regrade:
        groups = [g for g in groups if (out / f'{g.name}.log').exists()]
        stale = [g.name for g in groups if (out / f'{g.name}.txt').read_text() != g.script()]
        if stale:
            parser.error(f'the scenario no longer makes the recorded scripts of {stale}; rerun them')
        logs = [out / f'{g.name}.log' for g in groups]
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            logs = list(pool.map(lambda g: run_group(build_dir, out, g, '-'), groups))
    results, refusals, misses = graded(groups, logs, spec, out)
    (out / 'table.md').write_text(table(results, args.point))
    (out / 'results.json').write_text(json.dumps(dict(point=args.point, build=spec['executable_sha256'],
                                                      results=results, refusals=refusals, misses=misses),
                                                 indent=1) + '\n')
    for line in refusals:
        print('REFUSED', line)
    for line in misses:
        print('BUDGET', line)
    print(f'{len(results)} groups graded, {len(refusals)} refusals, {len(misses)} T_svc misses')
    return verdict(args, groups, refusals, misses)


if __name__ == '__main__':
    raise SystemExit(main())
