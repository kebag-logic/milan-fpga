# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The tier designs' search grid (#894's ruling of 2026-11-13, item 3): every candidate's rows by every source at a
point (rows_tiers.py, its tier model and each row's bound, bounds_at), its long-window load (load_grade.py) and whether
it holds every row within its bound and the load within 0.70. No bound moves; the grid is declared before it runs.

The grid, at the point's stated costs and tier 2 SRP first (the built order):
  aecp-first, others-first  the others' cap a pass 1, 2 or 4
  aecp-quota                each other tier-1 channel's quota 1, 2 or 3, AECP the time they leave
  wrr                       weights (AECP, ACMP, ADP, MAAP) 1/1/1/1, 2/1/1/1, 1/2/1/1 or 2/2/1/1
  turn                      the tree's cap (rows_tiers.REFERENCE's order), reported and not searched
each at every slice from one SRP record's apply to CTRL_LOOP_DRAIN_US on the 50 us grid, and under each rule for a
notice longer than a slot (rows_tiers.LONG_RULES). A candidate holds when every row is within its bound and the load
at or under LOAD_CEILING; of those, the one with the largest least relative margin over every row is chosen, a tie to
the built order, then the larger slice.

usage: python3 -I tier_grid.py [--point POINT] [--out DIR]
  --point  the point the grid is solved at (default 1x1/1if, the one the ruling gates)
  --out    write each order's table, the chosen or best candidates' terms and the summary there
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import load_grade  # noqa: E402
import rows_tiers  # noqa: E402

ROOT = rows_tiers.ROOT
#: The long-window load ceiling the ruling holds a design to at 1x1/1if (#665: the 0.70 long-window ceiling).
LOAD_CEILING = 0.70
#: The searched orders and each one's caps or quotas, and the order reported beside them.
CAPS = {'aecp-first': (1, 2, 4), 'others-first': (1, 2, 4)}
QUOTAS = {'aecp-quota': ((0, 1, 1, 1), (0, 2, 2, 2), (0, 3, 3, 3)),
          'wrr': ((1, 1, 1, 1), (2, 1, 1, 1), (1, 2, 1, 1), (2, 2, 1, 1))}
REPORTED = ('turn',)
#: The rows every candidate is held to, in the tables' order.
ROWS = (*rows_tiers.TIER_ROWS, *rows_tiers.ADDED_ROWS)


class Result(NamedTuple):
    """A candidate's rows, its least relative margin over every row, its loads and R4L's break-even notice cost."""

    design: rows_tiers.Design
    rows: dict
    margin: float
    holds: bool
    load: float
    long_load: float
    even_us: int | None


def candidates(i: rows_tiers.Inputs, orders: tuple[str, ...]) -> list[rows_tiers.Design]:
    """The grid's designs of those orders at the point's inputs, in the tables' order."""
    first = math.ceil(rows_tiers.smallest_slice(i) / rows_tiers.SLICE_GRID_US) * rows_tiers.SLICE_GRID_US
    grid = range(first, i.h['CTRL_LOOP_DRAIN_US'] + 1, rows_tiers.SLICE_GRID_US)
    out = []
    for order in orders:
        shapes = [{'cap': n} for n in CAPS.get(order, ())] + [{'quota': q} for q in QUOTAS.get(order, ())] or [{}]
        for shape in shapes:
            for long in rows_tiers.LONG_RULES:
                out += [rows_tiers.Design(us, order, 'srp-first', 'queue', long=long, **shape) for us in grid]
    return out


def even(i: rows_tiers.Inputs, d: rows_tiers.Design, bound: float) -> int | None:
    """The largest cost in us, on a 5 us grid, of the largest legal notice at which R4L fits its bound; None if none."""
    def fits(us: int) -> bool:
        """Whether R4L fits with that notice cost."""
        w = rows_tiers.solve('R4L', i._replace(c={**i.c, 'item.aecp.long': us}), d)[0]
        return w is not None and w <= bound
    if not fits(0):
        return None
    low, high = 0, 5000
    while high - low > 5:
        mid = (low + high) // 10 * 5
        low, high = (mid, high) if fits(mid) else (low, mid)
    return low


def solve(root: Path, point: str, d: rows_tiers.Design, i: rows_tiers.Inputs, loads: tuple[float, float]) -> Result:
    """A candidate's rows, margin, loads and break-even."""
    bounds = rows_tiers.bounds_at(i)
    held = rows_tiers.rows(root, point, d, i)
    margin = rows_tiers.least_margin(held, bounds)
    # by every source a command's notice may be the largest legal one under either rule: both loads are held
    holds = all(w is not None and w <= bounds[r] for r, (w, _) in held.items()) and max(loads) <= LOAD_CEILING
    return Result(d, held, margin, holds, *loads, even(i, d, bounds['R4L']))


