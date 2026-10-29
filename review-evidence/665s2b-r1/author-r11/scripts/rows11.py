#!/usr/bin/env python3
"""Scratch: every composed row's worst instance over the four backlog groups, and every group's passes against the
per-pass share, for the round-11 legs at both CPU clocks.

usage: rows11.py RESULTS_ROOT OUT_DIR
RESULTS_ROOT holds one directory per leg, named {N,D}11-{A,B}{1,8}-{50,100}, each with results.json (or
results.json.gz) and build.json. A row's bound is min(T_svc, its family's ceiling) plus its normative wait (FR_NFR.md
3.4.1), from the lane's scenario.py; the share is the lane's share.py. Every table names the CPU clock of its columns
from each leg's build.json, and refuses a leg whose clock is not the one its name says.
Cells are arm A / arm B in ms, bold over the bound; "never" is a command never answered or a record never released.
The owed window holds the egress for 60 ms, so its last AECP record, whose response waits for it, is its own row."""
import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, '$LANES/665-s2b-cycles/tb/verilator/ctrl_service_budget')
import scenario  # noqa: E402
import share  # noqa: E402

GROUPS = ('backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed')
CLOCKS = {'50': 50_000_000, '100': 100_000_000}
NAMES = {f'{f} record released under the composed load, {w}': f'{f} record, {w}'
         for f in ('ACMP', 'ADP', 'MAAP', 'AECP', 'SRP') for w in ('first', 'last')}
COLUMNS = (('N', '50', 'CPU 50 MHz (product)'), ('D', '50', 'CPU 50 MHz (product), with both drafts'),
           ('N', '100', 'CPU 100 MHz (labelled option)'), ('D', '100', 'CPU 100 MHz (labelled option), with both drafts'))


def load(leg: Path) -> tuple[dict, dict]:
    """A leg's results and build record; refuses a leg whose recorded CPU clock is not its name's."""
    path = leg / 'results.json'
    raw = path.read_bytes() if path.is_file() else gzip.decompress((leg / 'results.json.gz').read_bytes())
    spec = json.loads((leg / 'build.json').read_text())
    want = CLOCKS[leg.name.rsplit('-', 1)[1]]
    if spec['cpu_hz'] != want or spec['product_cpu_hz'] != 50_000_000 or \
            spec['cpu_clock'] != ('product' if want == 50_000_000 else 'option'):
        raise SystemExit(f'{leg.name}: build.json records CPU {spec["cpu_hz"]} ({spec.get("cpu_clock")}), not {want}')
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
                row += ', in the owed window'     # its responses wait for the held egress
            key = (never, r['ms'])
            if row not in out or key > out[row][0]:
                out[row] = (key, not never and r['ms'] <= bound(r), bound(r), r['family'], g['group'], r['probe'])
    return out


def cell(entry) -> str:
    if entry is None:
        return '-'
    (never, ms), fits = entry[0], entry[1]
    text = 'never' if never else f'{ms:.2f}'
    return text if fits else f'**{text}**'


def rows_table(point: str, legs: dict) -> list[str]:
    cols = [c for c in COLUMNS if (c[0], 'A', point, c[1]) in legs and (c[0], 'B', point, c[1]) in legs]
    w = {(d, arm, clk): worst(legs[(d, arm, point, clk)][0]) for d, clk, _ in cols for arm in 'AB'}
    rows = sorted(set().union(*w.values()))
    out = [f'| {point}: row | Bound, ms | ' + ' | '.join(label for _, _, label in cols) + ' |',
           '|---|---:|' + '---:|' * len(cols)]
    for row in rows:
        entry = next(e for e in (w[k].get(row) for k in w) if e)
        cells = [f"{cell(w[(d, 'A', clk)].get(row))} / {cell(w[(d, 'B', clk)].get(row))}" for d, clk, _ in cols]
        out.append(f'| {row} | {entry[2]:g} | ' + ' | '.join(cells) + ' |')
    return out


def residual_table(point: str, legs: dict) -> list[str]:
    """Every row over its bound in any leg: the worst instance's excess, per leg."""
    out = [f'| {point}: row over its bound | Leg | Bound, ms | Worst instance | ms | Over by, ms |',
           '|---|---|---:|---|---:|---:|']
    for (d, arm, pt, clk), (results, _) in sorted(legs.items()):
        if pt != point:
            continue
        for row, e in sorted(worst(results).items()):
            (never, ms), fits, b, _, group, probe = e
            if not fits:
                over = 'unbounded' if never else f'{ms - b:.2f}'
                out.append(f"| {row} | {d}11-{arm}{pt[0]}-{clk} | {b:g} | `{probe}` | "
                           f"{'at least ' if never else ''}{ms:.2f} | {over} |")
    return out


def share_table(point: str, legs: dict) -> list[str]:
    out = [f'| {point}: leg | CPU clock | Share, CPU cycles | Group | Work passes | Over the share | '
           'Longest pass, CPU cycles (ms) | Over by, ms | Its largest modules, CPU cycles |',
           '|---|---|---:|---|---:|---:|---:|---:|---|']
    for (d, arm, pt, clk), (results, spec) in sorted(legs.items()):
        if pt != point:
            continue
        for g in results['results']:
            s, top = g['passes']['share'], g['passes']['worst']
            mods = ', '.join(f'{m} {c:,}' for m, c in sorted(top['modules'].items(), key=lambda kv: -kv[1])[:4])
            over = f"{top['ms'] - s['ms']:.3f}" if s['over'] else '-'
            out.append(f"| {d}11-{arm}{pt[0]}-{clk} | {spec['cpu_hz'] // 1_000_000} MHz | {s['cycles']:,} | {g['group']} | "
                       f"{s['passes']} | {s['over']} | {top['cycles']:,} ({top['ms']:.3f}) | {over} | {mods} |")
    return out


def main() -> int:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    legs = {}
    for leg in sorted(root.iterdir()):
        if not (leg / 'build.json').is_file():
            continue
        tag, clk = leg.name.split('-')[0], leg.name.rsplit('-', 1)[1]
        arm, pt = leg.name.split('-')[1][0], {'1': '1x1', '8': '8x8'}[leg.name.split('-')[1][1]]
        legs[(tag[0], arm, pt, clk)] = load(leg)
    head = [f'Share: {share.bound_ms():g} ms over {share.SHARE_PASSES} passes, {share.share_ms():.3f} ms of CPU time.',
            f"Legs: {', '.join(f'{d}11-{a}{p[0]}-{c}' for d, a, p, c in sorted(legs))}.", '']
    for point in ('1x1', '8x8'):
        text = head + rows_table(point, legs) + [''] + residual_table(point, legs) + [''] + share_table(point, legs)
        (out / f'rows-{point}.md').write_text('\n'.join(text) + '\n')
        print('\n'.join(text) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
