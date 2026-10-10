#!/usr/bin/env python3
"""Recompute item 3 (withdrawals) from per-cycle msrp.tsv, acmp.tsv, snapshots and analysis.json,
and compare with the table in the findings page."""
import json, sys, os, re, statistics, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from counters_lib import decode
pk, doc = sys.argv[1], sys.argv[2]
base = pk + '/author/item3/cycles'
SID = '0200000000010001'
rows = {}
for l in open(doc):
    m = re.match(r'^\| (\d{3})(?: \(pilot\))? \| ([\d.]+) \| (-?[\d.]+) \| (\d+) \| \+(\d) / \+(\d) \| ([\d.]+) \| (\w+) \|$', l.strip())
    if m:
        rows[int(m.group(1))] = m.groups()[1:]
print('doc table rows', len(rows))
def tsv(p):
    with open(p) as f:
        return list(csv.DictReader(f, delimiter='\t'))
def snapctr(p, what):
    for l in open(p):
        e = json.loads(l)
        if e['what'] == what:
            return decode(e['response']['payload'])[3]
agg = dict(lv=[], last=[], restart=[], la_bridge=0, la_dut=0, span=0.0, msrp_by={}, mism=[], prof={}, ta_lv=[], la_before_lv=[], startstop={})
for c in range(1, 102):
    d = '%s/cycle-%03d' % (base, c)
    a = json.load(open(d + '/analysis.json'))
    r = json.load(open(d + '/result.json'))
    ms = tsv(d + '/msrp.tsv'); ac = tsv(d + '/acmp.tsv')
    disc = [float(x['t_s']) for x in ac if x['mt'] == '9']
    conn = [float(x['t_s']) for x in ac if x['mt'] == '6']
    assert len(disc) == 1 and len(conn) == 1, (c, disc, conn)
    disc, conn = disc[0], conn[0]
    lvs = [float(x['t_s']) for x in ms if x['sender'] == 'bridge' and x['type'] == 'Listener' and x['event'] == 'Lv' and x['stream_id'] == SID and float(x['t_s']) >= disc]
    lv = lvs[0]
    lv_after = lv - disc
    pdus = {}
    for x in ms:
        pdus.setdefault((x['sender'], x['t_s']), []).append(x)
    la = {}
    for (snd, t), evs in pdus.items():
        if any(e['event'] == 'LeaveAll' for e in evs):
            la.setdefault(snd, []).append(float(t))
    la_before = [(s, t) for s, ts in la.items() for t in ts if t < lv]
    hold = sorted({(x['sender'], x['type'], x['event']) for x in ms if disc <= float(x['t_s']) < conn})
    ta_lv = [float(x['t_s']) - lv for x in ms if x['sender'] == 'DUT' and x['type'] == 'TalkerAdvertise' and x['event'] == 'Lv' and x['stream_id'] == SID and disc <= float(x['t_s']) < conn]
    la_after_in_hold = [t - lv for t in la.get('bridge', []) if disc <= t < conn]
    before = snapctr(d + '/snapshot-before.jsonl', 'counter-6-1'); after = snapctr(d + '/snapshot-after.jsonl', 'counter-6-1')
    ss = (after['STREAM_START'] - before['STREAM_START'], after['STREAM_STOP'] - before['STREAM_STOP'])
    if c >= 2:
        agg['lv'].append(lv_after); agg['last'].append(a['last_pdu_after_lv_s']); agg['restart'].append(r['latency_s'])
        agg['la_bridge'] += len(la.get('bridge', [])); agg['la_dut'] += len(la.get('DUT', []))
        agg['span'] += a['capture_span_s']
        agg['prof'].setdefault(tuple(hold), []).append(c)
        agg['startstop'][ss] = agg['startstop'].get(ss, 0) + 1
        if ta_lv: agg['ta_lv'].append((c, [round(x, 4) for x in ta_lv], round(min(t for t in [float(x['t_s']) for x in ms if x['sender'] == 'DUT' and x['type'] == 'TalkerAdvertise' and x['event'] == 'Lv' and x['stream_id'] == SID and disc <= float(x['t_s']) < conn]) - disc, 4)))
        if la_before: agg['la_before_lv'].append((c, [(s, round(t - lv, 3)) for s, t in la_before]))
        if la_after_in_hold and min(la_after_in_hold) < 0: agg['mism'].append(('bridge LeaveAll in hold before Lv', c))
    # compare to analysis.json and doc
    if abs(lv_after - a['bridge_lv_after_disconnect_s']) > 1e-6: agg['mism'].append(('lv vs analysis', c, lv_after, a['bridge_lv_after_disconnect_s']))
    dr = rows.get(c)
    if not dr: agg['mism'].append(('no doc row', c)); continue
    if abs(float(dr[0]) - lv_after * 1e3) > 0.0006: agg['mism'].append(('doc lv', c, dr[0], lv_after * 1e3))
    if abs(float(dr[1]) - a['last_pdu_after_lv_s'] * 1e3) > 0.0006: agg['mism'].append(('doc last', c, dr[1], a['last_pdu_after_lv_s'] * 1e3))
    if int(dr[2]) != a['pdus_after_lv_plus_period']: agg['mism'].append(('doc pdus after', c))
    if (int(dr[3]), int(dr[4])) != ss: agg['mism'].append(('doc start/stop', c, dr[3:5], ss))
    if abs(float(dr[5]) - r['latency_s'] * 1e3) > 0.06: agg['mism'].append(('doc restart', c, dr[5], r['latency_s'] * 1e3))
    if dr[6] != a['stop_608']: agg['mism'].append(('doc stop', c))
print('graded n', len(agg['lv']))
print('lv after response ms min/median/max', round(min(agg['lv']) * 1e3, 3), round(statistics.median(agg['lv']) * 1e3, 3), round(max(agg['lv']) * 1e3, 3))
print('lv > 20 ms', [(c, round(v * 1e3, 1)) for c, v in zip(range(2, 102), agg['lv']) if v > 0.02])
print('last PDU minus Lv ms min/max', round(min(agg['last']) * 1e3, 3), round(max(agg['last']) * 1e3, 3))
print('restart ms min/median/max', round(min(agg['restart']) * 1e3, 1), round(statistics.median(agg['restart']) * 1e3, 2), round(max(agg['restart']) * 1e3, 1))
print('sorted restarts top 4', sorted(round(x * 1e3, 1) for x in agg['restart'])[-4:])
print('LeaveAll MRPDUs bridge/DUT', agg['la_bridge'], agg['la_dut'])
print('capture span total s', round(agg['span'], 3))
print('START/STOP deltas', agg['startstop'])
print('DUT TA Lv in hold (cycle, s after bridge Lv, s after DISCONNECT_RX response)', agg['ta_lv'])
print('LeaveAll (any party) before Lv inside capture', len(agg['la_before_lv']), agg['la_before_lv'][:10])
for p, cs in sorted(agg['prof'].items(), key=lambda kv: -len(kv[1])):
    print('profile', len(cs), p, cs if len(cs) < 15 else '')
print('mismatches', agg['mism'])
