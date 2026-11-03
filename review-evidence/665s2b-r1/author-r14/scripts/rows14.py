#!/usr/bin/env python3
"""This round's rows and passes from the legs' results: every composed row's worst instance over the four backlog
windows and, apart, over a save's windows and over the two held saves (save_window.py); each set's passes against the
per-pass share; every timed save against its stated worst case; and the passes that carry the store's step.

usage: rows14.py CHECKOUT BUILDS OUT.md LABEL=LEG_A[,LEG_B] ...
Each LEG is BUILDS/LEG with results/results.json and build.json. A row's bound is min(T_svc, its family's ceiling)
plus its normative wait (FR_NFR.md 3.4.1). Every table names the CPU clock, and a leg not on sys at 100 MHz is
refused. Cells are arm A / arm B in ms, bold over the bound; "never" is a command never answered. The owed window
holds the egress for 60 ms, so its last AECP record is its own row. A share cell is passes over it (those with no
mailbox write counted by their run's longest) of the work passes, then the longest pass in ms.
"""
import json
import sys
from pathlib import Path

checkout, builds, out, *cols = sys.argv[1:]
sys.path.insert(0, str(Path(checkout) / 'tb/verilator/ctrl_service_budget'))
sys.path.insert(0, str(Path(checkout) / 'sw/mailbox'))
import scenario  # noqa: E402
import share  # noqa: E402

BACKLOG = ('backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed')
NAMES = {f'{f} record released under the composed load, {w}': f'{f} record, {w}'
         for f in ('ACMP', 'ADP', 'MAAP', 'AECP', 'SRP') for w in ('first', 'last')}
ORDER = ('ACMP record, first', 'ADP record, first', 'MAAP record, first', 'AECP record, first', 'SRP record, first',
         'ACMP record, last', 'ADP record, last', 'MAAP record, last', 'AECP record, last', 'SRP record, last',
         'an ACMP command behind a full acmp ring', 'an ENTITY_AVAILABLE behind a full adp ring',
         'an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed)', 'an event behind 15 others',
         'AECP record, last, in the owed window', 'a response with 7 frames owed ahead of it',
         'an ACMP command behind the owed input',
         *(f'{f} record, every channel at its refill rate, the longest' for f in ('ADP', 'ACMP', 'AECP', 'MAAP', 'SRP')))
SETS = {'backlog': lambda g: g in BACKLOG, 'save': lambda g: '@' in g, 'held': lambda g: g == 'save-held',
        'starved': lambda g: g == 'save-starved', 'all': lambda g: True}


def load(leg: Path) -> dict:
    spec = json.loads((leg / 'build.json').read_text())
    if spec['cpu_cd'] != 'sys' or spec['cpu_hz'] != 100_000_000 or spec['sys_hz'] != 100_000_000:
        raise SystemExit(f'{leg}: build.json records CPU {spec.get("cpu_hz")} on {spec.get("cpu_cd")}')
    return json.loads((leg / 'results/results.json').read_text())


def bound(r: dict) -> float:
    return min(scenario.T_SVC_MS, scenario.CEILING_MS[r['family']]) + r.get('wait_ms', 0.0)


def worst(res: dict, which: str) -> dict:
    out = {}
    for g in res['results']:
        if not SETS[which](g['group']):
            continue
        for r in g['probes']:
            if r['status'] != 'measured':
                continue
            never = bool(r.get('unanswered') or r.get('starved'))
            row = NAMES.get(r['row'], r['row'])
            if g['group'] == 'backlog-owed' and row.startswith('AECP record'):
                row += ', in the owed window'
            key = (never, r['ms'])
            if row not in out or key > out[row][0]:
                out[row] = (key, not never and r['ms'] <= bound(r), bound(r), g['group'], r['probe'])
    return out


def cell(entry) -> str:
    if entry is None:
        return '-'
    (never, ms), fits, *_ = entry
    text = 'never' if never else f'{ms:.2f}'
    return text if fits else f'**{text}**'


