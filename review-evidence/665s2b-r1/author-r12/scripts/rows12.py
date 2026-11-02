#!/usr/bin/env python3
"""Every composed row's worst instance over the four backlog groups, and every group's passes against the per-pass
share, for this round's legs, the CPU on sys at 100 MHz.

usage: rows12.py BUILDS_OR_RECEIPTS OUT.md LABEL=LEG_A[,LEG_B] ...
Each LEG is a directory holding results/results.json with build.json, or results.json(.gz) with build.json.
A row's bound is min(T_svc, its family's ceiling) plus its normative wait (FR_NFR.md 3.4.1). Every table names the
CPU clock from the legs' build.json and refuses a leg not on sys at 100 MHz. Cells are arm A / arm B in ms, bold over
the bound; "never" is a command never answered. The owed window holds the egress for 60 ms, so its last AECP record,
whose response waits for it, is its own row."""
import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, '$LANES/665-s2b-cycles/tb/verilator/ctrl_service_budget')
import scenario  # noqa: E402
import share  # noqa: E402

GROUPS = ('backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed')
NAMES = {f'{f} record released under the composed load, {w}': f'{f} record, {w}'
         for f in ('ACMP', 'ADP', 'MAAP', 'AECP', 'SRP') for w in ('first', 'last')}
ORDER = ('ACMP record, first', 'ADP record, first', 'MAAP record, first', 'AECP record, first', 'SRP record, first',
         'ACMP record, last', 'ADP record, last', 'MAAP record, last', 'AECP record, last', 'SRP record, last',
         'an ACMP command behind a full acmp ring', 'an ENTITY_AVAILABLE behind a full adp ring',
         'an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed)', 'an event behind 15 others',
         'AECP record, last, in the owed window', 'a response with 7 frames owed ahead of it',
         'an ACMP command behind the owed input')
EGRESS_HELD = ORDER[-3:]


def load(leg: Path, refuse_clock: bool = True) -> tuple[dict, dict]:
    res = next((p for p in (leg / 'results/results.json', leg / 'results.json') if p.is_file()), None)
    raw = res.read_bytes() if res else gzip.decompress((leg / 'results.json.gz').read_bytes())
    spec = json.loads((leg / 'build.json').read_text())
    if refuse_clock and (spec['cpu_cd'] != 'sys' or spec['cpu_hz'] != 100_000_000 or spec['sys_hz'] != 100_000_000):
        raise SystemExit(f'{leg}: build.json records CPU {spec.get("cpu_hz")} on {spec.get("cpu_cd")}')
    return json.loads(raw), spec


def bound(r: dict) -> float:
    return min(scenario.T_SVC_MS, scenario.CEILING_MS[r['family']]) + r.get('wait_ms', 0.0)


def worst(results: dict) -> dict:
    out = {}
    for g in results['results']:
        if g['group'] not in GROUPS:
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
                out[row] = (key, not never and r['ms'] <= bound(r), bound(r), r['family'], g['group'], r['probe'])
    return out


def cell(entry) -> str:
    if entry is None:
        return '-'
    (never, ms), fits, *_ = entry
    text = 'never' if never else f'{ms:.2f}'
    return text if fits else f'**{text}**'


def shares(results: dict) -> tuple[int, int, float]:
    """Passes over the share, work passes run, the longest in ms, over the four groups."""
    over = passes = 0
    longest = 0.0
    for g in results['results']:
        if g['group'] not in GROUPS:
            continue
        s, top = g['passes']['share'], g['passes']['worst']
        over += s['over']
        passes += s['passes']
        longest = max(longest, top['ms'])
    return over, passes, longest


def share_cell(res: dict) -> str:
    over, passes, longest = shares(res)
    text = f'{over} of {passes}, {longest:.2f}'
    return f'**{text}**' if over else text


def main() -> int:
    root, out, *cols = sys.argv[1:]
    root = Path(root)
    lines = []
    columns = []
    for col in cols:
        label, legs = col.split('=')
        columns.append((label, [load(root / leg) for leg in legs.split(',')]))
    lines.append('CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.')
    lines.append('')
    lines.append('| Row | Bound, ms | ' + ' | '.join(c[0] for c in columns) + ' |')
    lines.append('|---|---:|' + '---:|' * len(columns))
    all_rows = {}
    for _, legs in columns:
        for res, _spec in legs:
            all_rows.update(worst(res))
    for row in ORDER:
        if row not in all_rows:
            continue
        cells = []
        for _, legs in columns:
            cells.append(' / '.join(cell(worst(res).get(row)) for res, _ in legs))
        lines.append(f'| {row} | {all_rows[row][2]:g} | ' + ' | '.join(cells) + ' |')
    lines.append('')
    lines.append(f'The share is {share.share_ms():.1f} ms. Passes over it of the work passes run, longest in ms, arm A / arm B:')
    lines.append('')
    lines.append('| ' + ' | '.join(c[0] for c in columns) + ' |')
    lines.append('|' + '---:|' * len(columns))
    lines.append('| ' + ' | '.join(' / '.join(share_cell(res) for res, _ in legs) for _, legs in columns) + ' |')
    lines.append('')
    Path(out).write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
