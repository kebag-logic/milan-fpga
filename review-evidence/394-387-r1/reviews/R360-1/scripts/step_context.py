#!/usr/bin/env python3
"""For each cycle, place the PHC step bracket against the media state it hit:
servo state transitions, DUT CRF input unlock/relock, stream stop/start reads,
and first PDUs in each direction.  All times are seconds after the OFF command.
usage: step_context.py <packet author dir>"""
import json, os, sys
pk = sys.argv[1]
names = {3: 'ACQUIRE', 4: 'LOCKED', 5: 'HOLDOVER'}
for n in range(1, 11):
    s = json.load(open(os.path.join(pk, 'cycle%02d' % n, 'analysis.json')))
    off = s['off']; r = lambda t: round(t - off, 2)
    b0, b1 = s['large_phc_discontinuities'][0]['bracket']
    servo = [(r(t), names.get(v, v)) for t, v in s['servo_states']]
    st_before = [v for t, v in s['servo_states'] if t <= b0][-1]
    ssp = [(r(t), v) for t, v in s['counter_transitions']['dut:counter-6-1']]
    mlk = [(r(t), v['0'], v['1']) for t, v in s['counter_transitions']['dut:counter-5-1']]
    print('cycle %2d step %.2f-%.2f | servo before step=%s | servo %s | DUT in MLK/MUL reads %s | DUT out START/STOP/MR reads %s | first DUT tx %.2f, first CRF into DUT %.2f, media_locked(dut) %.2f, servo LOCKED %.2f | last wire before gap %.2f, first wire return %.2f'
          % (n, r(b0), r(b1), names.get(st_before, st_before), servo, mlk,
             [(t, v['0'], v['1'], v['2']) for t, v in ssp], r(s['wire']['dut']['first_after_on']),
             r(s['wire']['peer']['first_after_on']), r(s['media_locked_at']['dut']), r(s['servo_locked_at']),
             r(s['last_wire_before_gap']), r(s['first_wire_return'])))
