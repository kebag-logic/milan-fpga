#!/usr/bin/env python3
"""Compare missing-build grading with and without an unrelated participant."""
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'))
import selftest
import selftest_leaveall as fixture
import mrpdu_grade
import run

graded = fixture.harness(selftest.synthetic, selftest.SYS_HZ, selftest.CPU_HZ, selftest.tx_record)
escaped = 0
late_escaped = 0
for interface in (0, 1):
    for app in (fixture.MSRP, fixture.MVRP):
        who = f'if{interface} {mrpdu_grade.APPLICATIONS[app]}'
        other = fixture.MVRP if app == fixture.MSRP else fixture.MSRP
        for peer in (False, True):
            sends = ((1000, app, False, interface),)
            if peer:
                sends += ((1250, other, False, 1 - interface),)
            _, held = graded(sends, ((1300, 'on_pt_timer', who),), ordinary=(1400,))
            misses = run.stated_misses([dict(group='missing-build', passes=dict(joins=held))])
            observed = next(k for k, v in held['runs'].items() if v)
            expected = 'absent'
            print(json.dumps(dict(owner=who, unrelated_participant=peer, expiry_ms=1300.001,
                                  owner_opportunity_ms=1300.001, bound_ms=49,
                                  log_end_ms=1400.020, expected=expected, observed=observed,
                                  findings=misses), sort_keys=True))
            if peer:
                escaped += observed != expected or not misses
            else:
                assert observed == expected and len(misses) == 1
        # A log genuinely ending before this owner's deadline remains unresolved.
        _, early = graded(((1000, app, False, interface),),
                          ((1300, 'on_pt_timer', who),), ordinary=(1340,))
        assert early['runs']['unresolved'] == 1 and not early['failing']
        # The same late first build cannot become timely by emitting only another participant's frame.
        prior = ((1000, app, False, interface), (1250, other, False, 1 - interface))
        for emits_other in (False, True):
            sends = prior + (((1431, other, False, 1 - interface),) if emits_other else ())
            rows, held = graded(sends, ((1300, 'on_pt_timer', who),), ordinary=(1500,),
                                empty=() if emits_other else (1431,))
            misses = run.stated_misses([dict(group='late-build', passes=dict(joins=held))])
            observed = next(k for k, v in held['runs'].items() if v)
            print(json.dumps(dict(owner=who, emits_other=emits_other, expiry_ms=1300.001,
                                  first_build_ms=1430.98, owner_delay_ms=130.979,
                                  expected='late', observed=observed, findings=misses,
                                  rows=[dict(interface=r['interface'], ms=r['ms']) for r in rows]), sort_keys=True))
            if emits_other:
                late_escaped += observed != 'late' or not misses
            else:
                assert observed == 'late' and len(misses) == 1
print(f'{escaped} missing-build failures hidden by another participant; 4 absent controls and 4 short-log controls passed')
print(f'{late_escaped} late-build failures hidden by another participant output; 4 empty-build late controls passed')
raise SystemExit(1 if escaped or late_escaped else 0)
