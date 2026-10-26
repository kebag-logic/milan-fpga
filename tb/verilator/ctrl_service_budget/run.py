#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The split CPU budget (#665, #397 re-opened): measured cycles of every service path.

The test SoC (split_soc.py) runs the linked split image unmodified on the
shipping cacheless core, and sim_main.cpp drives its mailbox. Each group is
one boot and one stimulus script (scenario.py); grade.py reads the log. The
default refuses a probe that misses T_svc unless --record-budget-findings is
given; that option records the misses and still requires every probe of
every selected group to be measured, so a missing log or script, or a
missing or malformed observation, always fails the run.
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


def verdict_word(r: dict) -> str:
    """fits, MISS T_svc, MISS ceiling (over the 3.4.1 ceiling as well), STARVED (never released) or
    NEVER ANSWERED (a command taken and dropped)."""
    if r.get('starved'):
        return 'STARVED: never released'
    if r.get('unanswered'):
        return 'NEVER ANSWERED'
    return 'fits' if r['within_t_svc'] else 'MISS T_svc' if r['within_ceiling'] else 'MISS ceiling'


def severity(r: dict) -> tuple[bool, float]:
    """A probe instance's place in its path's ordering: a record never released or a command
    never answered (unbounded) is worse than any measured time, then the time."""
    return bool(r.get('starved') or r.get('unanswered')), r['ms']


def windows(results: list[dict]) -> list[dict]:
    """Each composed window: its longest pass, whether it released its whole load, and what not."""
    return [dict(group=g['group'], **{k: g['passes']['composed'][k] for k in
                                      ('cycles', 'ms', 'passes', 'window_ms', 'serviced', 'unreleased')})
            for g in results if g['passes'].get('composed')]


def composed_maximum(results: list[dict]) -> dict | None:
    """The composed maximum: the longest pass over every backlog row's window, each of which
    committed its defined load (grade.check_load refuses one that did not). A window that left
    records unreleased ran its passes without that work, so while any did, the figure is a lower
    bound. The longest pass of the windows that released their whole load is given beside it."""
    import grade
    every = [w for w in windows(results) if w['group'] in grade.BACKLOG_ROWS]
    if not every:
        return None
    top = max(every, key=lambda w: w['cycles'])
    done = max((w for w in every if w['serviced']), key=lambda w: w['cycles'], default=None)
    return dict(cycles=top['cycles'], ms=top['ms'], group=top['group'], windows=len(every),
                lower_bound=not all(w['serviced'] for w in every),
                unreleased=[w['group'] for w in every if not w['serviced']],
                released=dict(cycles=done['cycles'], ms=done['ms'], group=done['group']) if done else None)


def paths(results: list[dict]) -> list[dict]:
    """Every measured path's worst instance across the groups, with its instance and miss counts.

    A path is a probe's path and interface (scenario.Probe.path_key): the same
    path measured by several groups is one path, reported at its worst.
    """
    out: dict[tuple[str, int], dict] = {}
    for group in results:
        for r in group['probes']:
            if r['status'] != 'measured':
                continue
            entry = out.setdefault(tuple(r['path']), dict(path=r['path'][0], interface=r['path'][1], row=r['row'],
                                                          instances=0, misses=0, worst=None))
            entry['instances'] += 1
            entry['misses'] += not r['within_t_svc']
            if entry['worst'] is None or severity(r) > severity(entry['worst']):
                entry['worst'] = dict(r, group=group['group'])
    return sorted(out.values(), key=lambda e: (e['path'], e['interface']))


def counts(results: list[dict]) -> dict[str, int]:
    """T_svc misses counted per path and per probe instance."""
    worst = paths(results)
    return dict(paths=len(worst), path_misses=sum(1 for e in worst if e['misses']),
                instances=sum(e['instances'] for e in worst), instance_misses=sum(e['misses'] for e in worst))


