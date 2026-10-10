#!/usr/bin/env python3
"""R575-2: recompute, from the archived per-cycle msrp.tsv/acmp.tsv, the bridge Listener Lv
after the DISCONNECT_RX response (ACMP message_type 9) and every DUT Talker Advertise Lv.
Usage: check_item3_withdrawals.py <author/item3>"""
import csv, os, sys
d = sys.argv[1]
CRF = '0200000000010001'
tsv = {r['cycle'].replace('cycle-', '').zfill(3): r for r in csv.DictReader(open(os.path.join(d, 'cycles.tsv')), delimiter='\t')}
maxdiff = 0.0; ta_lv_cycles = []; lvs = []
for c in sorted(x for x in os.listdir(os.path.join(d, 'cycles')) if x.startswith('cycle-')):
    n = c.split('-')[1]
    ms = list(csv.DictReader(open(os.path.join(d, 'cycles', c, 'msrp.tsv')), delimiter='\t'))
    ac = list(csv.DictReader(open(os.path.join(d, 'cycles', c, 'acmp.tsv')), delimiter='\t'))
    resp = [float(r['t_s']) for r in ac if r['mt'] == '9']
    t_resp = resp[0]
    blv = [float(r['t_s']) for r in ms if r['sender'] == 'bridge' and r['type'] == 'Listener' and r['event'] == 'Lv' and r['stream_id'] == CRF and float(r['t_s']) > t_resp]
    t_blv = blv[0]
    lv_ms = (t_blv - t_resp) * 1e3
    lvs.append((n, lv_ms))
    ref = float(tsv[n]['lv_after_disconnect_s']) * 1e3 if n in tsv and tsv[n]['lv_after_disconnect_s'] not in ('', 'None') else None
    if ref is not None: maxdiff = max(maxdiff, abs(ref - lv_ms))
    talv = [r for r in ms if r['sender'] == 'DUT' and r['type'] == 'TalkerAdvertise' and r['event'] == 'Lv']
    for r in talv:
        t = float(r['t_s'])
        ta_lv_cycles.append(n)
        print(f'cycle {n}: DUT TA Lv stream {r["stream_id"]} at {t:.9f}; after bridge Lv {t - t_blv:.4f} s; after DISCONNECT_RX response {t - t_resp:.4f} s; cycles.tsv dut_ta_lv_in_hold={tsv.get(n, {}).get("dut_ta_lv_in_hold")}')
print('cycles', len(lvs), 'compared with cycles.tsv', sum(1 for n, _ in lvs if n in tsv), 'max |cycles.tsv - recomputed| ms', round(maxdiff, 6))
g = [v for n, v in lvs if n != '001']
s = sorted(g)
print('graded Lv after response ms: min %.3f max %.3f median %.3f' % (s[0], s[-1], (s[49] + s[50]) / 2))
print('late (>50 ms):', [(n, round(v, 3)) for n, v in lvs if v > 50])
print('cycles with a DUT TA Lv:', sorted(set(ta_lv_cycles)))
print('cycles.tsv dut_ta_lv_in_hold true:', [n for n, r in sorted(tsv.items()) if r['dut_ta_lv_in_hold'] not in ('0', 'False', '', 'None', 'false')])
