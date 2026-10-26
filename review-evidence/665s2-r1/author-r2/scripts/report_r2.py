#!/usr/bin/env python3
"""Render the README's result tables from the final results.json of each arm.

Usage: report_r2.py FINAL_DIR
FINAL_DIR holds A1, A8, B1, B8, S1 and S8, each a regraded results directory. Every cell is a
path's worst measured instance across the arm's groups (run.py paths()), "ms (pass bound)".
"""
import json
import re
import sys
from pathlib import Path

F = Path(sys.argv[1])
ARMS = {k: json.loads((F / k / 'results.json').read_text()) for k in ('A1', 'A8', 'B1', 'B8', 'S1', 'S8')
        if (F / k / 'results.json').exists()}
PATHS = {k: {(e['path'], e['interface']): e for e in v['paths']} for k, v in ARMS.items()}
GROUPS = {k: {g['group']: g for g in v['results']} for k, v in ARMS.items()}


def worst(arm: str, path: str, interface: int = 0) -> dict | None:
    e = PATHS.get(arm, {}).get((path, interface))
    return e['worst'] if e else None


def cell(arm: str, path: str, interface: int = 0, ahead: bool = False) -> str:
    x = worst(arm, path, interface)
    if not x:
        return '-'
    mark = '' if x['within_t_svc'] else (' **miss**' if x['within_ceiling'] else ' **over ceiling**')
    bound = f" ({x['bound_ms']:.2f})" if 'bound_ms' in x else ''
    extra = f" [{x['ahead']} ahead]" if ahead else ''
    return f"{x['ms']:.2f}{bound}{mark}{extra}"


def pair(arm: str, path: str, ahead: bool = False) -> str:
    return ' / '.join(cell(arm, path, i, ahead) for i in (0, 1))


def accesses(path: str) -> str:
    a1, a8 = worst('A1', path), worst('A8', path)
    model = (a1 or a8 or {}).get('model_accesses')
    return (f"{a1.get('pass_mbx_accesses', '-') if a1 else '-'} / {a8.get('pass_mbx_accesses', '-') if a8 else '-'}"
            + (f' ({model})' if model is not None else ''))


def table(header: str, rows: list[tuple[str, str]], arms_b: bool = False, arm_a: tuple = ('A1', 'A8')) -> str:
    out = [header]
    for label, path in rows:
        cells = [cell(arm_a[0], path), pair(arm_a[1], path)]
        if arms_b:
            cells += [cell('B1', path), pair('B8', path)]
        out.append(f"| {label} | {' | '.join(cells)} | {accesses(path)} |")
    return '\n'.join(out)


def adp() -> str:
    header = ('| Path ([`MAILBOX_SPLIT.md:495-502`](../../../docs/design/MAILBOX_SPLIT.md#service-latency)) '
              '| 1x1 ms (bound) | 8x8 if0 / if1 ms (bound) | Accesses in the taking pass, 1x1 / 8x8 (model) |\n'
              '|---|---:|---:|---:|')
    rows = [('RCV_ADP_DISCOVER -> TMR_DELAY armed', 'adp.discover'),
            ('TMR_DELAY expiry -> ENTITY_AVAILABLE, TMR_ADVERTISE armed', 'adp.tmr_delay'),
            ('TMR_ADVERTISE expiry -> TMR_DELAY armed', 'adp.tmr_advertise'),
            ('GM_CHANGE -> TMR_DELAY armed', 'adp.gm_change'), ('LINK_UP -> TMR_DELAY armed', 'adp.link_up'),
            ('LINK_DOWN -> timer stopped', 'adp.link_down')]
    out = table(header, rows)
    s1, s8 = worst('S1', 'adp.shutdown'), worst('S8', 'adp.shutdown')
    if s1:
        out += (f"\n| SHUTDOWN -> ENTITY_DEPARTING (test-only entry, `shutdown-entry` arm) | {cell('S1', 'adp.shutdown')} "
                f"| {pair('S8', 'adp.shutdown')} | {s1.get('pass_mbx_accesses')} / "
                f"{s8.get('pass_mbx_accesses') if s8 else '-'} ({s1.get('model_accesses')}) |")
    return out


