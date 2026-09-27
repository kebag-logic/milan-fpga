#!/usr/bin/env python3
"""Independently recompute the findings page's per-cycle table and summary
claims from the packet's cycleNN/analysis.json, and report ordering checks the
page's claims depend on.  usage: recompute_table.py <page.md> <packet author dir>"""
import json, os, re, sys
page, pk = sys.argv[1], sys.argv[2]
lines = open(page).read().splitlines()
hdr = next(i for i, l in enumerate(lines) if l.startswith('| Cycle | OFF duration'))
ncol = lambda l: len(l.strip().strip('|').split('|'))
print('header cells', ncol(lines[hdr]), '; delimiter cells', ncol(lines[hdr + 1]),
      '; body cells', sorted({ncol(l) for l in lines[hdr + 2:hdr + 12]}))
prow = {int(l.split('|')[1]): [c.strip() for c in l.strip().strip('|').split('|')] for l in lines[hdr + 2:hdr + 12]}
F = lambda x: '%.2f' % x
def seq(vals):
    out = []
    for v in vals:
        if not out or out[-1] != v: out.append(v)
    return ' > '.join(map(str, out))
def gm_pattern(s):
    # role labels only: A = first grandmaster seen, SELF = the DUT's own id
    dut = s['states_end']['dut'][0]['listener'] if s['states_end']['dut'] else None
    lab = {}
    out = []
    for t, g in s['gm']:
        if g == dut: out.append('SELF')
        else: out.append(lab.setdefault(g, chr(65 + len(lab))))
    return '>'.join(out)
mism = 0; S = []
for n in range(1, 11):
    s = json.load(open(os.path.join(pk, 'cycle%02d' % n, 'analysis.json'))); S.append(s)
    off = s['off']
    car = [(t - off, v) for t, v in s['carrier'] if t > off]
    down = next(t for t, v in car if v == 0); up = next(t for t, v in car if v == 1 and t > down)
    st = s['large_phc_discontinuities']
    b0, b1 = st[0]['bracket']
    endpoint_parts = {'media_dut': s['media_locked_at']['dut'], 'servo': s['servo_locked_at'], 'gptp': s['gptp_recovered_at']}
    end = max(endpoint_parts.values())
    mine = [str(n), F(s['off_hold_s']), '%s / %s' % (F(down), F(up)),
            '%s / %s-%s' % (F(s['first_gm'] - off), F(b0 - off), F(b1 - off)), F(s['gptp_recovery_s']),
            '%s / %s' % (F(s['wire']['dut']['first_after_on'] - off), F(s['wire']['peer']['first_after_on'] - off)),
            '%s-%s' % (F(end - b1), F(end - b0)),
            '%d / %d' % (len(s['wire']['dut']['mr']) - 1, len(s['wire']['peer']['mr']) - 1),
            seq([v['2'] for t, v in s['counter_transitions']['dut:counter-6-1']])]
    diff = [(i, a, b) for i, (a, b) in enumerate(zip(mine, prow[n])) if a != b]
    if diff: mism += 1
    # ordering checks
    health_after_on = [(round(t - off, 2), h) for t, h in s['health'] if t > s['on']]
    tu_after_rec = [x for x in s['health'] if x[0] > s['gptp_recovered_at'] and x[1] != ['1', '1', '0']]
    print('cycle %2d: %s | steps=%d amount=%.2f s | step_end-gm=%.2f rec-step_end=%.2f | endpoint=%s | '
          'first-after-wire dut/peer=%.2f/%.2f | health>on=%s | unhealthy_after_rec=%d | gm_ids=%s | GMCH=%s | '
          'MLK/MUL=%s/%s CD=%s/%s SS/SP=%s/%s peerSS/SP=%s/%s | mac=%s epochs=%s gap=%.3f | servo=%s | carrier_n=%d'
          % (n, 'MATCH' if not diff else 'DIFF %s' % diff, len(st), st[0]['phc_minus_wall_delta_s'],
             b1 - s['first_gm'], s['gptp_recovered_at'] - b1,
             max(endpoint_parts, key=endpoint_parts.get),
             s['wire']['dut']['first_valid_after_wire_return_s'], s['wire']['peer']['first_valid_after_wire_return_s'],
             health_after_on, len(tu_after_rec), gm_pattern(s),
             s['counter_endpoints']['dut:counter-9-0']['delta'],
             s['counter_endpoints']['dut:counter-5-1']['delta']['0'], s['counter_endpoints']['dut:counter-5-1']['delta']['1'],
             s['counter_endpoints']['dut:counter-36-0']['delta']['0'], s['counter_endpoints']['dut:counter-36-0']['delta']['1'],
             s['counter_endpoints']['dut:counter-6-1']['delta']['0'], s['counter_endpoints']['dut:counter-6-1']['delta']['1'],
             s['counter_endpoints']['peer:counter-6-2']['delta']['0'], s['counter_endpoints']['peer:counter-6-2']['delta']['1'],
             s['mac_status'] and sorted({v for t, v in s['mac_status']}), s['reset_epochs'], s['max_console_gap_s'],
             [v for t, v in s['servo_states']], len(s['carrier'])))
print('table rows differing:', mism)
rec = [s['gptp_recovery_s'] for s in S]
fw = [s['wire'][r]['first_valid_after_wire_return_s'] for s in S for r in ('dut', 'peer')]
ends = [max(s['media_locked_at']['dut'], s['servo_locked_at'], s['gptp_recovered_at']) - s['large_phc_discontinuities'][0]['bracket'][0] for s in S]
amts = [s['large_phc_discontinuities'][0]['phc_minus_wall_delta_s'] for s in S]
zero = sum('> 0 >' in seq([v['2'] for t, v in s['counter_transitions']['dut:counter-6-1']]) for s in S)
print('gPTP recovery range %.3f-%.3f (page 0.44-1.82)' % (min(rec), max(rec)))
print('first valid after wire return %.2f-%.2f (page 5.07-14.00)' % (min(fw), max(fw)))
print('longest step-to-media %.2f (page 12.54)' % max(ends))
print('steps: c1 %.0f, c2 %.2f, c3-10 %.2f..%.2f (page -358781, -162.46, -95.74..-96.47)' % (amts[0], amts[1], max(amts[2:]), min(amts[2:])))
print('MEDIA_RESET intermediate zero caught in %d/10 (page 5)' % zero)
print('max console gap %.3f (page 0.251)' % max(s['max_console_gap_s'] for s in S))
print('half-RTT controller max %.3f tap max %.3f; anchor spread %s' % (
    max(s['clock_half_rtt_s']['controller'] for s in S), max(s['clock_half_rtt_s']['tap'] for s in S),
    [round(min(s['tap_anchor_spread_s'][0] for s in S), 3), round(max(s['tap_anchor_spread_s'][1] for s in S), 3)]))
print('switch frames absent while off, all cycles:', all(s['switch_frames_absent_off'] for s in S))
print('bindings_ok all:', all(s['bindings_ok'] for s in S), '; steady_recovered all:', all(s['steady_recovered'] for s in S))