def table(results: list[dict], point: str) -> str:
    """The Markdown rows of every path's worst instance, then every probe, then the timeouts."""
    tally = counts(results)
    lines = [f'### {point}', '',
             f"{tally['path_misses']} of {tally['paths']} paths and {tally['instance_misses']} of "
             f"{tally['instances']} probe instances miss T_svc.", '',
             '| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |',
             '|---|---:|---|---:|---|---:|---:|---:|']
    for e in paths(results):
        w = e['worst']
        bound = f" ({w['bound_ms']:.3f})" if 'bound_ms' in w else ''
        ms = f"at least {w['ms']:.3f}" if w.get('starved') or w.get('unanswered') else f"{w['ms']:.3f}"
        lines.append(f"| {e['row']} | {e['interface']} | `{w['probe']}` ({w['group']}) | {ms}{bound} | "
                     f"{verdict_word(w)} | {w['ahead']} {w['ring']} | {e['instances']} | {e['misses']} |")
    lines += ['', 'Composed windows: a window that left its load unreleased ran its passes without that work, so '
              'its longest pass is a lower bound.', '',
              '| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |',
              '|---|---:|---:|---:|---|---|']
    for w in windows(results):
        lines.append(f"| {w['group']} | {w['window_ms']:.3f} | {w['passes']} | {w['cycles']:,} ({w['ms']:.3f}) | "
                     f"{'yes' if w['serviced'] else 'no'} | {w['unreleased'] or '-'} |")
    top = composed_maximum(results)
    if top:
        bound = f", a lower bound (load unreleased in {', '.join(top['unreleased'])})" if top['lower_bound'] else ''
        done = top['released']
        lines += ['', f"Composed maximum over the {top['windows']} backlog windows: "
                  f"{'at least ' if top['lower_bound'] else ''}{top['cycles']:,} CPU cycles ({top['ms']:.3f} ms), "
                  f"{top['group']}{bound}.",
                  'Over the windows that released their whole load only: '
                  + (f"{done['cycles']:,} ({done['ms']:.3f} ms), {done['group']}." if done else 'none.')]
    lines += ['', '| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles '
              '| Mailbox accesses (model) | Fetch share |',
              '|---|---|---:|---:|---:|---:|---|---:|---:|---:|']
    for group in results:
        for r in group['probes']:
            if r['status'] != 'measured':
                cells = f"| {r['row']} | `{r['probe']}` | - | - | - | - | {r['status']}: {r['reason']} |"
                lines.append(cells + ' - | - | - |')
                continue
            model = f" ({r['model_accesses']})" if 'model_accesses' in r else ''
            lines.append(f"| {r['row']} | `{r['probe']}` | {r['cpu_cycles']:,} | {r['ms']:.3f} | {r['t_svc_ms']:g} | "
                         f"{r['ceiling_ms']:g} | {verdict_word(r)} | {r.get('pass_cycles', 0):,} | "
                         f"{r.get('pass_mbx_accesses', '-')}{model} | {r.get('pass_fetch_share', 0):.3f} |")
    timeouts = [f"- `{g['group']}`: {t}" for g in results for t in g['timeouts']]
    lines += ['', 'Bounded waits that timed out (the probe is graded on what the log holds):', '',
              *(timeouts or ['- none'])]
    return '\n'.join(lines) + '\n'


def arguments() -> tuple[argparse.ArgumentParser, argparse.Namespace]:
    """The command line."""
    import build as builder
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--point', choices=sorted(POINTS))
    parser.add_argument('--build-dir', type=Path)
    parser.add_argument('--reuse-build', action='store_true')
    parser.add_argument('--groups', help='comma-separated group names; default every group')
    parser.add_argument('--out', type=Path, help='results directory; default <build-dir>/results')
    parser.add_argument('--jobs', type=int, default=8)
    parser.add_argument('--cpu-regions', choices=('cover', 'as-built'), default='cover')
    parser.add_argument('--record-budget-findings', action='store_true')
    parser.add_argument('--mutation', choices=('none', *builder.MUTATIONS), default='none',
                        help='build a planted firmware defect; only its control group runs and must be caught')
    parser.add_argument('--variant', choices=('none', *builder.VARIANTS), default='none',
                        help="a labelled test-code arm: answering-ports (the fixture's observation callbacks "
                        'answer) or shutdown-entry (the SHUTDOWN path\'s test-only input)')
    parser.add_argument('--regrade', action='store_true',
                        help='grade the logs already in --out; a selected group whose script or log is '
                        'absent, or whose script the scenario no longer makes, is refused by name')
    parser.add_argument('--self-test', action='store_true')
    return parser, parser.parse_args()


