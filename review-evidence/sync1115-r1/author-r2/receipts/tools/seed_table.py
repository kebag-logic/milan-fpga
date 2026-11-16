#!/usr/bin/env python3
"""seed_table.py OUT.md: the LeaveAll phase spread at 8x8/1if, one row per tree, seed and group.

Each seed's clone (seeds/c-<tree>-<tag>) differs from its tree only in configs/endstation_ax7101_8x8.yaml's
mac_address (an experiment; never committed). lwSRP draws its first LeaveAll at 62 ms + 10 ms x (1001 + r % 499),
r = seed x 1664525 + 1013904223 mod 2^32, the seed the MAC's low 32 bits for MSRP and those XOR 0x91 for MVRP
(srp_mbx.c mrp_port_configure). Reads each run's results with the harness of its own clone (mrpdu_grade.resolve).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

S = Path('<scratch>')
GROUPS = ('save-held', 'save-starved')


def first_leaveall_ms(seed: int) -> int:
    r = (seed * 1664525 + 1013904223) & 0xFFFFFFFF
    return 62 + 10 * (1001 + r % 499)


def mac_of(clone: Path) -> str:
    text = (clone / 'configs/endstation_ax7101_8x8.yaml').read_text()
    return re.search(r'^  mac_address: "([0-9a-f:]+)"', text, re.M)[1]


def report(clone: Path, results: Path) -> dict:
    out = subprocess.run([sys.executable, '-B', str(S / 'bin/la_report.py'), str(clone / 'tb/verilator/ctrl_service_budget'),
                          str(results), *GROUPS], capture_output=True, text=True, timeout=900)
    groups, cur = {}, None
    for line in out.stdout.splitlines():
        m = re.match(r'GROUP (\S+) .* late_ms (\S+)', line)
        if m:
            cur = groups.setdefault(m[1], dict(late_ms=m[2], runouts=[], rows={}, timers=''))
            continue
        m = re.match(r'\s+leaveall run-out\s+([\d.]+) ms\s+(\S+)\s+first\s+([\d.]+) ms after it', line)
        if m and cur is not None:
            cur['runouts'].append((float(m[1]), m[2], float(m[3])))
        m = re.match(r'\s+ROW \S+\.mrpdu\.(\w+)\.if0 ([\d.]+) ms', line)
        if m and cur is not None:
            cur['rows'][m[1]] = float(m[2])
        m = re.match(r'\s+every MRP timer run-out: (.*)', line)
        if m and cur is not None:
            cur['timers'] = m[1]
    if out.returncode:
        groups['_error'] = out.stderr[-400:]
    return groups


def runs():
    """(tree, tag, clone, results dir, leg log) for each seed run, and the gate legs' product-MAC rows."""
    for log in sorted((S / 'seeds/logs').glob('*.log')):
        tree, tag = log.stem.split('-', 1)
        yield tree, tag, S / f'seeds/c-{tree}-{tag}', S / f'seeds/b-{tree}-{tag}/results', log
    # the sync's product MAC: arm A's parts 1 and 2 at the head (save-held, save-starved)
    yield 'sync', 'product', S / 'c-b2', None, None


def main() -> int:
    rows, worst = [], {}
    for tree, tag, clone, results, log in runs():
        mac = mac_of(clone)
        low = int(mac.replace(':', ''), 16) & 0xFFFFFFFF
        pred = (first_leaveall_ms(low), first_leaveall_ms(low ^ 0x91))
        if results is None:
            parts = {'save-held': S / 'budget2/b81/results-a1', 'save-starved': S / 'budget2/b81/results-a2'}
            got = {}
            for g, d in parts.items():
                if (d / f'{g}.json').exists():
                    got.update({k: v for k, v in report(clone, d).items() if k == g})
            end = 'arm A parts 1 and 2'
        else:
            done = log.read_text(errors='replace')
            end = re.findall(r'^END rc=(\d+)', done, re.M)
            end = f'rc {end[-1]}' if end else 'running'
            got = report(clone, results) if all((results / f'{g}.json').exists() for g in GROUPS) else {}
        for g in GROUPS:
            r = got.get(g)
            if not r:
                rows.append(f'| {tree} | {mac} | {pred[0]:,} / {pred[1]:,} | {g} | ({end}) | | | | |')
                continue
            la = r['rows'].get('leaveall')
            outs = '; '.join(f'{t:,.1f} {o} +{a:.1f}' for t, o, a in r['runouts'])
            rows.append(f"| {tree} | {mac} | {pred[0]:,} / {pred[1]:,} | {g} | {outs} | {r['timers']} | "
                        f"{la if la is not None else '-'} | {r['rows'].get('join', '-')} | {r['rows'].get('periodic', '-')} |")
            if la is not None and (tree not in worst or la > worst[tree][0]):
                worst[tree] = (la, mac, g)
    head = ['| Tree | MAC (8x8 config) | First LeaveAll drawn, MSRP / MVRP, ms | Group | LeaveAll run-outs: ms, outcome, '
            'first frame or build after it, ms | Every MRP timer run-out | mrpdu.leaveall.if0, ms | mrpdu.join.if0, ms | '
            'mrpdu.periodic.if0, ms |', '|---|---|---:|---|---|---|---:|---:|---:|']
    tail = [''] + [f'Worst `mrpdu.leaveall.if0`, {t}: {w[0]} ms ({w[2]}, MAC {w[1]})' for t, w in sorted(worst.items())]
    Path(sys.argv[1]).write_text('\n'.join(head + rows + tail) + '\n')
    print('\n'.join(tail))
    return 0


if __name__ == '__main__':
    sys.exit(main())
