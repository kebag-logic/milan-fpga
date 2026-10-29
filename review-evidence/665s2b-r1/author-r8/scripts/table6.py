#!/usr/bin/env python3
"""Scratch: every composed row before and after, and the instruction-cache refills of each composed window.

usage: table6.py rows POINT LABEL=A_RESULTS,B_RESULTS ...
       table6.py misses POINT LABEL=A_DIR,B_DIR ...
rows: rows.py's worst instance over the four backlog groups for every composed row (the owed window's AECP record its
own row), one column per run, cells arm A / arm B in ms, bold where an arm misses T_svc, "never" for a command
never answered.
misses: per backlog group, its composed window (from its first loaded record's commit to its last record's release,
the grader's service probes), the line refills of the work passes overlapping it (the PASS lines' fetch_rom count),
their wait in ms at the run's CPU clock, and the passes; cells arm A / arm B."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rows import GROUPS, load, worst  # noqa: E402


def cell(entry):
    if entry is None:
        return '-', True
    (never, ms), fits, _ = entry
    return ('never' if never else f'{ms:.2f}'), fits


def rows(point: str, specs: list[str]) -> None:
    runs = []
    for spec in specs:
        label, _, paths = spec.partition('=')
        a, b = paths.split(',')
        runs.append((label, worst(load(a)), worst(load(b))))
    every = sorted(set().union(*(set(wa) | set(wb) for _, wa, wb in runs)))
    print(f'| {point}: row | ' + ' | '.join(label for label, _, _ in runs) + ' |')
    print('|---|' + '---:|' * len(runs))
    for row in every:
        out = []
        for _, wa, wb in runs:
            (ta, fa), (tb, fb) = cell(wa.get(row)), cell(wb.get(row))
            out.append(f'{ta if fa else f"**{ta}**"} / {tb if fb else f"**{tb}**"}')
        print(f'| {row} | ' + ' | '.join(out) + ' |')


def window(results: Path, group: str) -> tuple[int, int, float, int]:
    res = json.loads((results / f'{group}.json').read_text())
    svc = [p for p in res['probes'] if '.service.' in p['probe'] and p.get('end_sys')]
    start, end = min(p['start_sys'] for p in svc), max(p['end_sys'] for p in svc)
    spec = json.loads((results.parent / 'soc.json').read_text())
    ratio = spec['sys_hz'] / spec['cpu_hz']
    refills = wait = passes = 0
    for line in (results / f'{group}.log').read_text().splitlines():
        if not line.startswith('PASS '):
            continue
        f = line.split()
        s, c = int(f[2]), int(f[4])
        if s < end and s + c * ratio > start:
            passes += 1
            for kv in f[6:]:
                k, _, v = kv.partition('=')
                if k == 'fetch_rom':
                    n, w = v.split('/')
                    refills += int(n)
                    wait += int(w)
    return refills, passes, wait * 1000.0 / spec['cpu_hz'], end - start


def misses(point: str, specs: list[str]) -> None:
    runs = []
    for spec in specs:
        label, _, paths = spec.partition('=')
        a, b = (Path(p) for p in paths.split(','))
        runs.append((label, a, b))
    print(f'| {point}: window | ' + ' | '.join(f'{label}: refills (wait, ms)' for label, _, _ in runs) + ' |')
    print('|---|' + '---:|' * len(runs))
    for g in GROUPS:
        out = []
        for _, a, b in runs:
            ra, _, wa, _ = window(a, g)
            rb, _, wb, _ = window(b, g)
            out.append(f'{ra:,} ({wa:.2f}) / {rb:,} ({wb:.2f})')
        print(f'| `{g}` | ' + ' | '.join(out) + ' |')


if __name__ == '__main__':
    {'rows': rows, 'misses': misses}[sys.argv[1]](sys.argv[2], sys.argv[3:])
