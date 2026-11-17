#!/usr/bin/env python3
"""Focused expiry ownership controls; run with the reviewed checkout as argv[1]."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'))
import selftest
import selftest_leaveall as fixture
import mrpdu_grade
import run

graded = fixture.harness(selftest.synthetic, selftest.SYS_HZ, selftest.CPU_HZ, selftest.tx_record)
count = 0
for interface in (0, 1):
    for app in (fixture.MSRP, fixture.MVRP):
        who = f'if{interface} {mrpdu_grade.APPLICATIONS[app]}'
        other = fixture.MVRP if app == fixture.MSRP else fixture.MSRP
        peer = f'if{interface} {mrpdu_grade.APPLICATIONS[other]}'
        prior = ((1000, app, False, interface), (1040, other, False, interface))
        timers = ((1050, fixture.LA, who), (1180, fixture.JOIN, who),
                  (1190, fixture.LA, peer), (1220, fixture.JOIN, peer))
        for case, output, ordinary, expected in (
            ('skipped', ((1181, app, False, interface), (1221, other, True, interface),
                         (1371, app, True, interface)), (), {'sent': 1, 'skipped': 1}),
            ('late', ((1221, other, True, interface), (1240, app, True, interface)), (),
             {'sent': 1, 'late': 1}),
            ('absent', ((1221, other, True, interface),), (1500,), {'sent': 1, 'absent': 1}),
            ('clean', ((1181, app, True, interface), (1221, other, True, interface)), (), {'sent': 2}),
        ):
            rows, held = graded(prior + output, timers, ordinary=ordinary)
            assert fixture.by(held) == expected, (who, case, held)
            if case != 'clean':
                failures = held['leave_all']['failing']
                assert len(failures) == 1 and failures[0]['who'] == who
                assert failures[0]['opportunity_ms'] == 1180
                assert who in fixture.named(test=held)[0]
            if case == 'skipped':
                assert fixture.row(rows, 'leaveall', interface) == 191
            count += 1
            print('PASS', who, case)
        _, held = graded(((900, other, False, interface), (1000, app, False, interface),
                          (1101, other, True, interface), (1181, app, True, interface)),
                         ((1050, fixture.LA, who), (1100, fixture.LA, peer), (1180, fixture.JOIN, who)))
        assert fixture.by(held) == {'sent': 2} and not held['failing']
        count += 1
        print('PASS', who, 'clean reordered')
        # Test the exact inclusive 49 ms boundary, and its first whole-ms violation.
        for end, expected in ((1229, 'sent'), (1230, 'late')):
            _, held = graded(((1000, app, False, interface), (end, app, True, interface)),
                             ((1050, fixture.LA, who),))
            assert fixture.by(held) == {expected: 1}, (who, end, held)
            count += 1
            print('PASS', who, 'boundary', end, expected)
        # Empty periodic builds must use this owner's opportunity even with an unrelated callback.
        for callback in ((), ((1330, fixture.JOIN, peer),)):
            _, held = graded(((1000, app, False, interface),),
                             ((1300, 'on_pt_timer', who),) + callback, (1400,), (1360,))
            failure = next(f for f in held['failing'] if f['kind'] == 'periodic')
            assert failure['outcome'] == 'late' and failure['after_ms'] == 59.979
            count += 1
            print('PASS', who, 'empty periodic owner anchor', bool(callback))
        for timer in mrpdu_grade.TIMERS:
            for owner in (None, 'unresolved 12345678'):
                _, held = graded(((1000, app, False, interface), (1181, app, True, interface)),
                                 ((1050, timer, owner),))
                assert held['runs']['unowned'] == 1
                misses = run.stated_misses([dict(group='probe', passes=dict(joins=held))])
                assert any('(owner unresolved)' in m for m in misses), misses
                count += 1
                print('PASS', who, timer, 'missing' if owner is None else 'unresolved')
assert mrpdu_grade.LATE_MS == 49
print(f'{count} controls; 0 failures; bound 49 ms')
