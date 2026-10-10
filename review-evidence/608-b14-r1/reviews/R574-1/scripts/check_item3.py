#!/usr/bin/env python3
"""Recompute item 3 figures of docs/findings/B14_BENCH_5603C353.md from the
published packet (author/item3) and compare them with the page's table.
usage: check_item3.py <packet-author-dir> <findings-page>"""
import json, os, re, statistics, sys
A, PAGE = sys.argv[1], sys.argv[2]
cyc = os.path.join(A, 'item3', 'cycles')
names = sorted(d for d in os.listdir(cyc) if d.startswith('cycle-'))
rows = {}
la = {'DUT': set(), 'bridge': set()}
ta_lv = {}
cap = 0.0
own_la_before_lv = 0
for n in names:
    an = json.load(open(os.path.join(cyc, n, 'analysis.json')))
    res = json.load(open(os.path.join(cyc, n, 'result.json')))
    rows[n] = (an, res)
    cap += an['capture_span_s']
    ev = [l.rstrip('\n').split('\t') for l in open(os.path.join(cyc, n, 'msrp.tsv'))][1:]
    disc = an['disconnect_response_s']; conn = an['connect_command_s']
    tgt = res['stream_id']
    blv = [float(e[0]) for e in ev if e[1] == 'bridge' and e[2] == 'Listener' and e[3] == 'Lv' and e[4] == tgt]
    blv_hold = [t for t in blv if disc <= t <= conn]
    for e in ev:
        if e[3] == 'LeaveAll':
            la[e[1]].add((n, e[0]))
    if blv_hold:
        t0 = blv_hold[0]
        if any(e[3] == 'LeaveAll' and disc - 10 <= float(e[0]) < t0 for e in ev):
            own_la_before_lv += 1
        d = [float(e[0]) - t0 for e in ev if e[1] == 'DUT' and e[2] == 'TalkerAdvertise' and e[3] == 'Lv' and e[4] == tgt and disc <= float(e[0]) <= conn]
        if d:
            ta_lv[n] = d[0]
        # check analysis lv_after_disconnect
        assert abs((t0 - disc) - an['bridge_lv_after_disconnect_s']) < 1e-6, n
print('cycles', len(names), 'capture_s_total %.3f' % cap)
g = [n for n in names if n != 'cycle-001']
cap_g = sum(rows[n][0]['capture_span_s'] for n in g)
print('capture_s graded %.3f' % cap_g)
print('LeaveAll MRPDUs (distinct timestamps) by sender:', {k: len(v) for k, v in la.items()})
print('LeaveAll MRPDUs graded only:', {k: len([x for x in v if x[0] != 'cycle-001']) for k, v in la.items()})
print('cycles with any LeaveAll in the 10 s before the first in-hold bridge Lv:', own_la_before_lv)
print('DUT TA Lv after bridge Lv (s):', {k: round(v, 4) for k, v in ta_lv.items()})
def st(xs): return (min(xs), statistics.median(xs), max(xs))
lv = [rows[n][0]['bridge_lv_after_disconnect_s'] * 1e3 for n in g]
lp = [rows[n][0]['last_pdu_after_lv_s'] * 1e3 for n in g]
rs = [rows[n][0]['restart_s'] * 1e3 for n in g]
print('Lv after resp ms min/med/max', st(lv)); print('last PDU - Lv ms', st(lp)); print('restart ms', st(rs))
print('late Lv cycles (>20 ms):', [(n, round(rows[n][0]['bridge_lv_after_disconnect_s']*1e3, 1)) for n in g if rows[n][0]['bridge_lv_after_disconnect_s'] > 0.02])
print('stop PASS', sum(rows[n][0]['stop_608'] == 'PASS' for n in g), 'start/stop +1/+1', sum(rows[n][0]['dut_out1_start_stop_delta'] == [1, 1] for n in g),
      'pdus_after', sum(rows[n][0]['pdus_after_lv_plus_period'] for n in g), 'malformed', sum(len(rows[n][0]['msrp_malformed']) for n in g),
      'reversals', sum(rows[n][0]['reversals'] for n in g), 'capture_rc!=0', [n for n in g if rows[n][1]['capture_rc'] != 0])
print('restarts sorted top4', sorted(((round(rows[n][0]['restart_s']*1e3, 1), n) for n in g), reverse=True)[:4])
# page table
tab = {}
for l in open(PAGE):
    m = re.match(r'^\| (\d{3})(?: \(pilot\))? \| ([\d.]+) \| (-?[\d.]+) \| (\d+) \| \+(\d) / \+(\d) \| ([\d.]+) \| (\w+) \|$', l.strip())
    if m: tab['cycle-' + m.group(1)] = m.groups()
mis = []
for n in names:
    an = rows[n][0]; t = tab.get(n)
    if not t: mis.append((n, 'missing')); continue
    exp = ('%.3f' % (an['bridge_lv_after_disconnect_s'] * 1e3), '%.3f' % (an['last_pdu_after_lv_s'] * 1e3), str(an['pdus_after_lv_plus_period']),
           str(an['dut_out1_start_stop_delta'][0]), str(an['dut_out1_start_stop_delta'][1]), '%.1f' % (an['restart_s'] * 1e3), an['stop_608'])
    if tuple(t[1:]) != exp: mis.append((n, t[1:], exp))
print('page rows', len(tab), 'mismatches', mis)
