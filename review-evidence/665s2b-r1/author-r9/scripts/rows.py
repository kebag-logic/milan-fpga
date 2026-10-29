#!/usr/bin/env python3
"""Scratch: each composed row's worst instance over the four backlog groups, per run, against T_svc.

usage: rows.py LABEL=RESULTS ... (RESULTS a results.json or results.json.gz)
Prints one Markdown row per composed row, one column per run: the worst instance's ms (a command never answered
is the run's bound with "never"), bold where it misses T_svc, then the group that set the worst of the last run.
The owed window holds the egress for 60 ms, so its last AECP record, whose response waits for it, is its own row."""
import gzip
import json
import sys
from pathlib import Path

GROUPS = ('backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed')


def load(path: str) -> dict:
    raw = Path(path).read_bytes()
    return json.loads(gzip.decompress(raw) if path.endswith('.gz') else raw)


def worst(results: dict) -> dict:
    out = {}
    for g in results['results']:
        if g['group'] not in GROUPS:
            continue
        for r in g['probes']:
            if r['status'] != 'measured':
                continue
            key = (bool(r.get('unanswered') or r.get('starved')), r['ms'])
            row = r['row']
            if g['group'] == 'backlog-owed' and row.startswith('AECP record'):
                row += ', in the owed window (egress held)'     # its responses wait for the held egress
            if row not in out or key > out[row][0]:
                out[row] = (key, r['within_t_svc'], g['group'])
    return out


def main() -> int:
    runs = [(spec.partition('=')[0], worst(load(spec.partition('=')[2]))) for spec in sys.argv[1:]]
    print('| Row | ' + ' | '.join(label for label, _ in runs) + ' | Worst group, last run |')
    print('|---|' + '---:|' * len(runs) + '---|')
    for row in sorted(set().union(*(w for _, w in runs))):
        cells = []
        for _, w in runs:
            if row not in w:
                cells.append('-')
                continue
            (never, ms), fits, _ = w[row]
            text = f'never answered (at least {ms:.0f})' if never else f'{ms:.2f}'
            cells.append(text if fits else f'**{text}**')
        print(f'| {row} | ' + ' | '.join(cells) + f' | {runs[-1][1].get(row, (0, 0, "-"))[2]} |')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
