#!/usr/bin/env python3
"""seed_table2.py OUT.md: the LeaveAll phase spread at 8x8/1if as one table, from each run's result JSON (its mrpdu
rows) and la_join.py's read-out of its logs (seeds/join/<run>.txt): per tree, seed and group, the MAC, the first
LeaveAll lwSRP draws for MSRP and MVRP, every LeaveAll run-out with its outcome, frame delay and the join timer's
next run-out, and the rows. The product MAC's row on the sync alone is arm A's (parts 1 and 2, budget2/b81).
"""
import json
import re
import sys
from pathlib import Path

S = Path('<scratch>')
GROUPS = ('save-held', 'save-starved')


def first_leaveall_ms(seed: int) -> int:
    r = (seed * 1664525 + 1013904223) & 0xFFFFFFFF
    return 62 + 10 * (1001 + r % 499)


def mac_of(clone: Path) -> str:
    return re.search(r'^  mac_address: "([0-9a-f:]+)"', (clone / 'configs/endstation_ax7101_8x8.yaml').read_text(), re.M)[1]


def rows_of(results: Path, group: str) -> dict:
    data = json.loads((results / f'{group}.json').read_text())
    return {p['probe'].split('.mrpdu.')[1].split('.')[0]: p['ms'] for p in data['probes'] if '.mrpdu.' in p['probe']}


def joins_of(text: str, group: str) -> list[str]:
    out = []
    for line in text.splitlines():
        m = re.match(rf'{group} leaveall\s+([\d.]+) ms (\S+)\s+frame \+\s*([\d.]+) ms; .*next join timer \+\s*([\d.]+) ms; '
                     rf'CPU busy\s+([\d.]+) ms', line)
        if m:
            out.append(f'{float(m[1]):,.1f} {m[2]} +{float(m[3]):.1f} (join +{float(m[4]):.1f}, CPU {float(m[5]):.1f})')
    return out


def main() -> int:
    runs = [(p.stem.split('-', 1)[0], p.stem, S / f'seeds/c-{p.stem}', S / f'seeds/b-{p.stem}/results')
            for p in sorted((S / 'seeds/logs').glob('*.log'))]
    runs.append(('sync', 'sync-product', S / 'c-b2', None))
    lines = ['| Tree | MAC in the 8x8 config | First LeaveAll drawn, MSRP / MVRP, ms | Group | LeaveAll run-outs: ms, outcome, '
             'frame after it, ms (the join timer\'s next run-out, ms; CPU busy in the wait, ms) | leaveall.if0, ms | '
             'join.if0, ms | periodic.if0, ms |', '|---|---|---:|---|---|---:|---:|---:|']
    worst = {}
    for tree, name, clone, results in runs:
        mac = mac_of(clone)
        low = int(mac.replace(':', ''), 16) & 0xFFFFFFFF
        drawn = f'{first_leaveall_ms(low):,} / {first_leaveall_ms(low ^ 0x91):,}'
        jt = (S / f'seeds/join/{name}.txt')
        jtext = jt.read_text() if jt.exists() else ''
        for g in GROUPS:
            res = results or S / ('budget2/b81/results-a1' if g == 'save-held' else 'budget2/b81/results-a2')
            if not (res / f'{g}.json').exists():
                lines.append(f'| {tree} | {mac} | {drawn} | {g} | (no result) | | | |')
                continue
            r = rows_of(res, g)
            outs = '; '.join(joins_of(jtext, g)) or '(see arm A)'
            lines.append(f"| {tree} | {mac} | {drawn} | {g} | {outs} | {r.get('leaveall', '-')} | {r.get('join', '-')} | "
                         f"{r.get('periodic', '-')} |")
            for kind in ('leaveall', 'periodic', 'join'):
                v = r.get(kind)
                if v is not None and (tree, kind) not in worst or (v is not None and v > worst[(tree, kind)][0]):
                    worst[(tree, kind)] = (v, mac, g)
    lines.append('')
    for (tree, kind), (v, mac, g) in sorted(worst.items()):
        lines.append(f'- worst `mrpdu.{kind}.if0`, {tree}: {v} ms ({g}, MAC {mac})')
    Path(sys.argv[1]).write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines[-6:]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