def loads(root: Path, point: str) -> tuple[float, float]:
    """The point's long-window load at the pin, with the stated notice and with every command's notice the largest
    legal one (load_grade charges a record's owed frame at the larger of its response's and its notice's)."""
    table = {p: dict(v) for p, v in load_grade.STATED_US.items()}
    stated = sum(load_grade.load(root, point, table).values())
    table[point]['item.aecp.notice'] = rows_tiers.LONG_NOTICE_US[point]
    return stated, sum(load_grade.load(root, point, table).values())


def shape(d: rows_tiers.Design) -> str:
    """A candidate's cap or quotas as a table names them."""
    return f'quotas {"/".join(map(str, d.quota))}' if d.quota else f'cap {d.cap or "tree"}'


def table(results: list[Result], bounds: dict) -> list[str]:
    """Each candidate's row: its shape, slice, long-notice rule, every row's W and residual, its least margin, whether
    it holds, its loads and R4L's break-even notice cost."""
    lines = ['| Order | Cap or quotas | Slice, us | Long notices | ' + ' | '.join(f'{r} ({bounds[r]})' for r in ROWS) +
             ' | Least margin | Holds | Load | Load, long notices | R4L break-even, us |',
             '|---|---|---:|---|' + '---:|' * len(ROWS) + '---:|---|---:|---:|---:|']
    for r in results:
        cells = [('none' if w is None else f'{w:.2f} ({w - bounds[row]:+.2f})') for row, (w, _) in
                 ((row, r.rows[row]) for row in ROWS)]
        lines.append(f'| {r.design.tier1} | {shape(r.design)} | {r.design.slice_us} | {r.design.long} | ' +
                     ' | '.join(cells) + f' | {r.margin:+.4f} | {"yes" if r.holds else "no"} | {r.load:.3f} | '
                     f'{r.long_load:.3f} | {"none" if r.even_us is None else r.even_us} |')
    return lines


def tier1_needs(pool: list[Result], bounds: dict) -> list[str]:
    """The least tier-1 bound at which a candidate holds every row, every other row within its own bound and the load
    held: with R4L, and without it (its notice's cost a stated input, not a measurement)."""
    tier1 = [r for r in rows_tiers.TIER1_ROWS]
    out = ['| Tier-1 rows held | Least tier-1 bound a candidate needs, ms | At | Its tier-1 rows, ms |',
           '|---|---:|---|---|']
    for name, rows_held in (('all', tier1), ('all but R4L', [r for r in tier1 if r != 'R4L'])):
        fit = [r for r in pool if max(r.load, r.long_load) <= LOAD_CEILING and
               all(w is not None and w <= bounds[x] for x, (w, _) in r.rows.items() if x not in tier1)]
        top = min(fit, key=lambda r: max(r.rows[x][0] for x in rows_held))
        need = max(top.rows[x][0] for x in rows_held)
        out.append(f'| {name} | {need:.2f} | {top.design.label()} | ' +
                   ', '.join(f'{x} {top.rows[x][0]:.2f}' for x in rows_held) + ' |')
    return out


def best(results: list[Result]) -> Result:
    """The candidate with the largest least relative margin, a tie to the built order, then the larger slice."""
    return max(results, key=lambda r: (r.margin, r.design.tier1 == rows_tiers.BUILT.tier1, r.design.slice_us))


def terms(root: Path, point: str, d: rows_tiers.Design) -> list[str]:
    """Every term of every row of a design (rows_tiers.report)."""
    return rows_tiers.report(root, d, (point,), every=True)


def every_notice_long(root: Path, point: str, d: rows_tiers.Design) -> list[str]:
    """A design's rows with every AECP owed frame in every row the largest legal notice: what that source adds to the
    rows that charge the stated notice (indicative; the notice's cost is a stated input, not a measurement)."""
    i = rows_tiers.point_inputs(root, point)
    long = i._replace(c={**i.c, 'item.aecp': max(i.c['item.aecp'], i.c['item.aecp.long'])})
    bounds = rows_tiers.bounds_at(i)
    held = rows_tiers.rows(root, point, d, long)
    return [f'| {d.label()} | ' + ' | '.join('none' if w is None else f'{w:.2f} ({w - bounds[row]:+.2f})'
                                             for row, (w, _) in ((row, held[row]) for row in ROWS)) + ' |']


