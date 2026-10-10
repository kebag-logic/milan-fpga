#!/usr/bin/env python3
"""Recompute the item 2 figures of B14_BENCH_5603C353.md from the archived switches.json."""
import json, sys, statistics
pk = sys.argv[1]
d = json.load(open(pk + '/author/item2/summary/switches.json'))
aaf = [s for s in d if s['tag'].endswith('-aaf')]
crf = [s for s in d if s['tag'].endswith('-crf')]
ints = [s for s in d if s['tag'].endswith('-int')]
print('n aaf/crf/int', len(aaf), len(crf), len(ints))
for s in d:
    print(s['tag'], s['locked_s'], s.get('settle_boundary_s'), s['slip_lb_transient_dups'], s['slip_lb_after_dups'],
          s['slip_lb_after_skips'], [st['s_hi'] for st in s['slip_lb_steps']], s['rails_before_end'],
          s['converged_zero_polls_s'], s['servo_end'], s['trim_end_ppm'], s['bad_polls'],
          (s.get('counters_locked_to_end') or {}).get('dut-0x0005-0', {}).get('MEDIA_UNLOCKED', 0),
          (s.get('counters_locked_to_end') or {}).get('dut-0x0005-1', {}).get('MEDIA_UNLOCKED', 0))
print('aaf frames', [s['slip_lb_transient_dups'] / 2 for s in aaf])
print('aaf locked range', min(s['locked_s'][0] for s in aaf), max(s['locked_s'][1] for s in aaf))
print('crf locked range', min(s['locked_s'][0] for s in crf), max(s['locked_s'][1] for s in crf))
print('trim range followed', min(s['trim_end_ppm'] for s in aaf + crf), max(s['trim_end_ppm'] for s in aaf + crf))
print('servo_end set', {s['servo_end'] for s in aaf + crf})
# boundary check: any step after boundary in followed holds
for s in aaf + crf:
    bnd = s['locked_s'][1] + 4.096 + 0.5
    late = [st['s_hi'] for st in s['slip_lb_steps'] if st['s_hi'] > bnd]
    between = [st['s_hi'] for st in s['slip_lb_steps'] if s['locked_s'][1] <= st['s_hi'] <= bnd]
    if late or between or abs(bnd - (s.get('settle_boundary_s') or bnd)) > 0.002:
        print('  boundary', s['tag'], 'bnd', round(bnd, 3), 'json', s.get('settle_boundary_s'), 'between', between, 'late', late)
# counters moved other than expected
exp = {'LOCKED', 'UNLOCKED', 'MEDIA_RESET', 'FRAMES_TX', 'FRAMES_RX', 'TIMESTAMP_VALID'}
for s in aaf + crf + ints:
    for k, v in s['counters_before_to_end'].items():
        other = {c: n for c, n in v.items() if c not in exp and n}
        if other:
            print('  other counter', s['tag'], k, other)
    for k, v in (s.get('counters_locked_to_end') or {}).items():
        err = {c: n for c, n in v.items() if c not in {'FRAMES_TX', 'FRAMES_RX', 'TIMESTAMP_VALID'} and n}
        if err and s in aaf + crf:
            print('  locked->end moved', s['tag'], k, err)
for s in aaf + crf:
    t = s['tap']
    for st in ('peer-aaf', 'peer-crf', 'dut-aaf', 'dut-crf'):
        x = t[st]
        if x['seq_gaps'] or x['tv0'] or x['tu1'] or x['ts_steps_off_mode_gt_1us'] or (st.startswith('peer') and x['mr_toggles_s']) or (st.startswith('dut') and len(x['mr_toggles_s']) != 1):
            print('  tap anomaly', s['tag'], st, x)
    print('  mr', s['tag'], [round(t[k]['mr_toggles_s'][0], 3) for k in ('dut-aaf', 'dut-crf')])
