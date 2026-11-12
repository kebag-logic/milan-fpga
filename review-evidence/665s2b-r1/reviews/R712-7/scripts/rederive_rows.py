"""Independent re-derivation of R4, R5 and R6 at 1x1/1if (and 8x8/2if for reference) from ctrl_loop.h's drain as
built and the stated costs. Stated costs come from the tree's own tables (load_grade.stated at the pin, the polls'
poll_grade.stated_us, rows_grade.ROW_COSTS for LINK); every count below is written here, not imported.
usage: python3 -I rederive_rows.py <repo-root>"""
import math, re, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import load_grade, poll_grade, rows_grade, yaml

def consts(n_if):
    # read by hand from the headers at this head (verified by grep in the report): ctrl_loop.h, aecp.h, aecp_mbx.h
    one = n_if == 1
    return dict(DRAIN_US=1300, CAP=2, TICK_CAP=1, STEP_AGE=2, STEP_US=975 if one else 1030,
                BUILD=900 if one else 1995, BUILD_ONE=405 if one else 1215, SHARE=2000, MARGIN=65, TICK_US=430,
                NOTICE=255 if one else 365, COLD=85 if one else 165, PACE=2, YPACE=4, YN=1, YIELDS=3 * (n_if - 1),
                FIRM=12 if one else 4, MOST=12 if one else 40)

def inputs(point):
    s = dict(load_grade.POINTS[point]); k = consts(s['n_if'])
    c = load_grade.stated(root, point, load_grade.STATED_US)
    p = poll_grade.stated_us(s['n_if'])
    c.update({'item.withdraw': p['withdraw'], 'item.rebuild': p['rebuild'], 'item.aecp': p['aecp']})
    c['item.retained'] = max(c['item.retained'], c['record.srp']); c.update(rows_grade.ROW_COSTS[point])
    y = yaml.safe_load((root / 'sw/mailbox/mailbox.yaml').read_text())
    rate = {ch['name']: (ch['rate']['burst'], ch['rate']['refill_ms']) for ch in y['channels']}
    return s, k, c, rate, y['tick_ms']

