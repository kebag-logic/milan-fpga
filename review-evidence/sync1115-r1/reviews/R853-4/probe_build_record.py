#!/usr/bin/env python3
"""R853-4 probe: build-participant grading of an owned periodic run-out at the reviewed head (mrpdu_grade.settle).

Usage: python3 -I -B probe_build_record.py <checkout>

For each owner (both applications on both interfaces), a periodic run-out at 1,300.001 ms whose owner's last send was
at 1,000 ms, so its opportunity is the run-out itself (the bound ends at 1,349.001 ms). Cases:

  RE  another participant's build at 1,311 ms, RECORDED as that participant's, sending nothing; the owner's MRPDU at
      1,431 ms. Expected late (130.999 ms).
  RA  as RE with no owner MRPDU at all and no build past the bound; the log runs on. Expected absent.
  UR  a build at 1,311 ms whose slot the testbench recorded `unresolved`, sending nothing; the owner's MRPDU at
      1,431 ms. Expected late.
  PB  the owner's own join timer running (last send 1,250 ms, opportunity the 1,430 ms TICK), its own empty build at
      1,311 ms (before the opportunity); no owner frame; another participant's build at 1,500 ms past the bound.
      Expected late, resting on the bound.
  UF  control: a build at 1,311 ms with no participant recorded, then the owner's MRPDU at 1,312 ms in the same run.
      Expected released, row 12 ms.
  OF  control: another participant's MRPDU at 1,311 ms and the owner's at 1,312 ms in the same run. Expected
      released, row 12 ms.

Prints one JSON line per case (observed outcome, failing entries, rows) and a final summary line with the number of
cases whose outcome differs from the expectation. Exit 0 when all match, 1 otherwise. Changes nothing in the checkout.
"""
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'))
import selftest  # noqa: E402
import selftest_leaveall as fixture  # noqa: E402
import mrpdu_grade  # noqa: E402

graded = fixture.harness(selftest.synthetic, selftest.SYS_HZ, selftest.CPU_HZ, selftest.tx_record)
bad = 0
for interface in (0, 1):
    for app in (fixture.MSRP, fixture.MVRP):
        who = f'if{interface} {mrpdu_grade.APPLICATIONS[app]}'
        other = fixture.MVRP if app == fixture.MSRP else fixture.MSRP
        other_who = f'if{1 - interface} {mrpdu_grade.APPLICATIONS[other]}'
        base = ((1000, app, False, interface),)
        cases = {
            'RE': (dict(sends=base + ((1431, app, False, interface),), empty=((1311, other_who),)), 'late'),
            'RA': (dict(sends=base, empty=((1311, other_who),), ordinary=(1500, 1600)), 'absent'),
            'UR': (dict(sends=base + ((1431, app, False, interface),), empty=((1311, 'unresolved 0000000a'),)), 'late'),
            'PB': (dict(sends=((1250, app, False, interface), (1500, other, False, 1 - interface)),
                        empty=((1311, who),), ordinary=(1600,)), 'late'),
            'UF': (dict(sends=base + ((1312, app, False, interface),), empty=(1311,)), 'released'),
            'OF': (dict(sends=base + ((1311, other, False, 1 - interface), (1312, app, False, interface))), 'released'),
        }
        for name, (c, want) in cases.items():
            rows, held = graded(c['sends'], ((1300, 'on_pt_timer', who),), c.get('ordinary', (1500,)),
                                c.get('empty', ()))
            got = [k for k, v in held['runs'].items() if v]
            ok = got == [want]
            bad += not ok
            print(json.dumps(dict(case=name, owner=who, want=want, got=got, ok=ok,
                                  failing=[(f['outcome'], f.get('by'), f['from_ms'], f['after_ms'])
                                           for f in held['failing']],
                                  rows={r['probe'].split('.mrpdu.')[1]: r['ms'] for r in rows}), sort_keys=True))
print(json.dumps(dict(summary=True, mismatches=bad)))
sys.exit(1 if bad else 0)