def run(root: Path, point: str, out: Path | None) -> int:
    """Solve the grid, print the summary, write the tables; 0 when a candidate holds, 1 when none does, 2 when the
    grid's built candidate is not the built design's rows."""
    i = rows_tiers.point_inputs(root, point)
    bounds, at = rows_tiers.bounds_at(i), loads(root, point)
    built = rows_tiers.at_point(rows_tiers.BUILT, i)
    searched = tuple(CAPS) + tuple(QUOTAS)
    results, refused = {}, {}
    for order in (*searched, *REPORTED):
        designs = candidates(i, (order,))
        why = {d: rows_tiers.broken(root, d, (point,)) for d in designs}
        refused[order] = [(d, why[d][0]) for d in designs if why[d]]
        results[order] = [solve(root, point, d, i, at) for d in designs if not why[d]]
    mine = next(r for r in results['aecp-first'] if r.design.cap == 2 and r.design.slice_us == built.slice_us and
                r.design.long == 'buffer')
    if mine.rows != rows_tiers.rows(root, point, built, i):
        print('the grid\'s built candidate is not the built design\'s rows')
        return 2
    pool = [r for order in searched for r in results[order]]
    held = [r for r in pool if r.holds]
    lines = [f'Point {point}: {len(pool)} candidates solved and {sum(len(refused[o]) for o in searched)} refused by '
             f'their own rules; {len(held)} hold every row and the load (load at the pin {at[0]:.3f}, {at[1]:.3f} with '
             'every notice the largest legal one).', '']
    lines += ['| Order | Solved | Refused | Hold | Best: cap or quotas, slice, long notices | Its least margin | '
              'Its rows over their bounds |', '|---|---:|---:|---:|---|---:|---|']
    for order in (*searched, *REPORTED):
        top = best(results[order])
        over = ', '.join(f'{row} {w:.2f}' for row, (w, _) in top.rows.items() if w is None or w > bounds[row])
        lines.append(f'| {order}{" (reported)" if order in REPORTED else ""} | {len(results[order])} | '
                     f'{len(refused[order])} | {sum(r.holds for r in results[order])} | {shape(top.design)}, '
                     f'{top.design.slice_us} us, {top.design.long} | {top.margin:+.4f} | {over or "none"} |')
    lines += ['', *tier1_needs(pool, bounds)]
    lines += ['', '| Row | Bound, ms | Best W over the grid, ms | At | Built design |', '|---|---:|---:|---|---:|']
    for row in ROWS:
        top = min(pool, key=lambda r, x=row: (r.rows[x][0] is None, r.rows[x][0] or 0))
        w = top.rows[row][0]
        lines.append(f'| {row} | {bounds[row]} | {w:.2f} | {top.design.label()} | {mine.rows[row][0]:.2f} |')
    chosen = best(held) if held else None
    lines += ['', f'CHOSEN: {chosen.design.label()}, least margin {chosen.margin:+.4f}' if chosen else
              'NO CANDIDATE HOLDS every row by every source within its bound and the load within '
              f'{LOAD_CEILING:.2f} at {point}.']
    print('\n'.join(lines))
    if out:
        write(root, point, out, results, lines, chosen)
        for order, rs in refused.items():
            with (out / f'{order}.md').open('a') as f:
                f.write(''.join(f'| {order} | {shape(d)} | {d.slice_us} | {d.long} | refused: {why} |\n'
                                for d, why in rs))
    return 0 if held else 1


def write(root: Path, point: str, out: Path, results: dict, summary: list[str], chosen: Result | None) -> None:
    """Each order's table, the summary, and every term of the chosen or each order's best and of the built design."""
    bounds = rows_tiers.bounds_at(rows_tiers.point_inputs(root, point))
    out.mkdir(parents=True, exist_ok=True)
    for order, rs in results.items():
        (out / f'{order}.md').write_text('\n'.join([f'# {order} at {point}', ''] + table(rs, bounds)) + '\n')
    (out / 'summary.md').write_text('\n'.join(summary) + '\n')
    shown = [chosen.design] if chosen else [best(rs).design for rs in results.values()]
    built = rows_tiers.at_point(rows_tiers.BUILT, rows_tiers.point_inputs(root, point))
    lines = []
    for d in [built, *shown]:
        lines += terms(root, point, d) + ['']
    (out / 'terms.md').write_text('\n'.join(lines))
    long = ['| Design | ' + ' | '.join(ROWS) + ' |', '|---|' + '---:|' * len(ROWS)]
    for d in [built, *shown]:
        long += every_notice_long(root, point, d)
    (out / 'every-notice-long.md').write_text('\n'.join(long) + '\n')


def main() -> int:
    """Solve the grid at a point."""
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--point', choices=rows_tiers.POINTS, default='1x1/1if')
    ap.add_argument('--out', type=Path)
    args = ap.parse_args()
    return run(ROOT, args.point, args.out)


if __name__ == '__main__':
    sys.exit(main())
