#!/usr/bin/env python3
"""Recompute every numeric table in docs/findings/397_SERVICE_BUDGET.md from receipts.

usage: check_tables_r2.py <repo> <receipt-dir>
Receipts are round2-<1x1|8x8>-<plan>.json. Prints each mismatch; exit 1 on any.
"""
import json, re, sys
from pathlib import Path

repo, rdir = Path(sys.argv[1]), Path(sys.argv[2])
PLANS = ('all', 'uart-paced', 'queued-input', 'device-wait')
GROUPS = [
    ('Boot to entity enabled', lambda d: d == 'boot_to_entity_enabled'),
    ('AEM copy/CRC', lambda d: d == 'aem_copy_crc'),
    ('Binding restore walk', lambda d: d == 'restore_walk'),
    ('Journal erase envelope', lambda d: d == 'erase_enclosed_to_first_program'),
    ('Journal START-to-ACK', lambda d: d == 'journal_commit_bracket'),
    ('`milan_status`', lambda d: d == 'milan_status'),
    ('`milan_gettime`', lambda d: d == 'milan_gettime'),
    ('`milan_settime`, maximum tested case', lambda d: d.startswith('milan_settime')),
    ('`milan_utc`, maximum tested case', lambda d: d.startswith('milan_utc')),
    ('`milan_nvm` status', lambda d: d == 'milan_nvm'),
    ('`milan_nvm commit`', lambda d: d == 'milan_nvm commit'),
    ('`milan_nvm wipe`, whole command', lambda d: d == 'milan_nvm wipe'),
    ('Wipe erase envelope, maximum of two', lambda d: d == 'wipe_erase_envelope'),
    ('`milan_nvm invalid`', lambda d: d == 'milan_nvm invalid'),
]
rec = {(k, p): json.loads((rdir / f'round2-{k}-{p}.json').read_text()) for k in ('1x1', '8x8') for p in PLANS}
text = (repo / 'docs/findings/397_SERVICE_BUDGET.md').read_text()

def tables():
    out, cur = [], None
    for line in text.splitlines():
        if line.startswith('| ') and not line.startswith('| ---'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if cur is None: cur = [cells]; out.append(cur)
            else: cur.append(cells)
        elif not line.startswith('| ---'):
            cur = None
    return out

T = tables()
bad = 0
def eq(label, got, want):
    global bad
    if str(got) != str(want):
        bad += 1; print(f'MISMATCH {label}: page {want!r} receipts {got!r}')
def f5(x): return f'{x:.5f}'
def num(x): return f'{x:,}'

duty_tabs = [t for t in T if t[0][:2] == ['Duty', 'Plan at maximum']]
opp_tabs = [t for t in T if t[0][:2] == ['Duty', 'Longest no-tick span ms']]
assert len(duty_tabs) == 2 and len(opp_tabs) == 2
checked = 0
for k, dt, ot in zip(('1x1', '8x8'), duty_tabs, opp_tabs):
    dmap = {r[0]: r for r in dt[1:]}; omap = {r[0]: r for r in ot[1:]}
    assert list(dmap) == [g for g, _ in GROUPS] == list(omap), (list(dmap), list(omap))
    for name, sel in GROUPS:
        rows = [(p, r) for p in PLANS for r in rec[(k, p)]['rows'] if sel(r['duty'])]
        # duty table: max elapsed ms, first plan in PLANS order on ties
        p, r = max(rows, key=lambda pr: pr[1]['sys_cycles'])
        ties = sorted({pp for pp, rr in rows if rr['sys_cycles'] == r['sys_cycles']})
        row = dmap[name]
        if row[1].strip('`') not in ties: eq(f'{k} {name} plan', ties, row[1])
        eq(f'{k} {name} cpu', num(r['cpu_cycles']), row[2]); eq(f'{k} {name} ms', f5(r['ms']), row[3])
        b = r['budget_ms']
        eq(f'{k} {name} budget', 'N/A' if b is None else num(b), row[4])
        eq(f'{k} {name} margin', 'N/A' if b is None else f5(b - r['ms']), row[5])
        # opportunity table
        p2, r2 = max(rows, key=lambda pr: pr[1]['no_tick_sys_cycles'])
        ties2 = sorted({pp for pp, rr in rows if rr['no_tick_sys_cycles'] == r2['no_tick_sys_cycles']})
        tx = max(rr['uart_tx_allowance_ms'] for _, rr in rows)
        o = omap[name]
        eq(f'{k} {name} no-tick', f5(r2['no_tick_ms']), o[1])
        if o[2].strip('`') not in ties2: eq(f'{k} {name} no-tick plan', ties2, o[2])
        eq(f'{k} {name} tx', f5(tx), o[3])
        if name.startswith('Boot'):
            eq(f'{k} boot bound', 'Unarmed prefix', o[4])
        else:
            bound = 250 + r2['no_tick_ms'] + tx
            eq(f'{k} {name} bound', f5(bound), o[4]); eq(f'{k} {name} m500', f5(500 - bound), o[5])
            eq(f'{k} {name} m2000', f5(2000 - bound), o[6])
        checked += 1
sched = [t for t in T if t[0][0] == 'Shape / plan'][0]
for row in sched[1:]:
    k, p = [x.strip().strip('`') for x in row[0].split('/')]
    d = rec[(k, p)]; h = d['heartbeat']; g = [r for r in d['rows'] if r['duty'] == 'maximum_heartbeat_gap'][0]
    eq(f'{k}/{p} gap', f5(g['ms']), row[1]); eq(f'{k}/{p} m500', f5(500 - g['ms']), row[2])
    eq(f'{k}/{p} m2000', f5(2000 - g['ms']), row[3])
    eq(f'{k}/{p} ends', f"{f5(h['start_sys_cycle']/100000)} to {f5(h['end_sys_cycle']/100000)}", row[4])
    eq(f'{k}/{p} tail', 'Yes' if h['right_censored'] else 'No', row[5])
    eq(f'{k}/{p} backed', ', '.join(str(x['backed']) for x in d['liveness']), row[6])
    eq(f'{k}/{p} plan', p, h['plan']); checked += 1
dev = [t for t in T if t[0][0] == 'Shape / device-max duty'][0]
names = {'Erase envelope': 'erase_enclosed_to_first_program', 'Journal START-to-ACK': 'journal_commit_bracket',
         'Whole console commit': 'milan_nvm commit'}
for row in dev[1:]:
    k, n = [x.strip() for x in row[0].split('/')]
    r = [r for r in rec[(k, 'device-wait')]['rows'] if r['duty'] == names[n]]
    assert len(r) == 1; r = r[0]
    eq(f'dev {k} {n} cpu', num(r['cpu_cycles']), row[1]); eq(f'dev {k} {n} svc', f5(r['service_ms']), row[2])
    wip = r['device_wait_ms']; eq(f'dev {k} {n} wip', f'{wip:g}', row[3])
    eq(f'dev {k} {n} ms', f5(r['ms']), row[4]); eq(f'dev {k} {n} margin', f5(r['budget_ms'] - r['ms']), row[6])
    checked += 1
for (k, p), d in rec.items():
    import hashlib
    eq(f'{k}/{p} log digest', hashlib.sha256(d['raw_log'].encode()).hexdigest(), d['log_sha256'])
    eq(f'{k}/{p} plan/shape', (d['media']['plan'], d['media'].get('shape', d['shape'])), (p, d['shape']))
print(f'rows checked {checked}; mismatches {bad}')
sys.exit(1 if bad else 0)
