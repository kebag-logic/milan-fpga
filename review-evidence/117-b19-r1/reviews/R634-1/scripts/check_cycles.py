#!/usr/bin/env python3
"""Recompute the B19 per-cycle table and the box 3 edge placements from the
packet's bench/cycleNN/correlation.json. Usage: check_cycles.py <author-dir>"""
import json, os, sys
auth = sys.argv[1]
PAGE = {  # page table: sync0, gm_self, asc0, sw_first_frame, sw_first_ann, asc1, gm_sw, allgood, recovery
 1: (1.73, 3.73, 5.73, 39.25, 40.26, 40.75, 41.50, 41.75, 1.49),
 2: (1.73, 3.49, 5.49, 39.35, 40.37, 40.50, 40.50, 41.00, 0.63),
 3: (1.49, 3.99, 5.74, 39.22, 40.23, 40.75, 41.50, 42.00, 1.77),
 4: (1.75, 3.75, 6.00, 39.02, 40.27, 40.01, 40.51, 41.01, 0.75),
 5: (1.74, 3.49, 6.24, 39.05, 40.25, 40.25, 40.50, 40.75, 0.50),
 6: (1.47, 3.47, 6.22, 38.99, 40.26, 40.24, 40.49, 40.74, 0.47)}
bad = 0
for c in range(1, 7):
    d = json.load(open(os.path.join(auth, 'bench', 'cycle%02d' % c, 'correlation.json')))
    e, w = d['edges'], d['wire']
    def edge(k, to):
        xs = [x for x in e[k] if str(x['to']) == str(to)]
        return xs
    s0 = edge('sync', 0)[0]; g_self = edge('gm', '020000fffe000001')[0]
    a0 = edge('asCapable', 0)[0]; a1 = edge('asCapable', 1)[-1]
    g_sw = edge('gm', '3cc0c6fffefe0210')[-1]; t0 = edge('tu', 0)[-1]
    ann = w['switch_announces_after_return']
    rec = t0['first_after'] - ann[0][0]
    mine = (s0['first_after'], g_self['first_after'], a0['first_after'], w['switch_first_frame'],
            ann[0][0], a1['first_after'], g_sw['first_after'], t0['first_after'], rec)
    diffs = [round(m - p, 3) for m, p in zip(mine, PAGE[c])]
    ok = all(abs(x) <= 0.006 for x in diffs)
    bad += not ok
    print('cycle', c, 'table', 'MATCH' if ok else 'DIFF', [round(x, 3) for x in mine], diffs if not ok else '')
    # loss edges relative to wire causes
    ls, la, lp = w['switch_last_sync'], w['switch_last_announce'], w['switch_last_pdelay_resp']
    print('   sync loss after last Sync: (%.3f, %.3f]; 0.375 s timeout inside: %s' % (
        s0['last_before'] - ls, s0['first_after'] - ls, s0['last_before'] <= ls + 0.375 <= s0['first_after']))
    print('   GM loss after last Announce: (%.3f, %.3f]; 3 s timeout inside: %s' % (
        g_self['last_before'] - la, g_self['first_after'] - la, g_self['last_before'] <= la + 3.0 <= g_self['first_after']))
    print('   asCapable loss after last Pdelay_Resp: (%.3f, %.3f]' % (a0['last_before'] - lp, a0['first_after'] - lp), a0['how'])
    dp = w['dut_completed_pdelay_after_return']
    second = dp[1] if len(dp) > 1 else None
    print('   asCapable return interval (%.3f, %.3f]; DUT 2nd completed exchange %.3f inside: %s' % (
        a1['last_before'], a1['first_after'], second, a1['last_before'] <= second <= a1['first_after']))
    acc = [a[0] for a in ann if a[0] <= g_sw['first_after']]
    accepted = acc[-1]
    print('   GM return interval (%.4f, %.4f]; latest Announce before first_after %.4f; inside: %s; cause-to-last_before %.4f; first sample after cause %.3f' % (
        g_sw['last_before'], g_sw['first_after'], accepted, g_sw['last_before'] <= accepted <= g_sw['first_after'],
        g_sw['last_before'] - accepted, g_sw['first_after'] - accepted))
    for x in d.get('crf_tu_vs_csr', []):
        if x['wire']['to'] == 1:
            print('   first tu=1 CRF PDU %.3f in CSR tu rise (%.4f, %.4f]: %s' % (
                x['wire']['first_after'], x['csr']['last_before'], x['csr']['first_after'], x['wire_inside']))
    print('   tu1 PDUs', w.get('crf_tu1_pdus'), 'mr values', w.get('crf_mr_values'), 'TUCNT', d.get('clkv_tucnt'),
          'placed_by_phc', d['placed_by_phc'], '/', d['samples'], 'dut master syncs', w['dut_master_frames']['syncs'],
          'dut announces', w['dut_master_frames']['announces'])
print('RESULT', 'FAIL' if bad else 'PASS')
