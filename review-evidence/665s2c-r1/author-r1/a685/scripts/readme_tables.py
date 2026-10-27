#!/usr/bin/env python3
"""Print the README's instruction-cache tables from the graded results and the area runs.

usage: readme_tables.py BUILDS OOC_SWEEP_DIR YOSYS_SWEEP_JSON
BUILDS holds one build directory per arm (P1-<geometry>, P8-<geometry>, B1-/B8-/S1-/S8-,
P1-xip-/P8-xip-), each with its run.py results. Every figure is read from those files.
"""
import json
import re
import sys
from pathlib import Path

B, OOC, YOSYS = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
GEOMETRIES = (('none', 'none (S2)'), ('32x1', '2 KiB, 1 way'), ('64x1', '4 KiB, 1 way (split)'),
              ('128x1', '8 KiB, 1 way'), ('64x2', '8 KiB, 2 ways'), ('256x1', '16 KiB, 1 way'))
NETLIST = {'none': 'VexiiRiscvLitex_1e5f104c82c5f164d7a5893971248b56',
           '32x1': 'VexiiRiscvLitex_61319afc1650f6fd5b3ee1dcc49c4890',
           '64x1': 'VexiiRiscvLitex_2c4bb987d123aab6d38527891a2d9fd1',
           '128x1': 'VexiiRiscvLitex_e24c768bffcaa0dea813a890d13dd690',
           '64x2': 'VexiiRiscvLitex_a7c60866a6f9b89a7b14f6aa92648745',
           '256x1': 'VexiiRiscvLitex_c7d640635d5c7ba3667dac3fa3eee953',
           '128x2': 'VexiiRiscvLitex_e7a89a57f990e4f5da73a2e2cbf42982',
           '512x1': 'VexiiRiscvLitex_a0c06ad628d5b7d3d1e4126dbf13d26e'}


def results(arm: str) -> dict | None:
    path = B / arm / 'results/results.json'
    return json.loads(path.read_text()) if path.exists() else None


def passes(r: dict) -> dict:
    gs = r['results']
    idle = [g['passes'][k] for g in gs for k in ('idle_min', 'idle_max') if g['passes'][k]]
    worst = max(gs, key=lambda g: g['passes']['worst']['cycles'])
    windows = [g['passes']['composed'] for g in gs if g['passes']['composed'] and g['group'] != 'fixture']
    served = [w for w in windows if w.get('serviced', True)]
    starved = [w for w in windows if not w.get('serviced', True)]
    return dict(idle=(min(idle), max(idle)) if idle else None, worst=worst['passes']['worst']['ms'],
                composed=max((w['ms'] for w in served), default=None),
                starved=max((w['ms'] for w in starved), default=None))


def util(d: Path, name: str) -> dict:
    text = (d / name).read_text()

    def field(label: str) -> float:
        m = re.search(rf'^\|\s*{re.escape(label)}\s*\|\s*([\d.]+)\s*\|', text, re.M)
        return float(m.group(1)) if m else 0.0
    return dict(lut=field('Slice LUTs*'), ff=field('Slice Registers'), tiles=field('Block RAM Tile'),
                r36=field('RAMB36/FIFO*'), r18=field('RAMB18'))


def wns(d: Path) -> str:
    text = (d / 'timing.rpt').read_text()
    m = re.search(r'WNS\(ns\)\s+TNS\(ns\).*?\n\s*-+.*?\n\s*([-\d.]+)\s+\S+\s+\S+\s+\S+\s+([-\d.]+)', text, re.S)
    return f'{float(m.group(1)):+.3f} / {float(m.group(2)):+.3f}'


def ms(v: float | None) -> str:
    return '-' if v is None else f'{v:.2f}'


def sweep() -> None:
    base = util(OOC / NETLIST['none'], 'synth_util.rpt')
    print('| Instruction cache | Tiles, out of context (difference) | 1x1: composed maximum, ms | 1x1: under an unreleased '
          'load, at least | 1x1: paths (instances) missing T_svc | 8x8: composed maximum, ms | 8x8: under an unreleased '
          'load, at least | 8x8: paths (instances) missing T_svc |')
    print('|---|---:|---:|---:|---:|---:|---:|---:|')
    for geometry, label in GEOMETRIES:
        u = util(OOC / NETLIST[geometry], 'synth_util.rpt')
        cells = [label, f"{u['tiles']:g} ({u['tiles'] - base['tiles']:+g})"]
        for point in ('P1', 'P8'):
            r = results(f'{point}-{geometry}')
            if not r:
                cells += ['-', '-', '-']
                continue
            p, c = passes(r), r['counts']
            cells += [ms(p['composed']), ms(p['starved']),
                      f"{c['path_misses']} of {c['paths']} ({c['instance_misses']} of {c['instances']})"]
        print('| ' + ' | '.join(cells) + ' |')