def select(parser: argparse.ArgumentParser, args: argparse.Namespace, groups: list) -> list:
    """The groups this run takes: a control's own, or those --groups names."""
    import build as builder
    import scenario
    if args.cpu_regions == 'as-built':
        return scenario.boot_fault_groups()
    if args.mutation != 'none':
        _, _, _, control, variant = builder.MUTATIONS[args.mutation]
        if variant != args.variant:
            parser.error(f'mutation {args.mutation} needs --variant {variant}')
        if args.groups and args.groups != control:
            parser.error(f'a mutation runs only its control group, {control}')
        args.groups = control
    if not args.groups:
        return groups
    wanted = args.groups.split(',')
    unknown = set(wanted) - {g.name for g in groups}
    if unknown:
        parser.error(f'unknown groups {sorted(unknown)}')
    return [g for g in groups if g.name in wanted]


def recorded(groups: list, out: Path) -> tuple[list, list[Path], list[str]]:
    """For a regrade: the selected groups whose script and log are both present, their logs, and
    a refusal naming each group whose script or log is absent or whose script is stale."""
    kept, logs, refusals = [], [], []
    for g in groups:
        script, log = out / f'{g.name}.txt', out / f'{g.name}.log'
        if not script.is_file() or not log.is_file():
            refusals.append(f'{g.name}: no recorded {"script" if not script.is_file() else "log"} in the results')
        elif script.read_text() != g.script():
            refusals.append(f'{g.name}: the scenario no longer makes its recorded script; rerun it')
        else:
            kept.append(g)
            logs.append(log)
    return kept, logs, refusals


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
            elif r.get('starved') or r.get('unanswered'):
                misses.append(f"{r['probe']}: never {'released' if r.get('starved') else 'answered'}, "
                              f"at least {r['ms']:.3f} ms over T_svc {r['t_svc_ms']:g} ms")
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
        paths_ = [p.name for g in groups for p in g.probes if p.name.startswith('control.')]
        caught = [m for m in misses if m.split(':')[0] in paths_]
        if refusals or not paths_ or len(caught) != len(paths_):
            print(f'CONTROL {args.mutation} ESCAPED: {len(caught)} of {len(paths_)} control paths missed T_svc')
            return 1
        print(f'CONTROL {args.mutation} caught: every control path missed T_svc')
        return 0
    if refusals or not groups:
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
        try:
            spec = builder.reused(build_dir)
        except (RuntimeError, OSError, KeyError, ValueError) as error:
            print(f'REFUSED {error}')
            return 1
        if ((spec['shape'], spec['interfaces'], spec['cpu_regions'], spec['mutation'], spec['variant'])
                != (shape, n_if, args.cpu_regions, args.mutation, args.variant)):
            parser.error('the reused build is another point, CPU region set, mutation or variant')
    else:
        spec = builder.build(build_dir, shape, n_if, cpu_regions=args.cpu_regions, mutation=args.mutation,
                             variant=args.variant)
    groups = select(parser, args, scenario.all_groups(scenario.point(args.point, spec), spec))
    out = (args.out or build_dir / 'results').resolve()
    out.mkdir(parents=True, exist_ok=True)
    absent: list[str] = []
    if args.regrade:
        groups, logs, absent = recorded(groups, out)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            logs = list(pool.map(lambda g: run_group(build_dir, out, g, '-'), groups))
    results, refusals, misses = graded(groups, logs, spec, out)
    refusals = absent + refusals
    (out / 'table.md').write_text(table(results, args.point))
    (out / 'results.json').write_text(json.dumps(dict(point=args.point, build=spec['executable_sha256'],
                                                      results=results, paths=paths(results),
                                                      counts=counts(results), windows=windows(results),
                                                      composed_maximum=composed_maximum(results),
                                                      refusals=refusals, misses=misses), indent=1) + '\n')
    for line in refusals:
        print('REFUSED', line)
    for line in misses:
        print('BUDGET', line)
    tally = counts(results)
    print(f'{len(results)} groups graded, {len(refusals)} refusals, {len(misses)} T_svc misses '
          f"({tally['instance_misses']} of {tally['instances']} probe instances, "
          f"{tally['path_misses']} of {tally['paths']} paths)")
    return verdict(args, groups, refusals, misses)


if __name__ == '__main__':
    raise SystemExit(main())
