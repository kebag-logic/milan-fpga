#!/usr/bin/env python3
"""Reviewer-owned recomputation of round-2 duty, opportunity and schedule tables.

Usage: independent_r2.py <receipt-or-result.json>... (one per shape/plan)
Uses no harness code. Parses EVENT lines, re-derives every duty interval, the
longest no-tick span (from the compressed tick blocks), the containing command's
TX allowance, heartbeat-strobe gaps and printed backing samples, then prints
per-shape maxima over plans in the findings-page layout. ms = sys/100,000;
CPU cycles = ceil(sys/2).
"""
import json, re, sys
from collections import defaultdict

def events(raw):
    out = []
    for m in re.finditer(r'^EVENT cycle=(\d+) kind=(\w+)(.*)$', raw, re.M):
        e = {k: int(v) for k, v in re.findall(r'(\w+)=(\d+)', m[3])}
        e.update(kind=m[2], cycle=int(m[1]))
        out.append(e)
    return out

def nospan(ev, a, b):
    blocks = [e for e in ev if e['kind'] == 'ticks' and e['last'] >= a and e['first'] <= b]
    best, prev = (a, a), a
    def upd(x, y):
        nonlocal best
        if y - x > best[1] - best[0]: best = (x, y)
    for t in blocks:
        assert a <= t['first'] and t['last'] <= b, 'block straddles'
        upd(prev, t['first'])
        if t['count'] > 1: upd(t['gap_start'], t['gap_start'] + t['max_gap'])
        prev = t['last']
    upd(prev, b)
    return best[1] - best[0], sum(t['count'] for t in blocks)

def analyse(rec):
    raw = rec['raw_log'] if 'raw_log' in rec else open(rec['_log']).read()
    ev = events(raw)
    W = [e for e in ev if e['kind'] == 'write']
    st = [e for e in ev if e['kind'] == 'command_start']
    nd = [e for e in ev if e['kind'] == 'command_end']
    cmds = rec['_cmds']
    duties = []  # (group, start, end, wait, tx_owner_index)
    def owner(a, b):
        for i, (s, e) in enumerate(zip(st, nd)):
            if s['cycle'] <= a and b <= e['cycle']: return e['tx_bytes'] - s['tx_bytes']
        return 0
    en = next(e for e in W if e['address'] == 0x920 and e['value'] & 1)
    ws = next(e for e in W if e['address'] == 0x920 and e['value'] & 2)
    we = next(e for e in W if e['address'] == 0x920 and not e['value'] & 2 and e['cycle'] > ws['cycle'])
    aem = next(e for e in ev if e['kind'] == 'aem_read')
    duties += [('Boot to entity enabled', 64, en['cycle']), ('AEM copy/CRC', aem['cycle'], en['cycle']),
               ('Binding restore walk', ws['cycle'], we['cycle'])]
    for i, (s, e) in enumerate(zip(st, nd)):
        c = cmds[i]
        g = {'milan_nvm': '`milan_nvm` status', 'milan_nvm commit': '`milan_nvm commit`',
             'milan_nvm wipe': '`milan_nvm wipe`, whole command', 'milan_nvm invalid': '`milan_nvm invalid`',
             'milan_status': '`milan_status`', 'milan_gettime': '`milan_gettime`'}.get(c)
        if g is None:
            g = '`milan_settime`, maximum tested case' if c.startswith('milan_settime') else '`milan_utc`, maximum tested case'
        duties.append((g, s['cycle'], e['cycle']))
        if c == 'milan_nvm wipe':
            er = [x for x in ev if x['kind'] == 'flash' and x['opcode'] == 0xd8 and s['cycle'] <= x['cycle'] <= e['cycle']]
            duties += [('Wipe erase envelope, maximum of two', er[0]['cycle'], er[1]['cycle']),
                       ('Wipe erase envelope, maximum of two', er[1]['cycle'], e['cycle'])]
    cs = [e for e in W if e['address'] == 0x93c and e['value'] == 4]
    ak = [e for e in W if e['address'] == 0x93c and e['value'] & 2]
    for a, b in zip(cs, ak):
        fl = [x for x in ev if x['kind'] == 'flash' and a['cycle'] <= x['cycle'] <= b['cycle']]
        er = next(x for x in fl if x['opcode'] == 0xd8); pg = next(x for x in fl if x['opcode'] == 2)
        duties += [('Journal START-to-ACK', a['cycle'], b['cycle']), ('Journal erase envelope', er['cycle'], pg['cycle'])]
    out = []
    for g, a, b in duties:
        span, calls = nospan(ev, a, b)
        out.append(dict(group=g, sys=b - a, span=span, tx=owner(a, b), calls=calls))
    hb = [e['cycle'] for e in W if e['address'] == 0x93c and e['value'] == 1]
    last = nd[-1]['cycle']
    ga, gb = max(zip(hb, hb[1:] + [last]), key=lambda p: p[1] - p[0])
    chunks = re.split(r'^EVENT cycle=\d+ kind=command_start index=\d+.*$', raw, flags=re.M)[1:]
    samples = []
    for ch in chunks:
        t = re.sub(r'\nEVENT [^\n]*\n', '', ch)
        m = re.search(r'backed=([01])', t); p = re.search(r'PP_STAT=([0-9a-fA-F]{8})', t)
        if m: samples.append(int(m[1]))
        elif p: samples.append((int(p[1], 16) >> 6) & 1)
    return out, (ga, gb, gb == last), samples, len(hb)

