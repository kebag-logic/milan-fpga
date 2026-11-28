"""Recompute the 4x4 point's stated costs from the published census receipts: each cost by the rule
(cycles at the census clock, +5 %, rounded up to 5 us), the merge as the largest of censuses 2, 3 and 4,
and compare with merged234 and with the tables at the reviewed head.
usage: python3 -I costs_check.py EVIDENCE_ROUND3_RECEIPTS CLONE"""
import json, math, sys
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
ev, clone = Path(sys.argv[1]), Path(sys.argv[2])
def rule(cycles, hz):
    us = Decimal(cycles) * Decimal(10**6) / Decimal(hz) * Decimal('1.05')
    return int((us / 5).to_integral_value(ROUND_CEILING) * 5)
bad = 0
cs = {n: json.load(open(ev / f'census{n}-969.json')) for n in (2, 3, 4)}
for n, c in cs.items():
    for k, v in c['costs'].items():
        if isinstance(v, dict) and 'cycles' in v and 'rule_us' in v:
            r = rule(v['cycles'], c['cpu_hz'])
            if r != v['rule_us']:
                bad += 1; print(f'RULE census{n} {k}: cycles {v["cycles"]} -> {r} us, receipt {v["rule_us"]}')
m = json.load(open(ev / 'merged234-969.json'))
mc = m['costs']
for k, v in mc.items():
    if not (isinstance(v, dict) and 'rule_us' in v):
        continue
    got = [cs[n]['costs'][k]['rule_us'] for n in cs if isinstance(cs[n]['costs'].get(k), dict) and 'rule_us' in cs[n]['costs'][k]]
    if got and max(got) != v['rule_us']:
        bad += 1; print(f'MERGE {k}: max of censuses {got} = {max(got)}, merged {v["rule_us"]}')
print('checked keys', len(mc))
d = json.load(open(ev / 'derive-merged234-969.json'))['costs']
sys.path.insert(0, str(clone / 'tb/verilator/ctrl_service_budget'))
import load_grade, poll_grade, rows_tiers, rows_grade, edit_rows, shape_costs
S = shape_costs.Shape(1, 5, 5)
tab = {}
tab.update({k: v for k, v in load_grade.STATED_US['arty-4x4'].items()})
pg = poll_grade.STATED_US[S]
for a, b in (('base', 'base'), ('withdraw', 'item.withdraw'), ('rebuild', 'item.rebuild'), ('walk', 'item.walk'),
             ('reclaim', 'item.reclaim'), ('retained', 'item.retained'), ('acmp', 'item.acmp'), ('aecp', 'item.aecp'),
             ('aecp_long', 'item.aecp_long'), ('acmp_declined', 'item.acmp_declined')):
    tab[b] = pg[a]
for k, v in rows_tiers.DATAPATH_US['arty-4x4'].items():
    tab['event.' + k] = v
tab['record.aecp.long'] = rows_tiers.LONG_RECORD_US['arty-4x4']
tab['event.LINK'] = rows_grade.ROW_COSTS['arty-4x4']['event.LINK']
tab['paced.45'] = edit_rows.PACED['arty-4x4']['a one-row edit']
tab['paced.6'] = edit_rows.PACED['arty-4x4']['an accepted SET_CONFIGURATION']
h = shape_costs.at(S, clone)
for a, b in (('CTRL_LOOP_BUILD_PASS_US', 'build'), ('CTRL_LOOP_BUILD_ONE_PASS_US', 'build_one'),
             ('CTRL_LOOP_SRP_UNIT_US', 'item.record'), ('CTRL_LOOP_STEP_PASS_US', 'step'),
             ('CTRL_LOOP_TICK_US', 'centisecond')):
    tab['h:' + b] = h[a]
for k, v in sorted(tab.items()):
    key = k[2:] if k.startswith('h:') else k
    if key not in d:
        print(f'NOKEY {k} = {v}'); continue
    if d[key] != v:
        bad += 1; print(f'TABLE {k}: head {v}, derivation {d[key]}')
print('compared', len(tab), 'head statements with the derivation; header row:', {k: h[k] for k in sorted(h)})
print('RESULT', 'PASS' if bad == 0 else f'FAIL {bad}')
sys.exit(1 if bad else 0)