def rounds(k, w, extra=0):
    per = max(1, min(k['FIRM'], (k['SHARE'] - k['MARGIN'] - k['COLD']) // k['NOTICE']))
    left, t, us = k['MOST'] + extra, 0.0, 0.0
    for _ in range(k['YIELDS']):
        if t > w or left <= 0: break
        b = min(left, k['YN']); us += k['COLD'] + b * k['NOTICE']; left -= b; t += k['YPACE']
    while t <= w and left > 0:
        b = min(left, per); us += k['COLD'] + b * k['NOTICE']; left -= b; t += k['PACE']
    return us

def demand(row, point, w, v):
    s, k, c, rate, tick = inputs(point); n_if, cap = s['n_if'], k['CAP']
    arrive = lambda ch: rate[ch][0] + math.floor(w / rate[ch][1])
    d = {}
    ticks = math.floor(w / tick) + 1
    d['ticks'] = ticks * (c['event.TICK'] + max(c['centisecond'], k['TICK_US']))
    if row == 'R4':
        d['own'] = rate['aecp'][0] * c['record.aecp']
        srp_window = w - d['own'] / 1000 if v['srp_minus_own'] else w
        d['srp'] = (rate['srp'][0] + math.floor(max(0.0, srp_window) / rate['srp'][1])) * c['record.srp']
    else:
        d['srp'] = rate['srp'][0] * c['record.srp']
    both, one = n_if * k['BUILD'], 2 * n_if * k['BUILD_ONE']
    d['builds'], nb = (both, n_if) if both >= one else (one, 2 * n_if)
    held = (n_if + 1) if row == 'R5' else 0
    passes = 1
    for _ in range(80):
        adp = min(passes, 2 + math.floor(w / rate['adp'][1]) + s['sinks_per_if'])
        tm = n_if * (min(passes, adp) * c['event.ADP'] + min(passes, s['sinks_per_if']) * c['event.ACMP'] +
                     min(passes, 1) * c['event.MAAP']) + \
            min(passes, s['registrations'] * n_if + s['counter_descriptors'] + 2) * c['event.AECP']
        ev = d['ticks'] + tm
        drained = math.ceil((d['srp'] + ev) / k['DRAIN_US'])
        n = (math.ceil(rate['aecp'][0] / cap) + ticks + 1 + drained) if row == 'R4' else (1 + drained + held)
        if n == passes: break
        passes = n
    d['timers'] = tm
    if row == 'R4':
        d['others'] = sum(min(arrive(o), passes * cap) * c[f'record.{o}'] for o in ('acmp', 'adp', 'maap'))
    else:
        light = math.floor(ev / max(1, k['DRAIN_US'] - cap * c['record.srp'])) + held
        d['others'] = sum(min(arrive(o), light * cap) * c[f'record.{o}'] for o in ('aecp', 'acmp', 'adp', 'maap'))
    d['gm'] = n_if * min(passes, sum(math.floor(w / ms) + 1 for ms in (1000, 1000, 3000))) * c['event.GM']
    d['steps'] = (math.floor(w / (10 * (k['STEP_AGE'] + 1))) + 1) * k['STEP_US']
    srp_in = arrive('srp')
    d['item.walk'] = min(passes * n_if, n_if * (ticks + nb)) * c['item.walk']
    d['item.reclaim'] = min(2 * n_if * passes, 2 * (srp_in + nb)) * c['item.reclaim']
    retries = min(passes, srp_in) if v['retained_per_pass'] else min(passes, ticks, srp_in)
    d['item.retained'] = retries * c['item.retained']
    d['item.mrpdu'] = min(passes, 2 * nb) * c['item.mrpdu']
    d['item.acmp'] = min(passes, arrive('acmp') + arrive('adp') + n_if * s['sinks_per_if']) * c['item.acmp']
    ahead = arrive('aecp') if (v['aecp_items_all'] or row != 'R4') else rate['aecp'][0]
    d['item.aecp'] = min(passes, ahead + n_if * s['registrations']) * c['item.aecp']
    if row == 'R5':
        d['item.withdraw'] = n_if * c['item.withdraw']; d['item.rebuild'] = n_if * c['item.rebuild']
        d['links'] = n_if * c['event.LINK']
    d['passes'] = passes * (c['events_none'] + c['base'])
    extra = (rate['aecp'][0] - 1) if (v.get('notices_from_ahead') and row == 'R4') else 0
    d['rounds'] = rounds(k, w, extra)
    d['_passes'] = passes * 1000.0
    return d

def solve(row, point, v):
    w = 0.01
    while w < 2000:
        d = demand(row, point, w, v); tot = sum(x for kk, x in d.items() if not kk.startswith('_')) / 1000
        if tot <= w: return round(w, 2), d
        w = max(w + 0.01, math.ceil(tot * 100) / 100)
    return None, d

MODEL = dict(srp_minus_own=True, retained_per_pass=True, aecp_items_all=True)
VARIANTS = [('V0 the model as stated (rows_grade.py), re-implemented', MODEL),
            ('V1 SRP arrivals over the whole window', {**MODEL, 'srp_minus_own': False}),
            ('V2 V1 + retained retries at one a centisecond (srp_mbx.c tick/retry_spent)',
             {**MODEL, 'srp_minus_own': False, 'retained_per_pass': False}),
            ('V3 V2 + AECP owed frames only from the records ahead of the row and the probes',
             {**MODEL, 'srp_minus_own': False, 'retained_per_pass': False, 'aecp_items_all': False}),
            ('V4 V3 + the 15 records ahead each queueing a notice THE RETRY sends (sensitivity)',
             {**MODEL, 'srp_minus_own': False, 'retained_per_pass': False, 'aecp_items_all': False,
              'notices_from_ahead': True})]
for point in ('1x1/1if', '8x8/2if'):
    print(f'== {point}')
    tool = rows_grade.rows(root, point)
    print('   rows_grade.py:', {r: tool[r][0] for r in ('R4', 'R5', 'R6')})
    for name, v in VARIANTS:
        out = {}
        for row in ('R4', 'R5', 'R6'):
            w, d = solve(row, point, v); out[row] = w
            if point == '1x1/1if' and row == 'R4':
                terms = ', '.join(f'{kk} {x/1000:.2f}' for kk, x in sorted(d.items(), key=lambda t: -t[1])
                                  if not kk.startswith('_'))
                print(f'   {name}: R4 {w} ms, passes {int(d["_passes"]/1000)}: {terms}')
        print(f'   {name}: R4 {out["R4"]}  R5 {out["R5"]}  R6 {out["R6"]}')
