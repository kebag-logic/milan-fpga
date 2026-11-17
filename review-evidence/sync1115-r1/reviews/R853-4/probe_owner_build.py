#!/usr/bin/env python3
"""R853-3 probe: owner-bound grading of an owned periodic run-out at the reviewed head.

Usage: python3 -B probe_owner_build.py <checkout>

For each owner (both applications on both interfaces), a periodic run-out at 1,300.001 ms whose owner's join timer
has run out (last owner send at 1,000 ms), so the owner's opportunity is the run-out itself:

  F  another participant's build and MRPDU (other application, other interface) at 1,311 ms, inside 49 ms; the
     owner's own MRPDU at 1,431 ms in a separate build run, 131 ms after the owner's opportunity.
  FE the same, the 1,311 ms build sending nothing.
  O  control: the owner's own MRPDU alone at 1,431 ms (expected late).
  J  control: the owner's own running join timer (owner's last send at 1,250 ms arms it to the 1,430 ms TICK); the
     owner's MRPDU at 1,431 ms (expected released, row ~1 ms, from the owner's own opportunity).
  JF control: J plus another participant's MRPDU at 1,311 ms on the other interface.

Prints one JSON line per case with the observed outcome, the findings and the rows. Exit 0 always; the report reads
the lines. Changes nothing in the checkout.
"""
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'))
import selftest  # noqa: E402
import selftest_leaveall as fixture  # noqa: E402
import mrpdu_grade  # noqa: E402
import run  # noqa: E402

graded = fixture.harness(selftest.synthetic, selftest.SYS_HZ, selftest.CPU_HZ, selftest.tx_record)
timer = lambda who: ((1300, 'on_pt_timer', who),)
for interface in (0, 1):
    for app in (fixture.MSRP, fixture.MVRP):
        who = f'if{interface} {mrpdu_grade.APPLICATIONS[app]}'
        other = fixture.MVRP if app == fixture.MSRP else fixture.MSRP
        base = ((1000, app, False, interface),)
        cases = {
            'F': dict(sends=base + ((1311, other, False, 1 - interface), (1431, app, False, interface))),
            'FE': dict(sends=base + ((1431, app, False, interface),), empty=(1311,)),
            'O': dict(sends=base + ((1431, app, False, interface),)),
            'J': dict(sends=((1250, app, False, interface), (1431, app, False, interface))),
            'JF': dict(sends=((1250, app, False, interface), (1311, other, False, 1 - interface),
                              (1431, app, False, interface))),
        }
        for name, c in cases.items():
            rows, held = graded(c['sends'], timer(who), ordinary=(1500,), empty=c.get('empty', ()))
            misses = run.stated_misses([dict(group=name, passes=dict(joins=held))])
            print(json.dumps(dict(case=name, owner=who, runs={k: v for k, v in held['runs'].items() if v},
                                  findings=misses,
                                  rows={r['probe'].split('.mrpdu.')[1]: r['ms'] for r in rows}), sort_keys=True))