def acmp() -> str:
    header = ('| Path ([`MAILBOX_SPLIT.md:645-657`](../../../docs/design/MAILBOX_SPLIT.md#acmp-service-latency)) '
              '| A: 1x1 ms (bound) | A: 8x8 if0 / if1 | B: 1x1 | B: 8x8 if0 / if1 | Accesses, A 1x1 / 8x8 (model) |\n'
              '|---|---:|---:|---:|---:|---:|')
    rows = [('BIND_RX', 'acmp.bind_rx'), ('UNBIND_RX', 'acmp.unbind_rx'), ('GET_RX_STATE', 'acmp.get_rx_state'),
            ('PROBE_TX_RESPONSE', 'acmp.probe_tx_response'), ('PROBE_TX', 'acmp.probe_tx'),
            ('GET_TX_STATE', 'acmp.get_tx_state'), ('DISCONNECT_TX', 'acmp.disconnect_tx'),
            ('GET_TX_CONNECTION', 'acmp.get_tx_connection'), ('the first TMR_NO_RESP', 'acmp.tmr_no_resp1'),
            ('the second TMR_NO_RESP', 'acmp.tmr_no_resp2'), ('TMR_RETRY', 'acmp.tmr_retry'),
            ('TMR_DELAY', 'acmp.tmr_delay'), ('TMR_NO_TK', 'acmp.tmr_no_tk'),
            ('ENTITY_AVAILABLE from its RX_HEAD (H-DISC)', 'acmp.entity_available'),
            ('ENTITY_DEPARTING from its RX_HEAD (H-DISC)', 'acmp.entity_departing'),
            ('TMR_NO_ADP (H-DISC)', 'acmp.tmr_no_adp')]
    return table(header, rows, arms_b=True)


def aecp() -> str:
    header = '| AECP path | 1x1 ms (bound) | 8x8 if0 / if1 ms (bound) | Accesses, 1x1 / 8x8 |\n|---|---:|---:|---:|'
    paths = sorted({p for p, _ in PATHS['A1'] if p.startswith('aecp.')},
                   key=lambda n: (not n.startswith('aecp.read_descriptor'),
                                  int(n.split('.t')[1].split('.')[0]) if 'read_descriptor' in n else 0, n))
    rows = []
    for path in paths:
        x = worst('A1', path)
        if 'read_descriptor' in path:
            # One type's last index at 1x1; the 8x8 reads the same type at its own last index.
            kind = path.split('.t')[1].split('.')[0]
            label = f"READ_DESCRIPTOR type {kind}, {x['row'].split('(')[1].rstrip(')')}"
        else:
            label = x['row']
        rows.append((label, path))
    out = [header]
    for label, path in rows:
        kind = path.split('.t')[1].split('.')[0] if 'read_descriptor' in path else None
        p8 = path if not kind else next((p for p, _ in PATHS['A8'] if p.startswith(f'aecp.read_descriptor.t{kind}.')),
                                        path)
        out.append(f"| {label} | {cell('A1', path)} | {pair('A8', p8)} | {accesses(path).split(' / ')[0]} / "
                   f"{(worst('A8', p8) or {}).get('pass_mbx_accesses', '-')} |")
    return '\n'.join(out)


def srp_maap() -> str:
    header = '| SRP and MAAP path | 1x1 ms (bound) | 8x8 if0 / if1 ms (bound) | Accesses, 1x1 / 8x8 |\n|---|---:|---:|---:|'
    rows = [('SRP startup declarations (LINK_UP)', 'srp.startup'),
            ('SRP Listener Ready RX (registrar; the fixture grants no licence)', 'srp.listener_ready'),
            ('SRP malformed MRPDU discard', 'srp.malformed'),
            ('SRP Domain RX -> declarations (W = JoinTime 200 ms)', 'srp.domain'),
            ('MAAP first PROBE (LINK_UP)', 'maap.probe1'),
            ('MAAP PROBE retransmission (the worse of two)', 'maap.probe_retransmission'),
            ('MAAP last PROBE retransmission', 'maap.probe4'), ('MAAP ANNOUNCE', 'maap.announce'),
            ('MAAP conflicting PROBE -> DEFEND', 'maap.defend')]
    return table(header, rows)