def area() -> None:
    yosys = {Path(r['netlist']).stem: r for r in json.loads(YOSYS.read_text())}
    print('| Instruction cache | Vivado LUT / FF | Vivado RAMB36 / RAMB18 (tiles) | Routed WNS / WHS at 20 / 10 ns, ns '
          '| Yosys LUT (with LUTRAM) / FF | Yosys RAMB36 / RAMB18 |')
    print('|---|---:|---:|---:|---:|---:|')
    for geometry, label in (*GEOMETRIES, ('128x2', '16 KiB, 2 ways'), ('512x1', '32 KiB, 1 way')):
        d = OOC / NETLIST[geometry]
        u, y = util(d, 'synth_util.rpt'), yosys[NETLIST[geometry]]
        print(f"| {label} | {u['lut']:,.0f} / {u['ff']:,.0f} | {u['r36']:g} / {u['r18']:g} ({u['tiles']:g}) | {wns(d)} | "
              f"{y['LUT_TOT']:,} / {y['FF']:,} | {y['RAMB36']} / {y['RAMB18']} |")


def cpu() -> None:
    print('| Point, instruction cache | CPU cycles per instruction | Fetch commands per 1,000 instructions | Mean fetch '
          'wait, CPU cycles | Fetch waits / cycles | Data waits / cycles |')
    print('|---|---:|---:|---:|---:|---:|')
    for point, name in (('P1', '1x1'), ('P8', '8x8')):
        for geometry, label in (('none', 'none'), ('64x1', '4 KiB'), ('128x1', '8 KiB')):
            r = results(f'{point}-{geometry}')
            if not r:
                continue
            t = dict(cpu=0, instr=0, fetch=0, fwait=0, dwait=0)
            for g in r['results']:
                s = g['summary']
                t['cpu'] += int(s['cpu'])
                t['instr'] += int(s['instr'])
                for key, value in s.items():
                    n, w, *_ = (int(v) for v in value.split('/')) if '/' in value else (0, 0)
                    if key.startswith('fetch_'):
                        t['fetch'] += n
                        t['fwait'] += w
                    elif key.startswith(('load_', 'store_')):
                        t['dwait'] += w
            print(f"| {name}, {label} | {t['cpu'] / t['instr']:.2f} | {1000 * t['fetch'] / t['instr']:.1f} | "
                  f"{t['fwait'] / max(1, t['fetch']):.1f} | {t['fwait'] / t['cpu']:.3f} | {t['dwait'] / t['cpu']:.3f} |")


def worst_cell(r: dict | None, path: str, interface: int = 0) -> str:
    if not r:
        return '-'
    e = next((e for e in r['paths'] if e['path'] == path and e['interface'] == interface), None)
    if not e:
        return '-'
    w = e['worst']
    mark = '' if w['within_t_svc'] else (' **miss**' if w['within_ceiling'] else ' **over ceiling**')
    bound = f" ({w['bound_ms']:.2f})" if 'bound_ms' in w else ''
    return f"{w['ms']:.2f}{bound}{mark}"


def backlog() -> None:
    rows = (('an event behind 15 others', 'backlog.event'),
            ('an ACMP command behind a full acmp ring', 'backlog.acmp_command'),
            ('an ENTITY_AVAILABLE behind the adp ring at its burst (observed)', 'backlog.adp_available'),
            ("the same, its bucket refilling up to the ring's room (observed)", 'backlog.adp_available_refill'),
            ('a response with 7 frames owed ahead of it', 'backlog.owed'))
    arms = ('P1-none', 'P1-64x1', 'P8-none', 'P8-64x1', 'B1-64x1', 'B8-64x1')
    print('| Backlog row | A 1x1, none | A 1x1, 4 KiB | A 8x8, none | A 8x8, 4 KiB | B 1x1, 4 KiB | B 8x8, 4 KiB |')
    print('|---|---:|---:|---:|---:|---:|---:|')
    loaded = {a: results(a) for a in arms}
    for label, path in rows:
        print(f'| {label} | ' + ' | '.join(worst_cell(loaded[a], path) for a in arms) + ' |')


