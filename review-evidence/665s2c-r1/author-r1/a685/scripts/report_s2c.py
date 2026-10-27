#!/usr/bin/env python3
"""Render the lane's comparison tables from the harness's results.json of each arm.

usage: report_s2c.py OUT.md ARM=RESULTS_DIR [ARM=RESULTS_DIR ...]
An arm is named P<point>-<geometry>[-<label>], P1 the 1x1 point with one interface and P8 the
8x8 point with two; its RESULTS_DIR is a run.py --out directory. Every figure is read from the
graded results.json (run.py paths(), each group's passes and summary); nothing is restated.
"""
import json
import sys
from pathlib import Path

ARMS = {}
for spec in sys.argv[2:]:
    name, _, path = spec.partition('=')
    ARMS[name] = json.loads((Path(path) / 'results.json').read_text())
POINTS = {'P1': '1x1, one interface', 'P8': '8x8, two interfaces'}


def groups(arm: str) -> dict:
    return {g['group']: g for g in ARMS[arm]['results']}


def stat(text: str) -> tuple[int, int, int, int]:
    """count/sum/min/max of a SUMMARY counter."""
    return tuple(int(v) for v in text.split('/'))


def passes(arm: str) -> dict:
    gs = groups(arm)
    idle_min = min((g['passes']['idle_min'] for g in gs.values() if g['passes']['idle_min']), default=0)
    idle_max = max((g['passes']['idle_max'] for g in gs.values() if g['passes']['idle_max']), default=0)
    worst = max(gs.values(), key=lambda g: g['passes']['worst']['cycles'])
    windows = [(g['passes']['composed'], n) for n, g in gs.items() if g['passes']['composed'] and n != 'fixture']
    # S2 round 3: the composed maximum is the longest pass of a window that released its whole load;
    # a window that left records unreleased gives a lower bound.
    serviced = [w for w in windows if w[0].get('serviced', True)]
    starved = [w for w in windows if not w[0].get('serviced', True)]
    comp, comp_group = max(serviced, key=lambda c: c[0]['cycles']) if serviced else ({}, '-')
    low, low_group = max(starved, key=lambda c: c[0]['cycles']) if starved else ({}, '-')
    return dict(idle_min=idle_min, idle_max=idle_max, worst=worst['passes']['worst'], worst_group=worst['group'],
                composed=comp, composed_group=comp_group, starved=low, starved_group=low_group,
                unreleased={n: w['unreleased'] for w, n in starved})


def cpu(arm: str) -> dict:
    """Totals over every group's run: cycles, instructions, fetch commands and waits, data waits."""
    tot = dict(cpu=0, instr=0, fetch=0, fetch_wait=0, data=0, data_wait=0, mbx=0)
    for g in groups(arm).values():
        s = g['summary']
        tot['cpu'] += int(s['cpu'])
        tot['instr'] += int(s['instr'])
        for key, value in s.items():
            if key.startswith('fetch_'):
                n, w, _, _ = stat(value)
                tot['fetch'] += n
                tot['fetch_wait'] += w
            elif key.startswith(('load_', 'store_')):
                n, w, _, _ = stat(value)
                tot['data'] += n
                tot['data_wait'] += w
    return tot


def cell(entry: dict | None) -> str:
    if not entry:
        return '-'
    w = entry['worst']
    mark = '' if w['within_t_svc'] else (' **miss**' if w['within_ceiling'] else ' **over ceiling**')
    bound = f" ({w['bound_ms']:.2f})" if 'bound_ms' in w else ''
    return f"{w['ms']:.2f}{bound}{mark}"


def by_path(arm: str) -> dict:
    return {(e['path'], e['interface']): e for e in ARMS[arm]['paths']}


