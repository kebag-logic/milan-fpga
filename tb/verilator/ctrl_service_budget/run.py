#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The split CPU budget (#665, #397 re-opened): measured cycles of every service path.

The test SoC (split_soc.py) runs the linked split image unmodified on the
split placement's core (--fetch-l1 none: the cacheless core), and
sim_main.cpp drives its mailbox. Each group is
one boot and one stimulus script (scenario.py); grade.py reads the log. The
default refuses a probe that misses its budget, min(T_svc, its family's
ceiling) (FR_NFR.md 3.4.1), unless --record-budget-findings is
given; that option records the misses and still requires every probe of
every selected group to be measured, so a missing log or script, or a
missing or malformed observation, always fails the run. Apart from the
rows, every work pass is held to the per-pass share (share.py): the
default refuses a pass over it even when every row fits, unless
--record-share-findings is given, which records them.

The CPU runs in the split placement's clock domain, sys, at the bus clock,
100 MHz (#665, owner decision 2026-10-30): build.json records its domain and
clock, a build or reused build whose CPU is anywhere else, the Milan clock
among them, is refused, and every table and the run's last lines name the
clock its figures are at.
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
    """fits (within its budget), MISS T_svc (over T_svc, within a looser ceiling), MISS ceiling (over the
    3.4.1 ceiling, the budget where it is tighter than T_svc), STARVED (never released) or NEVER ANSWERED
    (a command taken and dropped)."""
    if r.get('starved'):
        return 'STARVED: never released'
    if r.get('unanswered'):
        return 'NEVER ANSWERED'
    return 'fits' if r['within_budget'] else 'MISS T_svc' if r['within_ceiling'] else 'MISS ceiling'


def severity(r: dict) -> tuple[bool, float]:
    """A probe instance's place in its path's ordering: a record never released or a command
    never answered (unbounded) is worse than any measured time, then the time."""
    return bool(r.get('starved') or r.get('unanswered')), r['ms']


def windows(results: list[dict]) -> list[dict]:
    """Each composed window: its longest pass, whether it released its whole load, and what not."""
    return [dict(group=g['group'], **{k: g['passes']['composed'][k] for k in
                                      ('cycles', 'ms', 'passes', 'window_ms', 'events_held', 'serviced',
                                       'unreleased')})
            for g in results if g['passes'].get('composed')]


def composed_maximum(results: list[dict]) -> dict | None:
    """The composed maximum: the longest pass over every backlog row's window, each of which
    committed its defined load (grade.check_load refuses one that did not). A window that left
    records unreleased ran its passes without that work, so while any did, the figure is a lower
    bound. A run that did not include every backlog row names the rows not run, and its figure is
    partial: the longest pass of the windows it ran, not the composed maximum. The longest pass of
    the windows that released their whole load is given beside it."""
    import grade
    every = [w for w in windows(results) if w['group'] in grade.BACKLOG_ROWS]
    if not every:
        return None
    top = max(every, key=lambda w: w['cycles'])
    done = max((w for w in every if w['serviced']), key=lambda w: w['cycles'], default=None)
    not_run = [row for row in grade.BACKLOG_ROWS if row not in {w['group'] for w in every}]
    return dict(cycles=top['cycles'], ms=top['ms'], group=top['group'], windows=len(every),
                rows=len(grade.BACKLOG_ROWS), not_run=not_run, partial=bool(not_run),
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
            entry['misses'] += not r['within_budget']
            if entry['worst'] is None or severity(r) > severity(entry['worst']):
                entry['worst'] = dict(r, group=group['group'])
    return sorted(out.values(), key=lambda e: (e['path'], e['interface']))


def counts(results: list[dict]) -> dict[str, int]:
    """Budget misses counted per path and per probe instance."""
    worst = paths(results)
    return dict(paths=len(worst), path_misses=sum(1 for e in worst if e['misses']),
                instances=sum(e['instances'] for e in worst), instance_misses=sum(e['misses'] for e in worst))


def share_misses(results: list[dict]) -> list[str]:
    """Each group with a work pass over the per-pass share (grade.pass_share), apart from its rows."""
    out = []
    for g in results:
        s, worst = g['passes'].get('share'), g['passes'].get('worst')
        if s and s['over']:
            idle = s.get('idle_over', 0)
            out.append(f"{g['group']}: {s['over'] - idle} of {s['passes']} work passes over the per-pass share "
                       f"{s['ms']:.3f} ms ({s['cycles']:,} CPU cycles); the longest {worst['cycles']:,} "
                       f"({worst['ms']:.3f} ms)" + (f"; and {idle} run(s) of passes with no mailbox write, the "
                                                   f"longest {s['idle_longest']:,}" if idle else ''))
    return out


def stated_misses(results: list[dict]) -> list[str]:
    """Each pass given whole to a build or an aged step, and each round of THE RETRY, dearer than the cost THE RETRY's
    search counts from (whole_grade.held, round_grade.held); each pass's polls base and each of the polls' heavy items
    dearer than its stated cost (poll_grade.held)."""
    return ([f"{g['group']}: a {o['kind']} pass of {o['cycles']:,} CPU cycles, over its stated "
             f"{g['passes']['stated']['limits'][o['kind']]:,}"
             for g in results for o in g['passes'].get('stated', {}).get('over', [])] +
            [f"{g['group']}: a round of {o['notices']} notice(s) and {o['refused']} refused attempt(s), "
             f"{o['cycles']:,} CPU cycles, over its stated {o['limit']:,}"
             for g in results for o in g['passes'].get('rounds', {}).get('over', [])] +
            [f"{g['group']}: " + ("a pass's polls base of " if o['kind'] == 'base' else f"a {o['kind']} item of ")
             + f"{o['cycles']:,} CPU cycles, over its stated {g['passes']['polls']['limits'][o['kind']]:,}"
             for g in results for o in g['passes'].get('polls', {}).get('over', [])])


def saves(results: list[dict]) -> list[dict]:
    """Every group's timed save (save_grade.save_time), with its group."""
    return [dict(g['save'], group=g['group']) for g in results if g.get('save')]


def aged(results: list[dict]) -> list[dict]:
    """Each aged window (save_window.aged_window): its opening age, the aged steps among its records
    (save_grade.aged_window), and its tightest row, the one with the least margin to its budget."""
    out = []
    for g in results:
        window = g['passes'].get('composed') or {}
        if not window.get('aged'):
            continue
        rows = [r for r in g['probes'] if r.get('status') == 'measured' and 'budget_ms' in r]
        tight = min(rows, key=lambda r: r['budget_ms'] - r['ms'])
        out.append(dict(window['aged'], group=g['group'], row=tight['probe'], ms=tight['ms'],
                        budget_ms=tight['budget_ms'], margin_ms=round(tight['budget_ms'] - tight['ms'], 5)))
    return out


def aged_table(results: list[dict]) -> list[str]:
    """The aged windows' section of the table: each window's opening age, its aged steps, its tightest row."""
    rows = aged(results)
    if not rows:
        return []
    lines = ['', "Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): "
             "the aged steps among the window's records and after them (start after the window opened, CPU time, the "
             "step) and the window's tightest row:", '', "| Group | Age at opening | Aged steps among its records | "
             "After them | Tightest row | ms (budget) | Margin ms |", '|---|---:|---|---|---|---:|---:|']
    for a in rows:
        steps = ['; '.join(f"+{s['start_ms']:.3f} ms, {s['cycles']:,} ({s['ms']:.3f} ms), {s['kind']}"
                           for s in a.get(key, [])) or 'none' for key in ('among', 'after')]
        lines.append(f"| {a['group']} | {a['age']} | {steps[0]} | {steps[1]} | `{a['row']}` | {a['ms']:.3f} "
                     f"({a['budget_ms']:g}) | {a['margin_ms']:.3f} |")
    least = min(rows, key=lambda a: a['margin_ms'])
    lines += ['', f"Least margin over the aged windows: {least['margin_ms']:.3f} ms, `{least['row']}` at "
              f"{least['ms']:.3f} ms."]
    return lines


def save_misses(results: list[dict]) -> list[str]:
    """Each save not durable within its stated worst case (save_window.bound_ms), named by its group."""
    out = []
    for s in saves(results):
        if not s['within']:
            when = (f"durable {s['ms']:.3f} ms after its change" if s['ms'] is not None else
                    f"not durable {s['waited_ms']:.3f} ms after its change, when the run ended")
            out.append(f"{s['group']}: {when}, over its stated worst case {s['bound_ms']:,} ms")
    return out


def notices(results: list[dict]) -> list[dict]:
    """Every retried notice's row (notice_window.py), measured, with its group."""
    import notice_window
    return [dict(r, group=g['group']) for g in results for r in g['probes']
            if r.get('status') == 'measured' and r['path'][0] in (notice_window.PATH, notice_window.QUEUED)]


def notice_misses(results: list[dict], interfaces: int) -> list[str]:
    """Each retried notice committed later than its bound after its port's answer, at a point of that many
    interfaces: a failure whatever the options record, since the bound is the construction's (ctrl_loop.h, THE RETRY;
    aecp.h, aecp_mbx.h)."""
    import notice_window
    import scenario
    rows = notices(results)
    late = [f"{n['group']}: committed {n['ms']:.3f} ms after its port's answer, over its bound {n['budget_ms']:g} ms"
            for n in rows if not n['within_budget']]
    # a group that holds its load across the timers times an MRPDU they owe (mrpdu_grade.py)
    for g in results:
        if g['group'].startswith('notice-retried-') and not any(r['path'][0] == 'mrpdu' for r in g['probes']):
            late.append(f"{g['group']}: no timer-driven MRPDU under its load")
    # the first of a queue keeps its own bound, AECP_QUEUED_FIRST_MS (FR_NFR.md 3.4.1), and those behind it the queue's
    bound = notice_window.queued_first_ms(interfaces)
    for group in {n['group'] for n in rows if n['path'][0] == notice_window.QUEUED}:
        first = min(n['ms'] for n in rows if n['group'] == group)
        if first > bound:
            late.append(f"{group}: its first notice committed {first:.3f} ms after its port's answer, "
                        f'over its bound {bound:g} ms')
    return late


def notice_table(results: list[dict]) -> list[str]:
    """The retried notices' section of the table: each from its port's answer to its last recipient's commit."""
    rows = notices(results)
    if not rows:
        return []
    lines = ['', "Retried notices, from the port's answer to the last recipient's commit (notice_window.py; "
             'ctrl_loop.h, THE RETRY):', '', '| Group | ms | Bound ms | Recipients | Events held at the answer | '
             'Verdict |', '|---|---:|---:|---:|---:|---|']
    for n in rows:
        lines.append(f"| {n['group']} | {n['ms']:.3f} | {n['budget_ms']:g} | {n['fanout']['recipients']} | "
                     f"{n['ahead']} | {'within' if n['within_budget'] else 'OVER'} |")
    worst = max(rows, key=lambda n: n['ms'])
    lines += ['', f"Latest: {worst['ms']:.3f} ms, {worst['group']}."]
    return lines


def save_table(results: list[dict]) -> list[str]:
    """The saves' section of the table: each timed save against its stated worst case."""
    rows = saves(results)
    if not rows:
        return []
    lines = ['', "Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a "
             "save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):", '',
             '| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between '
             'flash steps, ms | Grandmaster flood | Verdict |', '|---|---:|---:|---:|---:|---:|---|---|']
    for s in rows:
        durable = f"{s['ms']:.3f}" if s['ms'] is not None else f"not by {s['waited_ms']:.3f}"
        gap = f"{s['longest_gap_ms']:.3f}" if s['longest_gap_ms'] is not None else '-'
        lines.append(f"| {s['group']} | {durable} | {s['bound_ms']:,} | {s['steps']} | {s.get('flight') or '-'} | "
                     f"{gap} | {'yes' if s['flooded'] else 'no'} | {'within' if s['within'] else 'OVER'} |")
    return lines


def step_table(results: list[dict]) -> list[str]:
    """The store's steps' section of the table: each group's passes that carry a step (save_grade.step_figures)."""
    rows = [(g['group'], g['passes']['steps']) for g in results if g['passes'].get('steps', {}).get('passes')]
    if not rows:
        return []
    lines = ['', "Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and "
             "its flash port's:", '', '| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |',
             '|---|---:|---:|---:|']
    for group, s in rows:
        lines.append(f"| {group} | {s['passes']} | {s['cycles']:,} ({s['ms']:.3f}) | "
                     f"{s['store_cycles']:,} ({s['store_ms']:.3f}) |")
    top = max((s for _, s in rows), key=lambda s: s['cycles'])
    store = max((s for _, s in rows), key=lambda s: s['store_cycles'])
    lines += ['', f"Longest pass that carries a step: {top['cycles']:,} CPU cycles ({top['ms']:.3f} ms), "
              f"{next(g for g, s in rows if s is top)}; longest step: {store['store_cycles']:,} "
              f"({store['store_ms']:.3f} ms), {next(g for g, s in rows if s is store)}."]
    return lines


def share_table(results: list[dict]) -> list[str]:
    """The per-pass share's section of the table: each group's work passes against it."""
    import share
    graded = [g for g in results if g['passes'].get('share')]
    shares = [g['passes']['share'] for g in graded]
    if not shares:
        return []
    lines = ['', f"Per-pass share (share.py): {share.bound_ms():g} ms over {share.SHARE_PASSES} passes, "
             f"{shares[0]['ms']:.3f} ms, {shares[0]['cycles']:,} CPU cycles. A work pass over it is a finding "
             'whatever the rows say.', '',
             '| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |',
             '|---|---:|---:|---:|---|']
    for g, s in zip(graded, shares):
        worst = g['passes']['worst']
        longest = f"{worst['cycles']:,} ({worst['ms']:.3f})" if worst else '-'
        if s.get('idle_over'):
            longest += f"; with no mailbox write {s['idle_longest']:,}"
        lines.append(f"| {g['group']} | {s['passes']} | {s['over']} | {longest} | "
                     f"{'OVER the share' if s['over'] else 'fits'} |")
    return lines


def table(results: list[dict], point: str, clock: str = '') -> str:
    """The clock, the Markdown rows of every path's worst instance, the composed windows, the
    per-pass share, then every probe, then the timeouts."""
    tally = counts(results)
    lines = [f'### {point}', '', *([f'Clock: {clock}.', ''] if clock else []),
             f"{tally['path_misses']} of {tally['paths']} paths and {tally['instance_misses']} of "
             f"{tally['instances']} probe instances miss their budget.", '',
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
              '| Group | Event records held at its opening | Window ms | Passes in it | '
              'Longest pass, CPU cycles (ms) | Load released | Unreleased |',
              '|---|---:|---:|---:|---:|---|---|']
    for w in windows(results):
        lines.append(f"| {w['group']} | {w['events_held']} | {w['window_ms']:.3f} | {w['passes']} | "
                     f"{w['cycles']:,} ({w['ms']:.3f}) | "
                     f"{'yes' if w['serviced'] else 'no'} | {w['unreleased'] or '-'} |")
    top = composed_maximum(results)
    if top:
        bound = f", a lower bound (load unreleased in {', '.join(top['unreleased'])})" if top['lower_bound'] else ''
        over = (f"{top['windows']} of {top['rows']} backlog windows, a partial figure ({', '.join(top['not_run'])} "
                'not run)' if top['partial'] else f"the {top['windows']} backlog windows")
        done = top['released']
        lines += ['', f"Composed maximum over {over}: "
                  f"{'at least ' if top['lower_bound'] else ''}{top['cycles']:,} CPU cycles ({top['ms']:.3f} ms), "
                  f"{top['group']}{bound}.",
                  'Over the windows that released their whole load only: '
                  + (f"{done['cycles']:,} ({done['ms']:.3f} ms), {done['group']}." if done else 'none.')]
    lines += share_table(results)
    lines += aged_table(results)
    lines += save_table(results)
    lines += notice_table(results)
    lines += step_table(results)
    lines += ['', '| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles '
              '| Mailbox accesses (model) | Fetch share |',
              '|---|---|---:|---:|---:|---:|---|---:|---:|---:|']
    for group in results:
        for r in group['probes']:
            if r['status'] != 'measured':
                cells = f"| {r['row']} | `{r['probe']}` | - | - | - | - | {r['status']}: {r['reason']} |"
                lines.append(cells + ' - | - | - |')
                continue
            model = f" ({r['model_accesses']})" if 'model_accesses' in r else ''
            lines.append(f"| {r['row']} | `{r['probe']}` | {r['cpu_cycles']:,} | {r['ms']:.3f} | {r['budget_ms']:g} | "
                         f"{r['ceiling_ms']:g} | {verdict_word(r)} | {r.get('pass_cycles', 0):,} | "
                         f"{r.get('pass_mbx_accesses', '-')}{model} | {r.get('pass_fetch_share', 0):.3f} |")
    timeouts = [f"- `{g['group']}`: {t}" for g in results for t in g['timeouts']]
    lines += ['', 'Bounded waits that timed out (the probe is graded on what the log holds):', '',
              *(timeouts or ['- none'])]
    return '\n'.join(lines) + '\n'


def summary(point: str, build: str, results: list[dict], refusals: list[str], misses: list[str],
            shares: list[str] = ()) -> dict:
    """results.json: every grade, every path's worst instance, the counts, the composed windows,
    the composed maximum the table renders, the refusals, the misses and the passes over the
    per-pass share (main adds the clock)."""
    return dict(point=point, build=build, results=results, paths=paths(results), counts=counts(results),
                windows=windows(results), composed_maximum=composed_maximum(results),
                refusals=refusals, misses=misses, share_misses=list(shares), saves=saves(results),
                save_misses=save_misses(results), aged=aged(results), notices=notices(results),
                notice_misses=notice_misses(results, POINTS[point][1]))


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
    parser.add_argument('--fetch-l1', default='split', metavar='split|none|SETSxWAYS',
                        help="the CPU's instruction cache: the split placement's own (default), none "
                        '(the cacheless CPU) or a test-only sweep point of 64-byte lines')
    parser.add_argument('--xip', action='store_true',
                        help='the labelled hybrid-XIP arm: the code past the reset entry executes from the '
                        'flash window behind the instruction cache')
    parser.add_argument('--record-budget-findings', action='store_true')
    parser.add_argument('--record-share-findings', action='store_true',
                        help='record a work pass over the per-pass share (share.py) instead of failing the run')
    parser.add_argument('--mutation', choices=('none', *builder.MUTATIONS), default='none',
                        help='build a planted firmware defect; only its control group runs and must be caught')
    parser.add_argument('--variant', choices=('none', *builder.VARIANTS), default='none',
                        help='a labelled test-code arm: answering-ports (the observation ports answer: the face '
                        "block's stream, avb and counters and the fixture's path), shutdown-entry (the SHUTDOWN "
                        "path's test-only input) or answering-later (the face block's stream observation answers "
                        "from NOW_MS notice_window.ANSWER_MS: the retried notice's row)")
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
    """Every group's grade, the refusals and the budget misses; each grade is written beside its log."""
    import grade
    results, refusals, misses = [], [], []
    for group, log in zip(groups, logs):
        try:
            result = grade.grade(log.read_text(), group, spec['sys_hz'], spec['cpu_hz'], spec['interfaces'])
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
                              f"at least {r['ms']:.3f} ms over its budget {r['budget_ms']:g} ms")
            elif not r['within_budget']:
                misses.append(f"{r['probe']}: {r['ms']:.3f} ms over its budget {r['budget_ms']:g} ms")
    return results, refusals, misses


#: The access faults #791's region decode raises: whichever access first meets a rom
#: address with bit 15 set, an instruction fetch (cause 1) or a load (cause 5).
AS_BUILT_CAUSES = (1, 5)


def as_built_faults(refusals: list) -> list:
    """The trap refusals that name an access fault of AS_BUILT_CAUSES."""
    causes = '|'.join(map(str, AS_BUILT_CAUSES))
    return [r for r in refusals if 'trapped' in r and re.search(rf'TRAP \d+ 0 ({causes}) ', r)]


def mrpdu_groups(misses: list[str]) -> set[str]:
    """The groups with a timer-driven MRPDU over its bound, from the run's misses (a probe's name starts with its
    group's)."""
    return {m.partition(':')[0].partition('.')[0] for m in misses if '.mrpdu.' in m.partition(':')[0]}


def verdict(args: argparse.Namespace, groups: list, refusals: list, misses: list, shares: list = (),
            late: list = ()) -> int:
    """The run's exit status: a control must be caught by name; a measurement must be complete, its saves
    durable within their stated worst case and its retried notices within their bound (late names each that is
    not, by its group), and its rows and its passes are each a failure unless their own option records them."""
    if args.cpu_regions == 'as-built':
        caught = as_built_faults(refusals)
        print(f'CONTROL as-built {"caught" if caught else "ESCAPED"}: an instruction or load access fault '
              f'(cause {" or ".join(map(str, AS_BUILT_CAUSES))})')
        return 0 if caught else 1
    import build as builder
    if args.mutation in builder.SHARE_CONTROLS:
        # caught where the share sees what the rows do not: a group with a pass over it and every row of its own
        # within its budget (a probe's name starts with its group's)
        over = [s.partition(':')[0] for s in shares]
        missed = {m.partition(':')[0].partition('.')[0] for m in misses}
        alone = [g for g in over if g not in missed]
        caught = bool(alone) and not refusals
        print(f'CONTROL {args.mutation} {"caught" if caught else "ESCAPED"}: {len(alone)} group(s) with a pass over '
              f'the per-pass share and every row within its budget, {len(over) - len(alone)} with a row over its '
              f'budget as well, {len(missed - set(over))} with a row over and no pass over, {len(refusals)} '
              f'refusal(s)')
        return 0 if caught else 1
    if args.mutation in builder.SAVE_CONTROLS:
        # caught where a save under input that leaves no pass empty is not durable within its stated worst case
        named = [m.partition(':')[0] for m in late]
        want = builder.MUTATIONS[args.mutation][3].split(',')
        caught = set(want) <= set(named) and not refusals
        print(f'CONTROL {args.mutation} {"caught" if caught else "ESCAPED"}: {len(named)} save(s) not durable within '
              f'their stated worst case ({", ".join(named) or "none"}), {len(refusals)} refusal(s)')
        return 0 if caught else 1
    if args.mutation in builder.AGED_CONTROLS:
        # caught where an aged window's row goes over its budget, each named by its group
        import save_window
        aged_groups = {g.name for g in groups if save_window.aged_age(g.name) is not None}
        # or where an aged window's aged step passes the cost the search counts from (whole_grade.held)
        stepped = {s.partition(':')[0] for s in late if ': a step pass of ' in s}
        named = sorted(({m.partition(':')[0].partition('.')[0] for m in misses} | stepped) & aged_groups)
        caught = bool(named) and not refusals and not shares
        print(f'CONTROL {args.mutation} {"caught" if caught else "ESCAPED"}: {len(named)} aged window(s) with a row '
              f'over its budget or an aged step over its stated cost ({", ".join(named) or "none"}), {len(shares)} '
              f'with a pass over the share, {len(refusals)} refusal(s)')
        return 0 if caught else 1
    if args.mutation in builder.NOTICE_CONTROLS:
        # caught where every group's retried notice is committed later than its bound, or not within its window at
        # all, each named by its group
        want = sorted(builder.MUTATIONS[args.mutation][3].split(','))
        unsent = [r for r in refusals if '.stream_info.' in r and ': no end: ' in r]
        named = sorted(({m.partition(':')[0] for m in late} | {r.partition('.')[0] for r in unsent}) & set(want))
        caught = named == want and len(unsent) == len(refusals)
        print(f'CONTROL {args.mutation} {"caught" if caught else "ESCAPED"}: {len(named)} of {len(want)} group(s) '
              f'with the retried notice later than its bound ({", ".join(named) or "none"}), {len(refusals)} '
              f'refusal(s)')
        return 0 if caught else 1
    if args.mutation in builder.SRP_CONTROLS:
        # caught where every group's longest timer-driven MRPDU is over its bound, each named by its group
        want = sorted(builder.MUTATIONS[args.mutation][3].split(','))
        named = sorted(mrpdu_groups(misses) & set(want))
        caught = named == want and not refusals
        print(f'CONTROL {args.mutation} {"caught" if caught else "ESCAPED"}: {len(named)} of {len(want)} group(s) '
              f'with a timer-driven MRPDU over its bound ({", ".join(named) or "none"}), {len(refusals)} refusal(s)')
        return 0 if caught else 1
    if args.mutation in builder.POLL_CONTROLS:
        # caught where every group the plant runs has a pass's polls base, or a heavy item, over its stated cost,
        # each named by its group (poll_grade.held)
        words = builder.POLL_CONTROLS[args.mutation]
        want = sorted(builder.MUTATIONS[args.mutation][3].split(','))
        named = sorted({s.partition(':')[0] for s in late if words in s} & set(want))
        caught = named == want and not refusals
        print(f'CONTROL {args.mutation} {"caught" if caught else "ESCAPED"}: {len(named)} of {len(want)} group(s) '
              f'with {words!r} over its stated cost ({", ".join(named) or "none"}), {len(refusals)} refusal(s)')
        return 0 if caught else 1
    if args.mutation != 'none':
        paths_ = [p.name for g in groups for p in g.probes if p.name.startswith('control.')]
        caught = [m for m in misses if m.split(':')[0] in paths_]
        if refusals or not paths_ or len(caught) != len(paths_):
            print(f'CONTROL {args.mutation} ESCAPED: {len(caught)} of {len(paths_)} control paths missed their budget')
            return 1
        print(f'CONTROL {args.mutation} caught: every control path missed its budget')
        return 0
    if refusals or not groups or late:
        return 1
    if shares and not args.record_share_findings:
        return 1
    return 1 if misses and not args.record_budget_findings else 0


def all_groups(point: object, spec: dict) -> list:
    """Every group of a point's build; the answering-later variant has only the retried notice's (notice_window)."""
    import notice_window
    import scenario
    if spec.get('variant') == 'answering-every-port':
        return notice_window.every_groups(point, spec)
    return notice_window.groups(point) if spec.get('variant') == 'answering-later' else scenario.all_groups(point, spec)


def selected(args: argparse.Namespace, shape: str, n_if: int) -> tuple:
    """What this run's build must be: point, CPU regions, mutation, variant, fetch L1 and arm. Its CPU
    clock is the split CPU's on the bus clock, which build.reused holds every build to."""
    return shape, n_if, args.cpu_regions, args.mutation, args.variant, args.fetch_l1, args.xip


def built_as(spec: dict) -> tuple:
    """What a build records it is, in selected()'s order; a build that records no fetch L1 is cacheless."""
    return (spec['shape'], spec['interfaces'], spec['cpu_regions'], spec['mutation'], spec['variant'],
            spec.get('fetch_l1', 'none'), spec.get('xip', False))


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
    import share
    shape, n_if = POINTS[args.point]
    if args.reuse_build or args.regrade:
        try:
            spec = builder.reused(build_dir)
        except (RuntimeError, OSError, KeyError, ValueError) as error:
            print(f'REFUSED {error}')
            return 1
        if built_as(spec) != selected(args, shape, n_if):
            parser.error('the reused build is another point, CPU region set, mutation, variant, fetch L1 or arm')
    else:
        try:
            spec = builder.build(build_dir, shape, n_if, mutation=args.mutation, variant=args.variant,
                                 core=builder.Core(args.cpu_regions, args.fetch_l1, args.xip))
        except builder.ClockRefusal as error:
            print(f'REFUSED {error}')
            return 1
    clock = builder.clock_line(spec)
    print('CLOCK', clock, flush=True)
    groups = select(parser, args, all_groups(scenario.point(args.point, spec), spec))
    out = (args.out or build_dir / 'results').resolve()
    out.mkdir(parents=True, exist_ok=True)
    absent: list[str] = []
    if args.regrade:
        groups, logs, absent = recorded(groups, out)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            logs = list(pool.map(lambda g: run_group(build_dir, out, g, spec.get('flash_image') or '-'), groups))
    results, refusals, misses = graded(groups, logs, spec, out)
    refusals = absent + refusals
    shares = share_misses(results)
    hz = dict(cpu_hz=spec['cpu_hz'], cpu_cd=spec.get('cpu_cd'), sys_hz=spec['sys_hz'], label=clock)
    (out / 'table.md').write_text(table(results, args.point, clock))
    record = dict(summary(args.point, spec['executable_sha256'], results, refusals, misses, shares), clock=hz)
    (out / 'results.json').write_text(json.dumps(record, indent=1) + '\n')
    for line in refusals:
        print('REFUSED', line)
    for line in misses:
        print('BUDGET', line)
    for line in shares:
        print('SHARE', line)
    late = save_misses(results)
    stepped = [(g['group'], g['passes']['steps']) for g in results if g['passes'].get('steps', {}).get('passes')]
    if stepped:
        group, top = max(stepped, key=lambda r: r[1]['cycles'])
        where, store = max(stepped, key=lambda r: r[1]['store_cycles'])
        print(f"STEPS {sum(s['passes'] for _, s in stepped)} passes carry the store's step; the longest "
              f"{top['cycles']:,} CPU cycles ({top['ms']:.3f} ms), {group}; the longest step {store['store_cycles']:,} "
              f"({store['store_ms']:.3f} ms), {where}")
    opened = aged(results)
    if opened:
        least = min(opened, key=lambda a: a['margin_ms'])
        print(f"AGED {len(opened)} windows opened with the step's age at its limit or one short of it, "
              f"{sum(len(a['among']) for a in opened)} aged steps among their records; the least margin "
              f"{least['margin_ms']:.3f} ms, {least['row']} at {least['ms']:.3f} ms")
    for s in saves(results):
        print('SAVE', f"{s['group']}:", f"durable {s['ms']:.3f} ms after its change" if s['ms'] is not None else
              f"not durable {s['waited_ms']:.3f} ms after its change", f"(stated worst case {s['bound_ms']:,} ms,",
              f"{s['steps']} steps, longest gap between flash steps {s['longest_gap_ms']} ms)",
              'within' if s['within'] else 'OVER')
    for n in notices(results):
        print('NOTICE', f"{n['group']}: committed {n['ms']:.3f} ms after its port's answer to the last of "
              f"{n['fanout']['recipients']} recipients (bound {n['budget_ms']:g} ms)",
              'within' if n['within_budget'] else 'OVER')
    tally = counts(results)
    passes = sum(g['passes']['share']['passes'] for g in results)
    idle = sum(g['passes']['share'].get('idle_over', 0) for g in results)
    over = sum(g['passes']['share']['over'] for g in results) - idle
    print(f'{len(results)} groups graded, {len(refusals)} refusals, {len(misses)} budget misses '
          f"({tally['instance_misses']} of {tally['instances']} probe instances, "
          f"{tally['path_misses']} of {tally['paths']} paths), {over} of {passes} work passes over the per-pass "
          f"share {share.share_ms():.3f} ms ({share.share_cycles(spec['cpu_hz']):,} CPU cycles)"
          + (f", and {idle} run(s) of passes with no mailbox write" if idle else ''))
    print('CLOCK', clock)
    stated = stated_misses(results)
    for line in stated:
        print('STATED', line)
    import build as builder
    return verdict(args, groups, refusals, misses, shares,
                   late + notice_misses(results, n_if)
                   + (stated if args.mutation in ('none', *builder.AGED_CONTROLS, *builder.POLL_CONTROLS) else []))


if __name__ == '__main__':
    raise SystemExit(main())
