#!/usr/bin/env python3
"""Scratch: every composed row's worst instance over the four backlog groups, graded against its own bound.

usage: rows9.py POINT LABEL=A_RESULTS,B_RESULTS ...   (each a results.json or results.json.gz)
A row's bound is min(T_svc, its family's ceiling) plus its normative wait (FR_NFR.md 3.4.1, approved 2026-10-29),
taken from the lane's scenario.py, so a run graded at the 10 ms proposal is graded again here at the approved one.
Cells are arm A / arm B in ms, bold over the bound; "never" is a command never answered or a record never released.
The owed window holds the egress for 60 ms, so its last AECP record, whose response waits for it, is its own row."""
import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, '$LANES/665-s2b-cycles/tb/verilator/ctrl_service_budget')
import scenario  # noqa: E402

GROUPS = ('backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed')
NAMES = {
    'ACMP record released under the composed load, last': 'ACMP record, last',
    'ADP record released under the composed load, last': 'ADP record, last',
    'MAAP record released under the composed load, last': 'MAAP record, last',
    'AECP record released under the composed load, last': 'AECP record, last',
    'SRP record released under the composed load, last': 'SRP record, last',
    'ACMP record released under the composed load, first': 'ACMP record, first',
    'ADP record released under the composed load, first': 'ADP record, first',
    'MAAP record released under the composed load, first': 'MAAP record, first',
    'AECP record released under the composed load, first': 'AECP record, first',
    'SRP record released under the composed load, first': 'SRP record, first',
}


def load(path: str) -> dict:
    raw = Path(path).read_bytes()
    return json.loads(gzip.decompress(raw) if path.endswith('.gz') else raw)


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
                row += ', in the owed window'     # its responses wait for the held egress
            key = (never, r['ms'])
            if row not in out or key > out[row][0]:
                out[row] = (key, not never and r['ms'] <= bound(r), bound(r), r['family'], g['group'])
    return out


def cell(entry) -> str:
    if entry is None:
        return '-'
    (never, ms), fits, _, _, _ = entry
    text = 'never' if never else f'{ms:.2f}'
    return text if fits else f'**{text}**'


def main() -> int:
    point, specs = sys.argv[1], sys.argv[2:]
    runs = []
    for spec in specs:
        label, _, paths = spec.partition('=')
        a, b = paths.split(',')
        runs.append((label, worst(load(a)), worst(load(b))))
    rows = sorted(set().union(*(set(wa) | set(wb) for _, wa, wb in runs)))
    print(f'| {point}: row | Bound, ms | ' + ' | '.join(label for label, _, _ in runs) + ' |')
    print('|---|---:|' + '---:|' * len(runs))
    for row in rows:
        entry = next(e for _, wa, wb in runs for e in (wa.get(row), wb.get(row)) if e)
        cells = [f'{cell(wa.get(row))} / {cell(wb.get(row))}' for _, wa, wb in runs]
        print(f'| {row} | {entry[2]:g} | ' + ' | '.join(cells) + ' |')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