def summary_table() -> list[str]:
    out = ['| Arm | Groups | Refusals | Paths missing T_svc | Instances missing T_svc | Idle pass, CPU cycles (ms) '
           '| Worst pass, CPU cycles (ms), group | Composed maximum, CPU cycles (ms), group '
           '| Longest pass under a load left unreleased (lower bound) |',
           '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for arm, r in ARMS.items():
        c, p = r['counts'], passes(arm)
        comp, low = p['composed'], p['starved']
        comp_cell = f"{comp['cycles']:,} ({comp['ms']:.2f}), {p['composed_group']}" if comp else '-'
        low_cell = f"{low['cycles']:,} ({low['ms']:.2f}), {p['starved_group']}" if low else '-'
        out.append(f"| {arm} | {len(r['results'])} | {len(r['refusals'])} | {c['path_misses']} of {c['paths']} | "
                   f"{c['instance_misses']} of {c['instances']} | {p['idle_min']:,} to {p['idle_max']:,} "
                   f"({p['idle_min'] / 50000:.2f} to {p['idle_max'] / 50000:.2f}) | {p['worst']['cycles']:,} "
                   f"({p['worst']['ms']:.2f}), {p['worst_group']} | {comp_cell} | {low_cell} |")
    return out


def cpu_table() -> list[str]:
    out = ['| Arm | CPU cycles per instruction | Fetch commands per 1,000 instructions | Mean fetch wait, CPU cycles '
           '| Fetch waits / cycles | Data accesses per instruction | Data waits / cycles |',
           '|---|---:|---:|---:|---:|---:|---:|']
    for arm in ARMS:
        t = cpu(arm)
        out.append(f"| {arm} | {t['cpu'] / t['instr']:.2f} | {1000 * t['fetch'] / t['instr']:.1f} | "
                   f"{t['fetch_wait'] / max(1, t['fetch']):.1f} | {t['fetch_wait'] / t['cpu']:.3f} | "
                   f"{t['data'] / t['instr']:.3f} | {t['data_wait'] / t['cpu']:.3f} |")
    return out


BACKLOG = (('an event behind 15 others', 'backlog.event'),
           ('an ACMP command behind a full acmp ring', 'backlog.acmp_command'),
           ('an ENTITY_AVAILABLE behind the adp ring at its burst (observed)', 'backlog.adp_available'),
           ("the same, its bucket refilling up to the ring's room (observed)", 'backlog.adp_available_refill'),
           ('a response with 7 frames owed ahead of it', 'backlog.owed'))


def backlog_table(point: str) -> list[str]:
    arms = [a for a in ARMS if a.startswith(point + '-')]
    out = [f"| Backlog row, {POINTS[point]}, ms (bound) | " + ' | '.join(arms) + ' |',
           '|---|' + '---:|' * len(arms)]
    for label, path in BACKLOG:
        out.append(f'| {label} | ' + ' | '.join(cell(by_path(a).get((path, 0))) for a in arms) + ' |')
    return out


def path_table(point: str) -> list[str]:
    arms = [a for a in ARMS if a.startswith(point + '-')]
    keys = sorted({k for a in arms for k in by_path(a)})
    out = [f"| Path, {POINTS[point]} | Interface | " + ' | '.join(f'{a} ms (bound)' for a in arms)
           + ' | ' + ' | '.join(f'{a} CPU cycles' for a in arms) + ' |',
           '|---|---:|' + '---:|' * (2 * len(arms))]
    for key in keys:
        entries = [by_path(a).get(key) for a in arms]
        row = next(e['row'] for e in entries if e)
        cycles = [f"{e['worst']['cpu_cycles']:,}" if e else '-' for e in entries]
        out.append(f'| {row} | {key[1]} | ' + ' | '.join(cell(e) for e in entries) + ' | ' + ' | '.join(cycles) + ' |')
    return out


def fanout_table(point: str) -> list[str]:
    arms = [a for a in ARMS if a.startswith(point + '-')]
    keys = sorted({k for a in arms for k, e in by_path(a).items() if 'fanout' in e['worst']
                   or k[0] in ('aecp.set_name', 'aecp.lock_entity', 'aecp.unlock_entity')})
    out = [f"| Notification path, {POINTS[point]} | Interface | " + ' | '.join(arms) + ' |',
           '|---|---:|' + '---:|' * len(arms)]
    for key in keys:
        entries = [by_path(a).get(key) for a in arms]
        out.append(f'| `{key[0]}` | {key[1]} | ' + ' | '.join(cell(e) for e in entries) + ' |')
    return out


def main() -> int:
    lines = ['# S2c comparison tables', '', 'Generated by `report_s2c.py` from each arm\'s `results.json`.', '',
             '## Arms', '', *summary_table(), '', '## CPU', '', *cpu_table(), '']
    for point in POINTS:
        if any(a.startswith(point + '-') for a in ARMS):
            lines += [f'## Backlog rows, {POINTS[point]}', '', *backlog_table(point), '',
                      f'## Notification fan-out, {POINTS[point]}', '', *fanout_table(point), '',
                      f'## Every path, {POINTS[point]}', '', *path_table(point), '']
    Path(sys.argv[1]).write_text('\n'.join(lines) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