def fanout() -> None:
    p1n, p1c, p8n, p8c = (results(a) for a in ('P1-none', 'P1-64x1', 'P8-none', 'P8-64x1'))
    keys = sorted({(e['path'], e['interface']) for r in (p1c, p8c) if r for e in r['paths']
                   if e['path'].startswith('aecp_fanout.')})
    print('| Fan-out at registration capacity | Interface | 1x1, none | 1x1, 4 KiB | 8x8, none | 8x8, 4 KiB |')
    print('|---|---:|---:|---:|---:|---:|')
    for path, interface in keys:
        cells = [worst_cell(r, path, interface) if (interface == 0 or r in (p8n, p8c)) else '-'
                 for r in (p1n, p1c, p8n, p8c)]
        print(f"| `{path.split('.', 1)[1]}` | {interface} | " + ' | '.join(cells) + ' |')


def still_missing() -> None:
    for point, name in (('P1', '1x1'), ('P8', '8x8')):
        none, cached = results(f'{point}-none'), results(f'{point}-64x1')
        if not cached:
            continue
        print(f'\n| {name}: path missing T_svc with the 4 KiB cache | Interface | none, ms (bound) | 4 KiB, ms (bound) '
              '| 4 KiB, CPU cycles |')
        print('|---|---:|---:|---:|---:|')
        for e in sorted(cached['paths'], key=lambda e: (e['path'], e['interface'])):
            if e['misses']:
                print(f"| {e['row']} | {e['interface']} | {worst_cell(none, e['path'], e['interface'])} | "
                      f"{worst_cell(cached, e['path'], e['interface'])} | {e['worst']['cpu_cycles']:,} |")


def counts() -> None:
    print('| Arm, with the 4 KiB cache | Groups | Paths missing T_svc | Probe instances missing T_svc | Without the cache '
          '(S2), paths / instances |')
    print('|---|---:|---:|---:|---:|')
    s2 = {'A1': ('22 of 81', '58 of 141'), 'A8': ('60 of 129', '102 of 182'), 'B1': ('18 of 44', '41 of 68'),
          'B8': ('36 of 68', '60 of 92'), 'S1': ('0 of 1', '0 of 2'), 'S8': ('0 of 2', '0 of 3')}
    for label, arm in (('A1', 'P1-64x1'), ('A8', 'P8-64x1'), ('B1', 'B1-64x1'), ('B8', 'B8-64x1'), ('S1', 'S1-64x1'),
                       ('S8', 'S8-64x1')):
        r = results(arm)
        if not r:
            continue
        c = r['counts']
        print(f"| {label} | {len(r['results'])} | {c['path_misses']} of {c['paths']} | {c['instance_misses']} of "
              f"{c['instances']} | {s2[label][0]} / {s2[label][1]} |")


def xip() -> None:
    print('| Point, instruction cache, code | Planned block RAM, tiles | CPU cycles per instruction | Mean refill, CPU '
          'cycles | Groups graded, probes refused | Paths (instances) missing T_svc | Composed maximum, ms (or under an '
          'unreleased load, at least) | Worst pass, ms |')
    print('|---|---:|---:|---:|---:|---:|---:|---:|')
    for point, name in (('P1', '1x1'), ('P8', '8x8')):
        for geometry, label, xip_arm in (('64x1', '4 KiB, block RAM', False), ('64x1', '4 KiB, flash', True),
                                         ('512x1', '32 KiB, flash', True)):
            arm = f'{point}-xip-{geometry}' if xip_arm else f'{point}-{geometry}'
            if not (B / arm / 'build.json').exists():
                continue
            tiles = json.loads((B / arm / 'build.json').read_text())['ctrl_plan']['tiles']
            r = results(arm)
            if not r:
                print(f'| {name}, {label} | {tiles:g} | - | - | - | - | - | - |')
                continue
            t = dict(cpu=0, instr=0, fetch=0, fwait=0)
            for g in r['results']:
                summary = g['summary']
                t['cpu'] += int(summary['cpu'])
                t['instr'] += int(summary['instr'])
                for key, value in summary.items():
                    if key.startswith('fetch_'):
                        n, w, *_ = (int(v) for v in value.split('/'))
                        t['fetch'] += n
                        t['fwait'] += w
            p, c = passes(r), r['counts']
            comp = ms(p['composed']) if p['composed'] is not None else f"({ms(p['starved'])})"
            print(f"| {name}, {label} | {tiles:g} | {t['cpu'] / t['instr']:.2f} | {t['fwait'] / max(1, t['fetch']):,.0f} | "
                  f"{len(r['results'])}, {len(r['refusals'])} | {c['path_misses']} of {c['paths']} ({c['instance_misses']} "
                  f"of {c['instances']}) | {comp} | {ms(p['worst'])} |")


if __name__ == '__main__':
    for section in sys.argv[4:] or ('sweep', 'counts', 'area', 'cpu', 'backlog', 'fanout', 'still_missing', 'xip'):
        print(f'\n<!-- {section} -->\n')
        globals()[section]()