ORDER = ['Boot to entity enabled', 'AEM copy/CRC', 'Binding restore walk', 'Journal erase envelope',
         'Journal START-to-ACK', '`milan_status`', '`milan_gettime`', '`milan_settime`, maximum tested case',
         '`milan_utc`, maximum tested case', '`milan_nvm` status', '`milan_nvm commit`',
         '`milan_nvm wipe`, whole command', 'Wipe erase envelope, maximum of two', '`milan_nvm invalid`']
PLAN_CMDS = None
def plan_cmds(plan, shape):
    all_ = ['milan_status', 'milan_gettime', 'milan_nvm', 'milan_nvm commit', 'milan_nvm commit', 'milan_nvm',
            'milan_nvm wipe', 'milan_nvm', 'milan_nvm invalid', 'milan_settime 0 0',
            'milan_settime 18446744073 709551615', 'milan_settime 18446744073 709551616', 'milan_settime invalid',
            'milan_utc 0 0 37', 'milan_utc 18446744073709551615 0 1', 'milan_utc invalid 0 0', 'milan_status']
    if plan == 'queued-input': return ['milan_nvm'] * (3 if '8x8' in shape else 12) + ['milan_status']
    if plan == 'device-wait': return ['milan_nvm commit', 'milan_status']
    return all_

per = defaultdict(lambda: defaultdict(list))
sched = []
for path in sys.argv[1:]:
    rec = json.load(open(path))
    shape = rec.get('shape') or rec['media']['shape']; plan = rec.get('plan') or rec['media'].get('plan', 'all')
    rec['_cmds'] = plan_cmds(plan, shape)
    if 'raw_log' not in rec: rec['_log'] = path.rsplit('/', 1)[0] + '/raw.log'
    rows, (ga, gb, tail), samples, nhb = analyse(rec)
    for r in rows: per[shape][r['group']].append((r, plan))
    sched.append((shape, plan, ga, gb, tail, samples, nhb))
f5 = lambda c: f'{c / 100_000:.5f}'
for shape in sorted(per):
    print(f'\n## {shape} duties: group | plan@max | CPU cycles | ms | span ms | plan@span | max TX ms | conditional ms')
    for g in ORDER:
        if g not in per[shape]: continue
        L = per[shape][g]
        r, p = max(L, key=lambda x: x[0]['sys'])
        rs, ps = max(L, key=lambda x: x[0]['span'])
        tx = max(x[0]['tx'] for x in L) * 10_000 / 115200
        cond = 250 + rs['span'] / 100_000 + tx
        print(f"{g} | {p} | {(r['sys'] + 1) // 2:,} | {f5(r['sys'])} | {f5(rs['span'])} | {ps} | {tx:.5f} | {cond:.5f}")
print('\n## schedules: shape | plan | gap ms | start ms | end ms | tail | samples | strobes')
for shape, plan, ga, gb, tail, samples, nhb in sorted(sched):
    print(f'{shape} | {plan} | {f5(gb - ga)} | {f5(ga)} | {f5(gb)} | {tail} | {samples} | {nhb}')