def backlog() -> str:
    out = ['| Backlog row ([`MAILBOX_SPLIT.md:753-758`](../../../docs/design/MAILBOX_SPLIT.md#acmp-service-latency)) '
           '| Desk bound, accesses IF=1 / IF=2 | A: 1x1 ms (bound) [records ahead] | A: 8x8 | B: 1x1 | B: 8x8 |',
           '|---|---:|---:|---:|---:|---:|']
    desk = {'backlog.event': '10,569 / 13,287', 'backlog.acmp_command': '38,753 / 48,719',
            'backlog.adp_available': '77,506 / 97,438', 'backlog.adp_available_refill': '-',
            'backlog.owed': '31,707 / 39,861'}
    for label, path in (('an event behind 15 others', 'backlog.event'),
                        ('an ACMP command behind a full acmp ring', 'backlog.acmp_command'),
                        ('an ENTITY_AVAILABLE behind the adp ring at its burst (observed)', 'backlog.adp_available'),
                        ('the same, its bucket refilling up to the ring\'s room (observed)',
                         'backlog.adp_available_refill'),
                        ('a response with 7 frames owed ahead of it', 'backlog.owed')):
        cells = [cell(a, path, ahead=True) for a in ('A1', 'A8', 'B1', 'B8')]
        out.append(f"| {label} | {desk[path]} | {' | '.join(cells)} |")
    owed = [f"{worst(a, 'backlog.owed')['from_origin_ms']:.2f}" if worst(a, 'backlog.owed') else '-'
            for a in ('A1', 'A8', 'B1', 'B8')]
    out.append(f"| the same, from the moment the room returns | - | {' | '.join(owed)} |")
    return '\n'.join(out)


def admission() -> str:
    g = GROUPS['A1']['backlog']['passes']['composed']
    out = ['| Channel | Burst | Refill | Ring room, records of the load\'s frame | Offered at once | Bound? |',
           '|---|---:|---:|---:|---:|---|']
    for name, a in g['admission'].items():
        out.append(f"| {name} | {a['burst']} | 1 per {a['refill_ms']} ms | {a['room']} ({a['record_words']} words each) "
                   f"| {a['at_once']} | {'yes: the ring is full' if a['bounded'] else 'no: observed at the burst'} |")
    return '\n'.join(out)


def population() -> str:
    out = ['| Arm, group | Composed population committed (records; events) | Composed maximum, CPU cycles (ms) |',
           '|---|---|---:|']
    for arm in ('A1', 'A8', 'B1', 'B8'):
        for name, g in GROUPS.get(arm, {}).items():
            c = g['passes']['composed']
            if c and name != 'fixture':
                pop = ', '.join(f'{k} {v}' for k, v in c['population'].items() if v)
                out.append(f"| {arm} {name} | {pop} | {c['cycles']:,} ({c['ms']:.2f}) |")
    return '\n'.join(out)


def passes() -> str:
    out = ['| Point, arm | Idle pass, CPU cycles (ms) | Worst pass, CPU cycles (ms), group | Composed maximum, CPU cycles (ms), group |',
           '|---|---:|---:|---:|']
    for arm, label in (('A1', '1x1, A'), ('B1', '1x1, B'), ('A8', '8x8, A'), ('B8', '8x8, B')):
        gs = GROUPS[arm]
        idle = [g['passes']['idle_max'] for g in gs.values() if g['passes']['idle_max']]
        idle_min = [g['passes']['idle_min'] for g in gs.values() if g['passes']['idle_min']]
        w = max(gs.values(), key=lambda g: g['passes']['worst']['cycles'])
        comp = [(g['passes']['composed'], name) for name, g in gs.items() if g['passes']['composed'] and name != 'fixture']
        cm, cname = max(comp, key=lambda c: c[0]['cycles'])
        out.append(f"| {label} | {min(idle_min):,} to {max(idle):,} ({min(idle_min) / 50000:.2f} to "
                   f"{max(idle) / 50000:.2f}) | {w['passes']['worst']['cycles']:,} ({w['passes']['worst']['ms']:.2f}), "
                   f"{w['group']} | {cm['cycles']:,} ({cm['ms']:.2f}), {cname} |")
    return '\n'.join(out)


