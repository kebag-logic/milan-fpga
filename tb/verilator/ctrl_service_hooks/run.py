#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The F2-F5 timing hooks on the target core (#665): the eight NFR-SCOUT-03 hooks, measured and ordered.

The split platform's image (ctrl_plat_image.py), linked unmodified, runs on
the CPU budget harness's split SoC with the platform's CSR window
(hooks_soc.py). Every group is one boot and one stimulus script: the CPU
budget harness's groups, graded by its grader, and this harness's
(hooks.py). Each measured path is graded against its hook's bound,
min(T_svc, its family's ceiling) plus any normative wait, and its margin to
the family's normative timeout is recorded. Each hook's ordering check reads
the same logs, apart from the budget.

Exit 0 when every selected group was graded, every path was measured,
every ordering check that applied found nothing and, unless
--record-findings is given, every path is within its hook's bound by at
least the layout swing (hooks.LAYOUT_SWING_CYCLES); 1 otherwise. With
--plant, 0 when the plant's own words are found in its run and 1 when it
escapes. 2 refuses the command or the build.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import hooks_build  # noqa: E402
import hooks  # noqa: E402
import grade  # noqa: E402  the CPU budget harness's grader, read only
import scenario  # noqa: E402  its stimulus, read only

#: The groups whose paths run under the composed load: the CPU budget harness's backlog rows and this
#: harness's composed rows.
LOADED = (*grade.BACKLOG_ROWS, *hooks.composed_rows())


def run_group(build_dir: Path, out: Path, group: scenario.Group) -> Path:
    """One boot of the native model on the group's script; its whole output is the log."""
    script = out / f'{group.name}.txt'
    script.write_text(group.script())
    log = out / f'{group.name}.log'
    with log.open('w') as sink:
        subprocess.run([str(build_dir / 'native/Vsim'), str(script), '-'], cwd=build_dir / 'soc/gateware',
                       stdout=sink, stderr=subprocess.STDOUT, check=False)
    return log


def clock_label(spec: dict) -> str:
    """The CPU clock a run was measured at, labelled: `sys` is the product's split CPU clock (the owner's decision
    of 2026-10-30 on #665); `milan`, this base's wiring before it, is history and never the product's."""
    mhz = spec['cpu_hz'] / 1e6
    bus = f'bus {spec["sys_hz"] / 1e6:g} MHz'
    if spec['cpu_clock'] == hooks_build.CPU_CLOCKS[0]:
        return f'CPU {mhz:g} MHz on sys (the product split CPU clock), {bus}'
    return (f'CPU {mhz:g} MHz on the Milan clock (history: this base\'s wiring, not the product split CPU clock '
            f'of {spec["product_cpu_hz"] / 1e6:g} MHz), {bus}')


def hook_row(row: dict, group: str) -> dict:
    """One graded path with its hook, its bound, its verdict and its margin to the normative timeout."""
    hook = hooks.hook_of(row)
    bound = hooks.bound_ms(row['family']) + row['wait_ms']
    unbounded = bool(row.get('starved') or row.get('unanswered'))
    timeout = hooks.normative_ms(hook, row['family'])
    return dict(hook=hook, group=group, probe=row['probe'], path=row['path'][0], row=row['row'],
                interface=row['interface'],
                family=row['family'], ms=row['ms'], cpu_cycles=row['cpu_cycles'], wait_ms=row['wait_ms'],
                bound_ms=bound, within=not unbounded and row['ms'] <= bound, unbounded=unbounded,
                loaded=group in LOADED, normative_ms=timeout,
                margin_ms=round(timeout - row['wait_ms'] - row['ms'], 5), ahead=row.get('ahead', 0))


def held_row(held: dict, spec: dict) -> dict:
    """H-COUNTERS' held push as a path row (hooks.held_push)."""
    if held.get('missing'):
        return dict(hook='H-COUNTERS', group='hooks-counters', probe=held['probe'], path='counters.held',
                    row='GET_COUNTERS push, held '
                    '(H-COUNTERS)', interface=0, family='notify', ms=0.0, cpu_cycles=0, wait_ms=0.0,
                    bound_ms=hooks.bound_ms('notify'), within=False, unbounded=True, loaded=False,
                    normative_ms=hooks.COUNTERS_NORMATIVE_MS, margin_ms=0.0, ahead=0, missing=True)
    bound = hooks.bound_ms('notify')
    cycles = -(-(held['end'] - held['eligible']) * spec['cpu_hz'] // spec['sys_hz'])
    return dict(hook='H-COUNTERS', group='hooks-counters', probe=held['probe'], path='counters.held',
                row='GET_COUNTERS push, held until 1 s after the last departure, from its eligibility (H-COUNTERS)',
                interface=0, family='notify', ms=held['ms'], cpu_cycles=cycles, wait_ms=held['wait_ms'],
                bound_ms=bound, within=held['ms'] <= bound, unbounded=False, loaded=False,
                normative_ms=hooks.COUNTERS_NORMATIVE_MS,
                margin_ms=round(hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'] - held['ms'], 5), ahead=0)


def slack_cycles(r: dict, cpu_hz: int) -> int:
    """The CPU cycles a path has left to its bound, its bound in CPU cycles less its own; negative over it, and for
    a path never served."""
    if r['unbounded'] or r.get('missing'):
        return -1
    return round(r['bound_ms'] * cpu_hz / 1000) - r['cpu_cycles']


def grade_all(groups: list, logs: list[Path], spec: dict, out: Path) -> dict:
    """Every group's grade, path rows, ordering checks, refusals and findings."""
    rows, refusals, findings = [], [], []
    checks = {h: dict(applied=0, undecided=0, findings=[]) for h in hooks.HOOKS}
    unmeasured = []
    for group, log in zip(groups, logs):
        text = log.read_text()
        try:
            result = hooks.graded(text, group, spec)
        except grade.Refusal as error:
            refusals.append(str(error))
            continue
        (out / f'{group.name}.json').write_text(json.dumps(result, indent=1) + '\n')
        for r in result['probes']:
            if r['status'] != 'measured':
                unmeasured.append((r, group.name))
                continue
            rows.append(hook_row(r, group.name))
        held = hooks.held_push(text, group, spec)
        if held is not None:
            rows.append(held_row(held, spec))
        for hook, checked in hooks.ordering(text, group, spec).items():
            checks[hook]['applied'] += checked.applied
            checks[hook]['undecided'] += checked.undecided
            checks[hook]['findings'] += [f'{x} ({group.name})' for x in checked.findings]
    superseded = []
    for r, group in unmeasured:
        by = hooks.SUPERSEDED.get(r['path'][0])
        if by and any((x['group'], x['path'], x['interface']) == (by, *r['path']) for x in rows):
            superseded.append(f"{r['probe']} ({group}): {r['status']}: {r['reason']}; measured by {by}")
        else:
            refusals.append(f"{r['probe']}: {r['status']}: {r['reason']}")
    for r in rows:
        r['slack_cycles'] = slack_cycles(r, spec['cpu_hz'])
        if r.get('missing'):
            findings.append(f"LATE {r['hook']}: {r['probe']}: the held push was never sent")
        elif not r['within']:
            what = 'never served' if r['unbounded'] else f"{r['ms']:.3f} ms"
            findings.append(f"LATE {r['hook']}: {r['probe']}: {what} against its bound {r['bound_ms']:g} ms "
                            f"({r['group']})")
        elif r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES:
            findings.append(f"NARROW {r['hook']}: {r['probe']}: {r['ms']:.3f} ms, within its bound "
                            f"{r['bound_ms']:g} ms by {r['slack_cycles']:,} CPU cycles, under the layout swing of "
                            f"{hooks.LAYOUT_SWING_CYCLES:,} ({r['group']})")
    for hook, c in checks.items():
        findings += c['findings']
    return dict(rows=rows, refusals=refusals, superseded=superseded, findings=findings, checks=checks)


def summary(graded: dict) -> dict[str, dict]:
    """Each hook's worst path alone and under the composed load, its misses and its ordering check."""
    out = {}
    for name, hook in hooks.HOOKS.items():
        mine = [r for r in graded['rows'] if r['hook'] == name]
        worst = {}
        for loaded in (False, True):
            part = [r for r in mine if r['loaded'] == loaded]
            if part:
                top = max(part, key=lambda r: (r['unbounded'], r['ms'] - r['wait_ms']))
                worst['loaded' if loaded else 'alone'] = top
        check = graded['checks'][name]
        narrow = sum(r['within'] and r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES for r in mine)
        out[name] = dict(paths=len(mine), misses=sum(not r['within'] for r in mine), narrow=narrow, worst=worst,
                         ordering=hook.ordering, applied=check['applied'], undecided=check['undecided'],
                         ordering_findings=check['findings'], clauses=hook.clauses)
    return out


def cell(r: dict | None) -> str:
    """A table cell: ms (bound) and the path, or -."""
    if r is None:
        return '-'
    ms = 'never served' if r['unbounded'] else f"{r['ms']:.3f}"
    verdict = '' if r['within'] else ' **over its bound**'
    return f"{ms} ({r['bound_ms']:g}){verdict}, `{r['probe']}`, margin {r['margin_ms']:.1f} of {r['normative_ms']:g}"


def table(point: str, spec: dict, graded: dict) -> str:
    """The Markdown summary of one run: each hook, then every path, then the refusals and findings."""
    lines = [f'### {point}, {clock_label(spec)}, face arm {spec["arm"]}', '',
             '| Hook | Paths | Over its bound | Within it by less than the layout swing | Worst alone, ms (bound) '
             '| Worst under the composed load, ms (bound) | Ordering check applied (undecided) | Ordering findings |',
             '|---|---:|---:|---:|---|---|---:|---:|']
    for name, s in summary(graded).items():
        lines.append(f"| {name} | {s['paths']} | {s['misses']} | {s['narrow']} | {cell(s['worst'].get('alone'))} | "
                     f"{cell(s['worst'].get('loaded'))} | {s['applied']} ({s['undecided']}) | "
                     f"{len(s['ordering_findings'])} |")
    lines += ['', '| Hook | Path | Group | Interface | ms | CPU cycles | W ms | Bound ms | Within | Slack, CPU cycles '
              '| Under load | Margin to the normative timeout, ms |',
              '|---|---|---|---:|---:|---:|---:|---:|---|---:|---|---:|']
    for r in sorted(graded['rows'], key=lambda r: (r['hook'], r['probe'])):
        lines.append(f"| {r['hook']} | `{r['probe']}` | {r['group']} | {r['interface']} | "
                     f"{'never' if r['unbounded'] else format(r['ms'], '.3f')} | {r['cpu_cycles']:,} | "
                     f"{r['wait_ms']:g} | {r['bound_ms']:g} | {'yes' if r['within'] else 'NO'} | "
                     f"{r['slack_cycles']:,} | {'yes' if r['loaded'] else 'no'} | "
                     f"{r['margin_ms']:.3f} of {r['normative_ms']:g} |")
    lines += ['', 'Refusals:', '', *(f'- {x}' for x in graded['refusals'] or ['none']), '',
              'Probes of the CPU budget harness this harness measured again (hooks.SUPERSEDED):', '',
              *(f'- {x}' for x in graded['superseded'] or ['none']), '', 'Findings:', '',
              *(f'- {x}' for x in graded['findings'] or ['none'])]
    return '\n'.join(lines) + '\n'


def arguments() -> argparse.Namespace:
    """The command line."""
    parser = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    parser.add_argument('--point', choices=sorted(hooks_build.POINTS))
    parser.add_argument('--build-dir', type=Path)
    parser.add_argument('--cpu-clock', choices=hooks_build.CPU_CLOCKS, default=hooks_build.CPU_CLOCKS[0],
                        help='sys, the product split CPU clock, 100 MHz (default); or milan, this base\'s wiring '
                        'before the owner\'s decision of 2026-10-30, 50 MHz, history')
    parser.add_argument('--arm', choices=('idle', 'answering'), default='idle',
                        help='the face block: idle, as CtrlMailbox holds it (default), or the labelled answering '
                        'arm, whose CTR and GSI windows answer and whose counter-change event the script drives')
    parser.add_argument('--groups', help='comma-separated group names; default every group of the arm')
    parser.add_argument('--jobs', type=int, default=8)
    parser.add_argument('--out', type=Path, help='results directory; default <build-dir>/results')
    parser.add_argument('--reuse-build', action='store_true')
    parser.add_argument('--regrade', action='store_true', help='grade the logs already in --out')
    parser.add_argument('--record-findings', action='store_true',
                        help='record the paths over their bounds and still exit 0 when nothing else failed')
    parser.add_argument('--plant', choices=sorted(hooks.plants()),
                        help='build that planted defect at 1x1 and the product clock; run its group; it must be '
                        'caught by its own words')
    parser.add_argument('--self-test', action='store_true')
    return parser.parse_args()


def main() -> int:
    """Build or reuse, run, grade and tabulate one point; or one plant; or the self-test."""
    args = arguments()
    if args.self_test:
        import hooks_selftest
        return hooks_selftest.main()
    if not args.build_dir or not (args.point or args.plant):
        print('REFUSED: --build-dir and --point (or --plant) are required')
        return 2
    build_dir = args.build_dir.resolve()
    if build_dir == ROOT or ROOT in build_dir.parents:
        print('REFUSED: use an external scratch build directory')
        return 2
    os.environ.setdefault('PYTHONHASHSEED', '0')
    plant = hooks.plants()[args.plant] if args.plant else None
    point = '1x1' if plant else args.point
    arm = plant[1].arm if plant else args.arm
    clock = hooks_build.CPU_CLOCKS[0] if plant else args.cpu_clock
    try:
        if args.reuse_build or args.regrade:
            spec = hooks_build.reused(build_dir)
            want = (point, arm, clock, [list(e) for e in plant[1].edits] if plant else None)
            if (spec['point'], spec['arm'], spec['cpu_clock'], spec['plant']) != want:
                print('REFUSED: the reused build is another point, arm, clock or plant')
                return 2
        else:
            spec = hooks_build.build(build_dir, point, arm, clock, plant[1].edits if plant else None)
    except (RuntimeError, OSError, KeyError, ValueError) as error:
        print(f'REFUSED: {error}')
        return 2
    p = scenario.point(point, spec)
    groups = hooks.groups(p, spec)
    wanted = [plant[1].group] if plant else (args.groups.split(',') if args.groups else None)
    if wanted:
        unknown = set(wanted) - {g.name for g in groups}
        if unknown:
            print(f'REFUSED: unknown groups {sorted(unknown)}')
            return 2
        groups = [g for g in groups if g.name in wanted]
    out = (args.out or build_dir / 'results').resolve()
    out.mkdir(parents=True, exist_ok=True)
    if args.regrade:
        stale = [g.name for g in groups if not (out / f'{g.name}.log').is_file()
                 or (out / f'{g.name}.txt').read_text() != g.script()]
        if stale:
            print(f'REFUSED: no current log or script for {stale}')
            return 2
        logs = [out / f'{g.name}.log' for g in groups]
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            logs = list(pool.map(lambda g: run_group(build_dir, out, g), groups))
    graded = grade_all(groups, logs, spec, out)
    label = clock_label(spec)
    (out / 'table.md').write_text(table(point, spec, graded))
    (out / 'results.json').write_text(json.dumps(dict(point=point, clock=label, cpu_clock=spec['cpu_clock'],
                                                      cpu_hz=spec['cpu_hz'],
                                                      sys_hz=spec['sys_hz'], arm=spec['arm'], plant=args.plant,
                                                      build=spec['executable_sha256'], t_svc_ms=hooks.T_SVC_MS,
                                                      summary=summary(graded), **graded), indent=1) + '\n')
    for line in graded['refusals']:
        print('REFUSED', line)
    for line in graded['findings']:
        print('FINDING', line)
    print(f'{point}, {label}, face arm {spec["arm"]}: {len(groups)} groups, {len(graded["rows"])} paths, '
          f'{len(graded["refusals"])} refusals, {len(graded["findings"])} findings')
    if plant:
        words = plant[1].words
        caught = [x for x in graded['findings'] if x.startswith(words + ':')]
        found = caught[0] if caught else f'{words} not found'
        print(f'PLANT {args.plant} {"caught" if caught else "ESCAPED"}: {found}')
        return 0 if caught else 1
    unapplied = [h for h, c in graded['checks'].items() if not c['applied']]
    if unapplied and not wanted:
        print(f'ORDERING not applied for {unapplied}')
    orders = [x for x in graded['findings'] if x.startswith('ORDER ')]
    lates = [x for x in graded['findings'] if x.startswith(('LATE ', 'NARROW '))]
    if graded['refusals'] or orders or (lates and not args.record_findings):
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
