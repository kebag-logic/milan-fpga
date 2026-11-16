#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The rows the egress decides, held to their ledger (#894, #872; FR_NFR.md 3.4.1; SPLIT_CONTROL_MEMORY.md section 13).

backlog-owed's seven rows are set by the scenario's 60 ms egress hold, which no CPU lever moves: they miss their
budget at every point, and stay recorded misses by their row names and figures, not passing, since 3.4.1 charges TX
backpressure to the service budget. A new or larger miss fails the leg (#894's held-egress ruling, item (a)), so:
- a measured instance of a ledger row over its figure fails, by as little as one cycle of the bus, whatever its name;
- a ledger row with no measured instance fails, and so does any instance not measured, or never released or answered;
- a budget miss of any other row is new, and fails.

The ledger is derived at 8x8/1if, the one point that has one (#894's ledger ruling, items 2 and
3): each row's figure is the scenario's egress hold (HOLD_MS, read from scenario.py's backlog-owed group) plus the
service behind it at its measurement (MEASURED, the larger of two images') plus 5 %, rounded up to 0.01 ms (figure).
Section 13's table states those figures, and the self-test holds the two together and the derivation to the rule.
The tool reads the harness's own output: a results directory's group grades (run.py's <group>.json), whose ms is the
bus cycles' time to 10 ns, one cycle at 100 MHz, beside its run's results.json, whose refusals fail; or a run's log,
whose BUDGET lines name every instance over its budget to 1 us, so a ledger row read there is held at the most its
figure can be, and one printed at its ledger figure fails. A log must end in its run's summary, with no refusal and as
many budget misses as BUDGET lines.

usage: python3 -I egress_ledger.py --point 8x8-1if PATH ...   (each PATH a results directory or a run's log)
       python3 -I egress_ledger.py --selftest
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DOC = ROOT / 'docs/design/SPLIT_CONTROL_MEMORY.md'
#: The group whose rows the egress decides (scenario.py, backlog-owed).
GROUP = 'backlog-owed'
#: Units of a figure: 10 ns, one cycle of the 100 MHz bus, the resolution of a grade's ms (grade.py rounds it to 5
#: places), and half a log's printed microsecond in those units.
PER_MS, LOG_HALF = 100_000, 50
SCENARIO = HERE / 'scenario.py'
#: The hold the egress decides the rows by: backlog-owed's wait with the egress held before it is released
#: ('txready 1'), in ms, as scenario.py states it.
HOLD = re.compile(r"f'wait cycles \{(\d+) \* MS\}', 'mark room', 'txready 1'")


def hold_ms(text: str | None = None) -> int:
    """The scenario's egress hold in ms, read from scenario.py's backlog-owed group (or a planted copy's text)."""
    found = HOLD.findall(text if text is not None else SCENARIO.read_text())
    if len(found) != 1:
        raise ValueError(f'scenario.py states the egress hold {len(found)} times, not once')
    return int(found[0])


HOLD_MS = hold_ms()
#: Each row's measurement at 8x8/1if, arm A's backlog-owed, in ms to 10 ns: on the image that merges #902's 234bc149
#: (a15345f7's; #894's ledger ruling, item 2), and on the image that merges dev-soft-core 70f4056f (#901, d1c9023b's).
MERGED = {'backlog.owed.if0': 63.23710, 'backlog.owed_behind0.if0': 63.45889, 'backlog.owed_behind1.if0': 63.73898,
          'backlog.owed_behind2.if0': 63.95746, 'backlog.owed_behind3.if0': 64.19076,
          'backlog-owed.service.acmp.last.if0': 62.18386, 'backlog-owed.service.aecp.last.if0': 61.84625}
COMPOSED = {'backlog.owed.if0': 63.67337, 'backlog.owed_behind0.if0': 63.90106, 'backlog.owed_behind1.if0': 64.14858,
            'backlog.owed_behind2.if0': 64.38819, 'backlog.owed_behind3.if0': 64.62511,
            'backlog-owed.service.acmp.last.if0': 62.49045, 'backlog-owed.service.aecp.last.if0': 61.75319}
#: The measurement each figure derives from, the larger of the two (#894's ruling of 2026-11-16 on the composition
#: with #901, item 1): the six rows that grew there at their composed measurement, service.aecp.last, which shrank,
#: at the merged image's.
MEASURED = {'8x8-1if': {row: max(MERGED[row], COMPOSED[row]) for row in MERGED}}


def figure(measured_ms: float, hold: int = HOLD_MS) -> float:
    """A row's ledger figure: the hold plus the service behind it, its measurement less the hold, plus 5 %, rounded
    up to 0.01 ms; in 10 ns units throughout, so no float rounds it."""
    service = round(measured_ms * PER_MS) - hold * PER_MS
    served = -(-service * 105 // 100)
    return round(hold + -(-served // (PER_MS // 100)) / 100, 2)


#: Each point's ledger: every row the egress decides and the figure its miss may reach, in ms, derived (figure).
LEDGER = {point: {row: figure(ms) for row, ms in rows.items()} for point, rows in MEASURED.items()}
BUDGET_LINE = re.compile(r'^BUDGET (\S+): (?:never (?:released|answered), at least )?([\d.]+) ms over its budget '
                         r'([\d.]+) ms')
SUMMARY = re.compile(r'^(\d+) groups graded, (\d+) refusals, (\d+) budget misses')


def units(ms: float) -> int:
    """A figure in 10 ns units."""
    return round(ms * PER_MS)


def most(p: dict) -> int:
    """The most an instance can be, in 10 ns units: its grade's figure, or its log's printed figure and half its
    printed unit."""
    return units(p['ms']) + (0 if p['exact'] else LOG_HALF)


def over(p: dict, figure: float) -> bool:
    """An instance over its ledger figure, or a log's not shown within it."""
    return most(p) > units(figure)


def new_miss(p: dict) -> bool:
    """A budget miss of a row the ledger does not hold."""
    return not p['within_budget']


def from_results(path: Path) -> list[dict]:
    """Every instance of a results directory's group grades (run.py's <group>.json; results.json is the run's)."""
    out = []
    for f in sorted(path.glob('*.json')):
        g = json.loads(f.read_text())
        if f.name == 'results.json' or 'probes' not in g:
            continue
        out += [dict(group=g['group'], probe=p['probe'], status=p.get('status'), ms=p.get('ms'), exact=True,
                     within_budget=p.get('within_budget', True), budget_ms=p.get('budget_ms'),
                     never=bool(p.get('starved') or p.get('unanswered'))) for p in g['probes']]
    return out


def from_log(path: Path) -> tuple[list[dict], list[str]]:
    """A run's log: an instance for each BUDGET line, its group unnamed, and the log's own findings."""
    text = path.read_text(errors='replace').splitlines()
    out, refusals = [], []
    for line in text:
        m = BUDGET_LINE.match(line)
        if m:
            out.append(dict(group=None, probe=m[1], status='measured', ms=float(m[2]), exact=False,
                            within_budget=False, budget_ms=float(m[3]), never=' never ' in line))
        elif line.startswith('BUDGET '):
            refusals.append(f'{path.name}: a BUDGET line not in the harness\'s form: {line!r}')
    summary = [SUMMARY.match(line) for line in text if SUMMARY.match(line)]
    if len(summary) != 1:
        refusals.append(f'{path.name}: {len(summary)} run summaries, not one: the run did not end, or two are mixed')
    else:
        s = summary[0]
        if int(s[2]):
            refusals.append(f'{path.name}: the run refused {s[2]} (an instance not measured)')
        if int(s[3]) != len(out):
            refusals.append(f'{path.name}: {len(out)} BUDGET lines for the run\'s {s[3]} budget misses')
    return out, refusals


def run_refusals(path: Path) -> list[str]:
    """A results directory's run's refusals (its results.json, run.py's summary): a group the harness refused has no
    grade of its own, so a directory whose run refused, or that carries no results.json, cannot show every instance
    measured."""
    summary = path / 'results.json'
    if not summary.is_file():
        return [f"{path.name}: no results.json, so its run's refusals are not read (an instance not measured)"]
    refused = json.loads(summary.read_text()).get('refusals') or []
    return [f'{path.name}: the run refused {len(refused)} (an instance not measured): {refused[0]}'] if refused else []


def read(paths: list[Path]) -> tuple[list[dict], list[str], bool]:
    """The instances of every path, the readers' findings, and whether any path is a log."""
    instances, findings, logs = [], [], False
    for path in paths:
        if path.is_dir():
            got = from_results(path)
            if not got:
                findings.append(f'{path.name}: no group grade')
            instances, findings = instances + got, findings + run_refusals(path)
        elif path.is_file():
            got, refusals = from_log(path)
            instances, findings, logs = instances + got, findings + refusals, True
        else:
            findings.append(f'{path}: neither a results directory nor a log')
    return instances, findings, logs


def is_row(p: dict, ledger: dict) -> bool:
    """An instance of a ledger row: its name, in the group that has it (a log names no group)."""
    return p['probe'] in ledger and p['group'] in (GROUP, None)


def unseen(ledger: dict, seen: dict, logs: bool) -> list[str]:
    """Each ledger row with no measured instance."""
    return [f'{name}: no measured instance of the ledger row' + (
        ' (a log names only the instances over their budget)' if logs else '') for name in ledger if not seen[name]]


def findings(instances: list[dict], point: str, logs: bool = False) -> list[str]:
    """What fails the leg at a point: a ledger row over its figure, one not measured, an instance not measured or never
    released or answered, and a new budget miss."""
    ledger = LEDGER[point]
    out, seen = [], {name: [] for name in ledger}
    for p in instances:
        where = f"{p['probe']} ({p['group'] or 'a log'})"
        if p['status'] != 'measured':
            out.append(f'{where}: not measured ({p["status"]}), so a new or larger miss is not ruled out')
        elif is_row(p, ledger):
            seen[p['probe']].append(p)
            figure = ledger[p['probe']]
            if p['never']:
                out.append(f'{where}: never released or answered, at least {p["ms"]:.5f} ms, so not within its ledger '
                           f'figure {figure} ms')
            elif over(p, figure):
                out.append(f'{where}: {most(p) / PER_MS:.5f} ms' + ('' if p['exact'] else ' at most, by its log') +
                           f', over its ledger figure {figure} ms by {(most(p) - units(figure)) / PER_MS:.5f} ms: a '
                           'larger miss')
        elif p['never'] or new_miss(p):
            out.append(f'{where}: a new budget miss, {p["ms"]:.5f} ms against its budget {p["budget_ms"]} ms')
    return out + unseen(ledger, seen, logs)


def table(instances: list[dict], point: str) -> list[str]:
    """Each ledger row's worst measured instance against its figure."""
    rows = ['| Row the egress decides | Measured, ms | Ledger, ms | Difference, ms | Within |',
            '|---|---:|---:|---:|---|']
    for name, figure in LEDGER[point].items():
        ps = [p for p in instances if p['status'] == 'measured' and is_row(p, LEDGER[point]) and p['probe'] == name]
        if not ps:
            rows.append(f'| `{name}` | not measured | {figure} | | no |')
            continue
        p = max(ps, key=most)
        shown = f"{p['ms']:.5f}" if p['exact'] else f"{p['ms']:.3f} (log)"
        rows.append(f'| `{name}` | {shown} | {figure} | {(most(p) - units(figure)) / PER_MS:+.5f} | '
                    f'{"no" if over(p, figure) or p["never"] else "yes"} |')
    return rows


def main(argv: list[str] | None = None) -> int:
    """Grade the paths at a point, or run the self-test."""
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--point', choices=sorted(LEDGER))
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('paths', nargs='*', type=Path)
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.point or not args.paths:
        parser.error('--point and at least one PATH, or --selftest')
    instances, found, logs = read(args.paths)
    found += findings(instances, args.point, logs)
    measured = sum(p['status'] == 'measured' for p in instances)
    print(f'# {args.point}: the rows the egress decides against their ledger; {len(instances)} instance(s) read '
          f'({measured} measured) from {len(args.paths)} path(s)' + (', a log among them' if logs else ''))
    print('\n'.join(table(instances, args.point)))
    print('RESULT: ' + ('FAIL\n' + '\n'.join(f'- {f}' for f in found) if found else
                        'PASS: no ledger row over its figure, every one measured, no new budget miss'))
    return 1 if found else 0


# ---- the self-test -----------------------------------------------------------------------------------------------

#: Section 13's table of the rows the egress decides at 8x8/1if: the row, the measurement at 716a8ae7, the merged
#: image's, the composed image's, and the ledger figure derived from the larger of those two.
DOC_HEAD = ('| Row the egress decides (at 8x8/1if) | Measured at 716a8ae7, ms | '
            'Measured on #902\'s 234bc149 merged, ms | Measured on dev-soft-core 70f4056f composed, ms '
            '| Ledger, ms |')


def doc_ledger(text: str) -> tuple[dict[str, float], dict[str, float]]:
    """Section 13's table of the rows the egress decides at 8x8/1if: each row's ledger figure and the measurement it
    derives from."""
    merged, composed = doc_measurements(text)
    block = text.split(DOC_HEAD, 1)[1].split('\n\n', 1)[0]
    rows = re.findall(r'^\| `([^`]+)` \| [\d.]+ \| [\d.]+ \| [\d.]+ \| ([\d.]+) \|$', block, re.M)
    return {n: float(f) for n, f in rows}, {n: max(merged[n], composed[n]) for n, _ in rows}


def doc_measurements(text: str) -> tuple[dict[str, float], dict[str, float]]:
    """Section 13's table's two measurements of each row: the merged image's and the composed image's."""
    block = text.split(DOC_HEAD, 1)[1].split('\n\n', 1)[0]
    rows = re.findall(r'^\| `([^`]+)` \| [\d.]+ \| ([\d.]+) \| ([\d.]+) \| [\d.]+ \|$', block, re.M)
    return {n: float(m) for n, m, _ in rows}, {n: float(c) for n, _, c in rows}


def grade_dir(base: Path, name: str, figures: dict[str, float], extra: tuple[dict, ...] = (),
              status: dict[str, str] | None = None, never: tuple[str, ...] = ()) -> Path:
    """A results directory of one backlog-owed grade, each ledger row at its figure here, and extra probes."""
    d = base / name
    d.mkdir(parents=True)
    probes = [dict(probe=n, status=(status or {}).get(n, 'measured'), ms=round(ms, 5), budget_ms=20.0,
                   within_budget=False, **({'unanswered': True} if n in never else {})) for n, ms in figures.items()]
    (d / f'{GROUP}.json').write_text(json.dumps(dict(group=GROUP, probes=probes, passes={})))
    if extra:
        (d / 'other.json').write_text(json.dumps(dict(group='other', probes=list(extra), passes={})))
    (d / 'results.json').write_text('{}')
    return d


def log_file(base: Path, name: str, lines: list[str], summary: str | None) -> Path:
    """A run's log: its BUDGET lines and summary."""
    path = base / f'{name}.log'
    path.write_text('\n'.join([*lines, *([summary] if summary else []), 'END rc=0']) + '\n')
    return path


def budget_lines(figures: dict[str, float]) -> list[str]:
    """BUDGET lines as run.py prints them."""
    return [f'BUDGET {n}: {ms:.3f} ms over its budget 20 ms' for n, ms in figures.items()]


def summary(misses: int, refusals: int = 0) -> str:
    """A run's summary line as run.py prints it."""
    return f'22 groups graded, {refusals} refusals, {misses} budget misses (7 of 213 probe instances, 4 of 24 paths)'


def in_process(argv: list[str]) -> tuple[int, str]:
    """main() here, so a mutant patched into this module is the one graded."""
    text = io.StringIO()
    with contextlib.redirect_stdout(text), contextlib.redirect_stderr(text):
        try:
            rc = main(argv)
        except SystemExit as refusal:  # argparse's refusal of its arguments
            rc = refusal.code
    return rc, text.getvalue()


def as_process(argv: list[str]) -> tuple[int, str]:
    """This file run as its own process, its exit status the verdict."""
    r = subprocess.run([sys.executable, '-I', str(Path(__file__).resolve()), *argv], capture_output=True, text=True,
                       check=False)
    return r.returncode, r.stdout + r.stderr


def failing(rc: int, text: str, name: str) -> bool:
    """A nonzero exit whose findings name the row."""
    return rc != 0 and any(line.startswith((f'- {name} ', f'- {name}:')) for line in text.splitlines())


def controls(base: Path, run: Callable[[list[str]], tuple[int, str]]) -> list[tuple[str, bool, str]]:
    """Each control and whether it held: (name, held, detail)."""
    point, ledger = '8x8-1if', LEDGER['8x8-1if']
    doc_figures, measured = doc_ledger(DOC.read_text())
    from decimal import ROUND_CEILING, Decimal
    rule = {row: float(HOLD_MS + ((Decimal(str(ms)) - HOLD_MS) * Decimal('1.05')).quantize(Decimal('0.01'),
                                                                                         ROUND_CEILING))
            for row, ms in MEASURED[point].items()}
    planted_hold = SCENARIO.read_text().replace("f'wait cycles {60 * MS}', 'mark room', 'txready 1'",
                                                "f'wait cycles {59 * MS}', 'mark room', 'txready 1'")
    out = [("the ledger is section 13's table, row for row and figure for figure", doc_figures == ledger,
            str(doc_figures)),
           ("section 13's measurement is the one the ledger derives from", measured == MEASURED[point], str(measured)),
           ("section 13's two measurements are the two images'",
            doc_measurements(DOC.read_text()) == (MERGED, COMPOSED), str(doc_measurements(DOC.read_text()))),
           ('each figure is the hold plus the service behind it plus 5 %, rounded up to 0.01 ms', ledger == rule,
            str(rule)),
           ("the hold is scenario.py's backlog-owed hold, and a planted hold of another length is read as it",
            HOLD_MS == hold_ms() == 60 and hold_ms(planted_hold) == 59, str(HOLD_MS))]
    rc, text = run(['--point', point, str(grade_dir(base, 'at-ledger', ledger))])
    out.append(('the unchanged ledger, every row at its figure, passes', rc == 0 and 'RESULT: PASS' in text,
                f'rc {rc}'))
    rc, text = run(['--point', point, str(grade_dir(base, 'published', measured))])
    out.append(("section 13's measurement passes", rc == 0, f'rc {rc}'))
    for k, name in enumerate(ledger):
        for kind, ms in (('one cycle', ledger[name] + 1 / PER_MS), ('a large increase', ledger[name] + 36.76)):
            rc, text = run(['--point', point, str(grade_dir(base, f'{kind[:5]}-{k}', {**ledger, name: ms}))])
            out.append((f'{name} {kind} over its figure ({ms:.5f} ms) exits nonzero naming it', failing(rc, text, name),
                        f'rc {rc}'))
    other = dict(probe='backlog-adp@blank-6.service.aecp.last.if0', status='measured', ms=20.001, budget_ms=20.0,
                 within_budget=False)
    rc, text = run(['--point', point, str(grade_dir(base, 'new', ledger, (other,)))])
    out.append(('a miss of another row is new and fails, named', failing(rc, text, other['probe']), f'rc {rc}'))
    fits = dict(other, ms=19.999, within_budget=True)
    rc, _ = run(['--point', point, str(grade_dir(base, 'fits', ledger, (fits,)))])
    out.append(('another row within its budget passes', rc == 0, f'rc {rc}'))
    name = 'backlog.owed_behind2.if0'
    rc, text = run(['--point', point, str(grade_dir(base, 'absent', {n: v for n, v in ledger.items() if n != name}))])
    out.append(('a ledger row with no instance fails, named', failing(rc, text, name), f'rc {rc}'))
    rc, text = run(['--point', point, str(grade_dir(base, 'unmeasured', ledger, status={name: 'no end'}))])
    out.append(('a ledger row not measured fails, named', failing(rc, text, name), f'rc {rc}'))
    rc, text = run(['--point', point, str(grade_dir(base, 'never', ledger, never=(name,)))])
    out.append(('a ledger row never answered, within its figure, fails', failing(rc, text, name), f'rc {rc}'))
    rc, text = run(['--point', point, str(grade_dir(base, 'elsewhere', ledger, (dict(other, probe=name, ms=20.5),)))])
    out.append(("a ledger row's name in another group is a new miss", failing(rc, text, name), f'rc {rc}'))
    logged = {n: round(v - 0.001, 3) for n, v in ledger.items()}
    rc, _ = run(['--point', point, str(log_file(base, 'log-under', budget_lines(logged), summary(7)))])
    out.append(("a log's rows a printed microsecond under their figures pass", rc == 0, f'rc {rc}'))
    rc, _ = run(['--point', point, str(log_file(base, 'log-published', budget_lines(measured), summary(7)))])
    out.append(("a log of section 13's measurement passes", rc == 0, f'rc {rc}'))
    rc, text = run(['--point', point, str(log_file(base, 'log-at', budget_lines({**logged, name: ledger[name]}),
                                                   summary(7)))])
    out.append(("a log's row printed at its figure fails: its log does not show it within", failing(rc, text, name),
                f'rc {rc}'))
    for label, lines, s in (('no summary', budget_lines(logged), None),
                            ('a refusal', budget_lines(logged), summary(7, 1)),
                            ('a BUDGET line short of the summary', budget_lines(logged)[1:], summary(7))):
        rc, text = run(['--point', point, str(log_file(base, f'log-{label[:4]}', lines, s))])
        out.append((f'a log with {label} fails', rc == 1 and 'RESULT: FAIL' in text, f'rc {rc}'))
    refused = grade_dir(base, 'refused', ledger)
    (refused / 'results.json').write_text(json.dumps({'refusals': ['backlog-owed: no end: missing']}))
    rc, text = run(['--point', point, str(refused)])
    out.append(("a results directory whose run refused a group fails", rc == 1 and 'the run refused 1' in text,
                f'rc {rc}'))
    bare = grade_dir(base, 'bare', ledger)
    (bare / 'results.json').unlink()
    rc, text = run(['--point', point, str(bare)])
    out.append(('a results directory with no results.json fails', rc == 1 and 'no results.json' in text, f'rc {rc}'))
    rc, _ = run(['--point', '1x1', str(base / 'at-ledger')])
    out.append(('a point with no ledger is refused', rc == 2, f'rc {rc}'))
    return out


#: Each mutant of a rule, which some control must refuse.
MUTANTS = {
    'a ledger row waived by its name whatever its size': lambda m: patch.object(
        m, 'over', lambda p, figure: False),
    "a grade's figure read at its log's microsecond": lambda m: patch.object(
        m, 'most', lambda p: round(p['ms'], 3) * PER_MS + (0 if p['exact'] else LOG_HALF)),
    'a ledger row at its figure failing': lambda m: patch.object(
        m, 'over', lambda p, figure: m.most(p) >= m.units(figure)),
    'a new miss waived': lambda m: patch.object(m, 'new_miss', lambda p: False),
    'a ledger row with no instance passing': lambda m: patch.object(m, 'unseen', lambda ledger, seen, logs: []),
    "a log's figure read as exact": lambda m: patch.object(m, 'LOG_HALF', 0),
    "a ledger figure a hundredth over section 13's": lambda m: patch.dict(
        m.LEDGER['8x8-1if'], {'backlog.owed.if0': m.LEDGER['8x8-1if']['backlog.owed.if0'] + 0.01}),
    'a ledger figure with no 5 % on its service': lambda m: patch.dict(m.LEDGER['8x8-1if'], {
        row: m.HOLD_MS + -(-(round(ms * m.PER_MS) - m.HOLD_MS * m.PER_MS) // 1000) / 100
        for row, ms in m.MEASURED['8x8-1if'].items()}),
    'the 5 % on the whole row, the hold too': lambda m: patch.dict(m.LEDGER['8x8-1if'], {
        row: -(-round(ms * m.PER_MS) * 105 // 100 // 1000) / 100 for row, ms in m.MEASURED['8x8-1if'].items()}),
    "the hold not the scenario's": lambda m: patch.object(m, 'HOLD_MS', 59),
    'a measurement the ledger does not derive from': lambda m: patch.dict(
        m.MEASURED['8x8-1if'], {'backlog.owed_behind1.if0': 63.526}),
    "a figure at the merged image's measurement where the composed one is larger": lambda m: patch.dict(
        m.MEASURED['8x8-1if'], dict(m.MERGED)),
    "a run's refusals not read": lambda m: patch.object(m, 'run_refusals', lambda path: []),
    "a ledger row's name taken in any group": lambda m: patch.object(
        m, 'is_row', lambda p, ledger: p['probe'] in ledger),
}


def selftest() -> int:
    """Every control in this process and, for the exit status, as its own process; then each mutant refused."""
    me = sys.modules[__name__]
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        for mode, run in (('in process', in_process), ('as a process', as_process)):
            for name, held, detail in controls(Path(tmp) / mode.replace(' ', '-'), run):
                print(f"{'PASS' if held else 'FAIL'} [{mode}] {name}: {detail}")
                bad += not held
        for k, (name, plant) in enumerate(MUTANTS.items()):
            with plant(me):
                refused = [n for n, held, _ in controls(Path(tmp) / f'mutant-{k}', in_process) if not held]
            print(f"{'caught' if refused else 'ESCAPED'} mutant {name!r}" + (f': {refused[0]}' if refused else ''))
            bad += not refused
    print(f'RESULT: {"PASS" if not bad else "FAIL"}: {len(MUTANTS)} mutants, {bad} failure(s)')
    return 1 if bad else 0


if __name__ == '__main__':
    raise SystemExit(main())
