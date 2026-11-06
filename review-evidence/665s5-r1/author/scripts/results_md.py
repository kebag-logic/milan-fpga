#!/usr/bin/env python3
"""Render the README's Results tables from the four product-clock runs' results.json files.

usage: results_md.py SCRATCH   (reads SCRATCH/hr-<point>-<arm>/results/results.json)
Prints, per point: each hook's worst path alone and under the composed load on both arms (ms, bold over its
bound), then the paths, misses, narrow fits and ordering instances; then where each worst path is.
"""
import json
import sys
from pathlib import Path

HOOKS = ('H-ADP', 'H-DISC', 'H-ACMP', 'H-AECP', 'H-NOTIFY', 'H-COUNTERS', 'H-MAAP', 'H-SRP')
ARMS = (('idle', 'idle'), ('ans', 'answering'))


def cell(w: dict | None) -> str:
    """ms, bold when over its bound; '-' when the hook has no path there."""
    if not w:
        return '-'
    ms = 'never served' if w['unbounded'] else f"{w['ms']:.2f}"
    return ms if w['within'] else f'**{ms}**'


def margin(w: dict | None) -> str:
    """The margin to the family's normative timeout."""
    return '-' if not w or w['unbounded'] else f"{w['margin_ms']:.0f} of {w['normative_ms']:g}"


def main() -> int:
    base = Path(sys.argv[1])
    for point in ('1x1', '8x8'):
        runs = {a: json.loads((base / f'hr-{point}-{a}/results/results.json').read_text()) for a, _ in ARMS}
        clocks = {r['clock'] for r in runs.values()}
        print(f'\n{point}, {" / ".join(sorted(clocks))}; ms, bold is over its bound:\n')
        print('| Hook | Bound | Alone, idle | Alone, answering | Under load, idle | Under load, answering |')
        print('|---|---:|---:|---:|---:|---:|')
        for h in HOOKS:
            bound = 18 if h == 'H-SRP' else 20
            cells = [cell(runs[a]['summary'][h]['worst'].get(part)) for part in ('alone', 'loaded') for a, _ in ARMS]
            print(f'| {h} | {bound} | ' + ' | '.join(cells) + ' |')
        print(f'\n{point}: paths over their bound / within it by less than the layout swing / of paths; the ordering '
              'check\'s instances applied (undecided) and its findings:\n')
        print('| Hook | Idle: over / narrow / paths | Idle: ordering | Answering: over / narrow / paths '
              '| Answering: ordering |')
        print('|---|---:|---:|---:|---:|')
        for h in HOOKS:
            row = []
            for a, _ in ARMS:
                s = runs[a]['summary'][h]
                row += [f"{s['misses']} / {s['narrow']} / {s['paths']}",
                        f"{s['applied']} ({s['undecided']}), {len(s['ordering_findings'])}"]
            print(f'| {h} | ' + ' | '.join(row) + ' |')
        print(f'\n{point}, each worst path and its margin to the normative timeout, ms:\n')
        print('| Hook | Arm | Alone | Margin | Under load | Margin |')
        print('|---|---|---|---:|---|---:|')
        for h in HOOKS:
            for a, arm in ARMS:
                w = runs[a]['summary'][h]['worst']
                al, ld = w.get('alone'), w.get('loaded')
                if not al and not ld:
                    continue
                print(f"| {h} | {arm} | {f'`{al['probe']}`' if al else '-'} | {margin(al)} | "
                      f"{f'`{ld['probe']}`' if ld else '-'} | {margin(ld)} |")
        for a, arm in ARMS:
            r = runs[a]
            print(f"\n- {arm}: {len(r['rows'])} paths, {len(r['refusals'])} refusals, {len(r['superseded'])} "
                  f"superseded, {sum(x.startswith('ORDER') for x in r['findings'])} ordering findings, "
                  f"{sum(x.startswith('NARROW') for x in r['findings'])} narrow, "
                  f"{sum(x.startswith('LATE') for x in r['findings'])} late; executable {r['build'][:12]}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