def shares(res: dict, which: str) -> tuple[int, int, float, int]:
    """Passes over the share (idle runs included), work passes, the longest pass in ms, groups."""
    over = passes = groups = 0
    longest = 0.0
    for g in res['results']:
        if not SETS[which](g['group']):
            continue
        s, top = g['passes']['share'], g['passes']['worst']
        over += s['over']
        passes += s['passes']
        groups += 1
        longest = max(longest, top['ms'] if top else 0.0, s.get('idle_longest', 0) / 1e5)
    return over, passes, longest, groups


def share_cell(res: dict, which: str) -> str:
    over, passes, longest, _ = shares(res, which)
    text = f'{over} of {passes}, {longest:.2f}'
    return f'**{text}**' if over else text


def table(columns: list, which: str, title: str) -> list[str]:
    rows = {}
    for _, legs in columns:
        for res in legs:
            rows.update(worst(res, which))
    lines = [title, '', '| Row | Bound, ms | ' + ' | '.join(c[0] for c in columns) + ' |',
             '|---|---:|' + '---:|' * len(columns)]
    for row in ORDER:
        if row in rows:
            cells = [' / '.join(cell(worst(res, which).get(row)) for res in legs) for _, legs in columns]
            lines.append(f'| {row} | {rows[row][2]:g} | ' + ' | '.join(cells) + ' |')
    return lines + ['']


def main() -> None:
    columns = [(label, [load(Path(builds) / leg) for leg in legs.split(',')])
               for label, legs in (c.split('=') for c in cols)]
    write(columns)


def write(columns: list) -> None:
    lines = ['CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over '
             'the bound.', '']
    lines += table(columns, 'backlog', 'The four backlog windows:')
    lines += table(columns, 'save', "A save's windows (save_window.py), 24 at each leg:")
    lines += table(columns, 'held', 'save-held, every receive channel at its refill rate with its bursts:')
    lines += table(columns, 'starved', 'save-starved, the same and a grandmaster change as every pass starts:')
    lines += [f'The share is {share.share_ms():.1f} ms. Passes over it, of the work passes run, and the longest in ms, arm A / '
              'arm B:', '', '| Groups | ' + ' | '.join(c[0] for c in columns) + ' |', '|---|' + '---:|' * len(columns)]
    for which, label in (('backlog', 'The four backlog windows'), ('save', "A save's windows"), ('held', 'save-held'),
                         ('starved', 'save-starved'), ('all', 'Every group run')):
        lines.append(f'| {label} | ' + ' | '.join(' / '.join(share_cell(res, which) for res in legs) for _, legs in columns)
                     + ' |')
    lines.append('')
    lines += ['Saves, ms from the change to durable against the stated worst case, arm A / arm B (steps; longest gap '
              'between flash steps, ms):', '', '| Group | ' + ' | '.join(c[0] for c in columns) + ' |',
              '|---|' + '---:|' * len(columns)]
    for group in ('save', 'save-held', 'save-starved'):
        cells = []
        for _, legs in columns:
            parts = []
            for res in legs:
                s = next((x for x in res.get('saves', []) if x['group'] == group), None)
                parts.append('-' if s is None else (f"{s['ms']:.1f}" if s['ms'] is not None else 'never')
                             + f" of {s['bound_ms']:,} ({s['steps']}; {s['longest_gap_ms']})"
                             + ('' if s['within'] else ' **OVER**'))
            cells.append(' / '.join(parts))
        lines.append(f'| {group} | ' + ' | '.join(cells) + ' |')
    lines += ['', "Passes that carry the store's step, every group: count, the longest pass and the longest step, CPU cycles "
              '(ms), arm A / arm B:', '', '| ' + ' | '.join(c[0] for c in columns) + ' |', '|' + '---:|' * len(columns)]
    cells = []
    for _, legs in columns:
        parts = []
        for res in legs:
            st = [g['passes'].get('steps', {}) for g in res['results'] if g['passes'].get('steps', {}).get('passes')]
            if not st:
                parts.append('-')
                continue
            top, own = max(st, key=lambda x: x['cycles']), max(st, key=lambda x: x['store_cycles'])
            parts.append(f"{sum(x['passes'] for x in st)}: {top['cycles']:,} ({top['ms']:.3f}); {own['store_cycles']:,} "
                         f"({own['store_ms']:.3f})")
        cells.append(' / '.join(parts))
    lines += ['| ' + ' | '.join(cells) + ' |', '']
    Path(out).write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
