#!/usr/bin/env python3
"""Re-grade the ten B19 grandmaster edges from bench/gmNN/analysis.json alone
(not from the summary). Split each run at 27 s, as the page states.
Counter indices: STREAM_INPUT 1 MEDIA_UNLOCKED, 4 MEDIA_RESET;
STREAM_OUTPUT 2 MEDIA_RESET; AVB_INTERFACE 5 GPTP_GM_CHANGED.
Usage: check_gm_steps.py <author-dir>"""
import json, os, sys
auth = sys.argv[1]
SPLIT = 27.0
PAGE_PHC = {1: (9.987, -10.003), 2: (9.987, -10.004), 3: (9.987, -10.004), 4: (9.987, -10.005), 5: (9.987, -10.004)}
bad = 0
def at(trans, t, idx):
    v = None
    for tt, c in trans:
        if tt <= t and idx in c: v = c[idx]
    return v
for r in range(1, 6):
    a = json.load(open(os.path.join(auth, 'bench', 'gm%02d' % r, 'analysis.json')))
    tr = a['counter_transitions']; end = a['counter_endpoints']
    health = a['health']; wire = a['wire']['dut']
    jumps = [round(j['delta_s'] * 1e3, 3) for j in a['dut_phc_wire_jumps']]
    for k, (lo, hi) in enumerate(((-1e9, SPLIT), (SPLIT, 1e9))):
        edge = ('takeover', 'release')[k]
        def delta(key, idx):
            t = tr[key]
            v0 = at(t, lo if lo > -1e9 else -1e8, idx) if lo > -1e9 else t[0][1].get(idx)
            v1 = at(t, hi, idx) if hi < 1e9 else end[key]['last'].get(idx)
            return None if v0 is None or v1 is None else v1 - v0
        tu_rises = sum(1 for i in range(1, len(health)) if lo < health[i][0] <= hi
                       and 'tu1' in health[i][1] and 'tu1' not in health[i - 1][1])
        asc0 = sum(1 for h in health if lo < h[0] <= hi and 'asc0' in h[1])
        w_tu = [x for x in wire['tu'] if lo < x[0] <= hi and x[1] == 1]
        mr = sorted({m[1] for m in wire['mr']})
        g = dict(
            gm_changed=delta('dut:counter-9-0', '5'),
            mr_aaf_talker=delta('dut:counter-6-0', '2'), mr_crf_talker=delta('dut:counter-6-1', '2'),
            mr_peer_crf_listener=delta('peer:counter-5-8', '4'),
            unl_dut=delta('dut:counter-5-0', '1'), unl_peer_crf=delta('peer:counter-5-8', '1'),
            unl_peer_aaf=delta('peer:counter-5-0', '1'),
            dut_listener_media_reset=delta('dut:counter-5-0', '4'),
            peer_aaf_talker_media_reset=delta('peer:counter-6-0', '2'))
        ok = (tu_rises == 1 and len(w_tu) == 1 and asc0 == 0 and g['gm_changed'] == 1 and len(mr) == 1
              and g['mr_aaf_talker'] == 0 and g['mr_crf_talker'] == 0 and g['mr_peer_crf_listener'] == 0
              and g['unl_dut'] == 0 and g['unl_peer_crf'] == 0 and g['unl_peer_aaf'] == 0
              and abs(jumps[k] - PAGE_PHC[r][k]) < 0.0015)
        bad += not ok
        print('run', r, edge, 'PASS' if ok else 'FAIL', 'phc_step_ms', jumps[k], 'page', PAGE_PHC[r][k],
              'tu rises console', tu_rises, 'wire tu=1 episodes', len(w_tu), 'asc0 samples', asc0, 'mr values', mr, g)
    print('   run', r, 'samples', a['console_samples'], 'max gap', round(a['max_console_gap_s'], 3),
          'crf max gap', a['wire']['dut']['max_gap_s'], 'tu1 pdus', a['wire']['dut']['tu_counts'].get('1'),
          'TUCNT', a['clkv_tucnt_first_last'], 'servo', a['servo'], 'crf_ctrl', a['crf_ctrl'])
print('RESULT', 'FAIL' if bad else 'PASS')