def counts() -> str:
    out = ['| Arm | Groups | Paths missing T_svc | Probe instances missing T_svc |', '|---|---:|---:|---:|']
    for arm, v in ARMS.items():
        c = v['counts']
        out.append(f"| {arm} | {len(v['results'])} | {c['path_misses']} of {c['paths']} | "
                   f"{c['instance_misses']} of {c['instances']} |")
    return '\n'.join(out)


def modules(arm: str, group: str, key: str = 'worst') -> str:
    w = GROUPS[arm][group]['passes'][key]
    return f"{w['cycles']:,}: " + ', '.join(f"`{k}` {v:,}" for k, v in sorted(w['modules'].items(),
                                                                           key=lambda kv: -kv[1])[:6])


def summaries() -> str:
    """CPI, fetches per instruction and the access costs, over every log of arm A at each point."""
    out = ['| Point | CPU cycles per instruction | Fetches per instruction | Mailbox read / write, CPU cycles | '
           'BRAM fetch, CPU cycles (max) | sram load/store | CSR | Flash window load | '
           'Code fetched, boot / service (largest run) |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for arm, label in (('A1', '1x1'), ('A8', '8x8')):
        cpu = instr = fetch = 0
        stats: dict = {}
        code = (0, 0)
        for path in sorted((F / arm).glob('*.log')):
            text = path.read_text()
            m = re.search(r'^SUMMARY (.*)$', text, re.M)
            if not m:
                continue
            d = dict(kv.split('=', 1) for kv in m.group(1).split())
            cpu += int(d['cpu'])
            instr += int(d['instr'])
            fetch += int(d['fetch_rom'].split('/')[0])
            for k in ('mbx_read', 'mbx_write', 'fetch_rom', 'load_sram', 'store_sram', 'load_csr', 'store_csr',
                      'load_flash'):
                c, tot, mn, mx = (int(v) for v in d[k].split('/'))
                a = stats.setdefault(k, [0, 0, 1 << 60, 0])
                a[0] += c
                a[1] += tot
                a[2] = min(a[2], mn) if c else a[2]
                a[3] = max(a[3], mx)
            c = re.search(r'^CODE boot_bytes=(\d+) service_bytes=(\d+)', text, re.M)
            if c and int(c.group(2)) > code[1]:
                code = (int(c.group(1)), int(c.group(2)))

        def rng(k: str) -> str:
            _, _, mn, mx = stats[k]
            return f'{mn}-{mx}' if mn != mx else f'{mn}'
        out.append(f"| {label} | {cpu / instr:.2f} | {fetch / instr:.2f} | {rng('mbx_read')} / {rng('mbx_write')} | "
                   f"{stats['fetch_rom'][1] / stats['fetch_rom'][0]:.2f} ({stats['fetch_rom'][3]}) | "
                   f"{rng('load_sram')} / {rng('store_sram')} | {rng('load_csr')} / {rng('store_csr')} | "
                   f"{stats['load_flash'][1] / stats['load_flash'][0]:.1f} mean ({rng('load_flash')}) | "
                   f"{code[0]:,} / {code[1]:,} B |")
    return '\n'.join(out)


if __name__ == '__main__':
    for name, fn in (('counts', counts), ('summaries', summaries), ('passes', passes), ('adp', adp), ('acmp', acmp), ('aecp', aecp),
                     ('srp maap', srp_maap), ('backlog', backlog), ('admission', admission),
                     ('population', population)):
        print(f'## {name}\n{fn()}\n')
    for arm in ('A1', 'A8', 'B1', 'B8'):
        for group in GROUPS.get(arm, {}):
            if group.startswith('backlog'):
                print(arm, group, 'composed', modules(arm, group, 'composed'))
        w = max(GROUPS[arm], key=lambda g: GROUPS[arm][g]['passes']['worst']['cycles'])
        print(arm, 'worst', w, modules(arm, w))
