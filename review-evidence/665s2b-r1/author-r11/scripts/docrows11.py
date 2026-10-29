#!/usr/bin/env python3
"""Scratch: the round-11 legs as SPLIT_CONTROL_MEMORY section 13's tables, one per CPU clock, and the per-pass share's
table, from rows11.py's reading of each leg.

usage: docrows11.py RESULTS_ROOT
Cells are arm A / arm B in ms, bold over the row's own bound."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rows11  # noqa: E402

ROWS = (('ACMP record, last', 'ACMP record, last'), ('ADP record, last', 'ADP record, last'),
        ('MAAP record, last', 'MAAP record, last'), ('AECP record, last', 'AECP record, last'),
        ('SRP record, last', 'SRP record, last'),
        ('an ACMP command behind a full acmp ring', 'An ACMP command behind a full ACMP ring'),
        ('an ENTITY_AVAILABLE behind a full adp ring', 'An ENTITY_AVAILABLE behind a full ADP ring'),
        ('an event behind 15 others', 'An event behind 15 others'),
        ('AECP record, last, in the owed window', 'AECP record, last, in the owed window'),
        ('a response with 7 frames owed ahead of it', 'A response with 7 frames owed ahead of it'),
        ('an ACMP command behind the owed input', 'An ACMP command behind the owed input'))
COLS = (('N', '1x1', '1x1/1if'), ('D', '1x1', '1x1/1if, with both drafts'), ('N', '8x8', '8x8/2if'),
        ('D', '8x8', '8x8/2if, with both drafts'))


def main() -> int:
    root = Path(sys.argv[1])
    legs = {}
    for leg in sorted(root.iterdir()):
        if (leg / 'build.json').is_file():
            tag, mid, clk = leg.name.split('-')
            legs[(tag[0], mid[0], {'1': '1x1', '8': '8x8'}[mid[1]], clk)] = rows11.load(leg)
    for clk, label in (('50', "the product's split CPU clock, 50 MHz"), ('100', 'the labelled 100 MHz option')):
        w = {(d, arm, pt): rows11.worst(legs[(d, arm, pt, clk)][0]) for d, pt, _ in COLS for arm in 'AB'}
        print(f'CPU at {label}, bus 100 MHz:\n')
        print('| Row | Bound, ms | ' + ' | '.join(c for _, _, c in COLS) + ' |')
        print('|---|---:|' + '---:|' * len(COLS))
        for key, name in ROWS:
            bound = next(e[2] for e in (w[k].get(key) for k in w) if e)
            cells = [f"{rows11.cell(w[(d, 'A', pt)].get(key))} / {rows11.cell(w[(d, 'B', pt)].get(key))}"
                     for d, pt, _ in COLS]
            print(f'| {name} | {bound:g} | ' + ' | '.join(cells) + ' |')
        print()
    print('Per-pass share, 2.0 ms of CPU time; each cell is arm A / arm B: the work passes over it of the four groups\''
          ' runs, and the longest pass in ms:\n')
    print('| CPU clock | ' + ' | '.join(c for _, _, c in COLS) + ' |')
    print('|---|' + '---:|' * len(COLS))
    for clk, label in (('50', '50 MHz (product)'), ('100', '100 MHz (option)')):
        cells = []
        for d, pt, _ in COLS:
            parts = []
            for arm in 'AB':
                results = legs[(d, arm, pt, clk)][0]['results']
                over = sum(g['passes']['share']['over'] for g in results)
                total = sum(g['passes']['share']['passes'] for g in results)
                top = max(g['passes']['worst']['ms'] for g in results)
                text = f'{over} of {total}, {top:.2f}'
                parts.append(f'**{text}**' if over else text)
            cells.append(' / '.join(parts))
        print(f'| {label} | ' + ' | '.join(cells) + ' |')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
