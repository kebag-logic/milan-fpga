#!/usr/bin/env python3
"""Render the README's results tables from the recorded runs' results.json files.

usage: results_tables.py RUN_DIR...   (each RUN_DIR holds results/results.json)
Each run is labelled by its point, clock and arm, read from its results.json.
"""
import json
import sys
from pathlib import Path

HOOKS = ('H-ADP', 'H-DISC', 'H-ACMP', 'H-AECP', 'H-NOTIFY', 'H-COUNTERS', 'H-MAAP', 'H-SRP')


def load(d: Path) -> dict:
    r = json.loads((d / 'results' / 'results.json').read_text())
    clock = '50' if r['cpu_hz'] == 50_000_000 else '100 (variant)'
    r['label'] = (r['point'], clock, r['arm'])
    return r


def cell(w: dict | None) -> str:
    if not w:
        return '-'
    ms = 'never served' if w['unbounded'] else f"{w['ms']:.2f}"
    bold = '' if w['within'] else '**'
    return f"{bold}{ms}{bold} ({w['bound_ms']:g})"


def where(w: dict | None) -> str:
    return f"`{w['probe']}`" if w else '-'


def main() -> int:
    runs = [load(Path(a)) for a in sys.argv[1:]]
    runs.sort(key=lambda r: (r['point'], r['arm'] != 'idle', r['cpu_hz']))
    for point in ('1x1', '8x8'):
        mine = [r for r in runs if r['point'] == point]
        if not mine:
            continue
        head = ' | '.join(f"CPU {c} MHz, {a}" for _, c, a in (r['label'] for r in mine))
        for part, title in (('alone', 'alone'), ('loaded', 'under the composed load')):
            print(f'\n{point}, each hook\'s worst path {title}, ms (bound); bold is over its bound:\n')
            print(f'| Hook | {head} |')
            print('|---|' + '---:|' * len(mine))
            for h in HOOKS:
                print(f'| {h} | ' + ' | '.join(cell(r['summary'][h]['worst'].get(part)) for r in mine) + ' |')
        print(f'\n{point}, paths over their bound (of paths), and the ordering check (instances applied, findings):\n')
        print(f'| Hook | {head} |')
        print('|---|' + '---:|' * len(mine))
        for h in HOOKS:
            row = []
            for r in mine:
                s = r['summary'][h]
                row.append(f"{s['misses']} of {s['paths']}; {s['applied']}, {len(s['ordering_findings'])}")
            print(f'| {h} | ' + ' | '.join(row) + ' |')
        print(f'\n{point}, where each worst path is (alone / under load):\n')
        for r in mine:
            print(f"- CPU {r['label'][1]} MHz, {r['label'][2]}: " + '; '.join(
                f"{h} {where(r['summary'][h]['worst'].get('alone'))} / {where(r['summary'][h]['worst'].get('loaded'))}"
                for h in HOOKS))
        print()
        for r in mine:
            print(f"- CPU {r['label'][1]} MHz, {r['label'][2]}: {len(r['rows'])} paths, {len(r['refusals'])} refusals, "
                  f"{len(r['superseded'])} superseded, build {r['build'][:12]}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
