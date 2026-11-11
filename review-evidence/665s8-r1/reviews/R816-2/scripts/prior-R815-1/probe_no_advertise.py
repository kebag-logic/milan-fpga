#!/usr/bin/env python3
"""Probe: the self-test's clean 37 s campaign-shaped log, rebuilt with ADP never re-advertising (only the startup
ENTITY_AVAILABLE and its advertise arm; the periodic delays and AVAILABLEs gone), graded as a campaign unit
(two ANNOUNCEs). A pass means the grade does not require an advertise-period sample (#868 item 3).

usage: probe_no_advertise.py <checkout>
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_wire_timing'))
import wire_grade as g
import wire_selftest as t
for name, delays in (('clean-announce-interval (control)', t.ADP_DELAYS), ('no periodic advertising', ())):
    log = t.announced(delays=delays).text()
    result, findings = g.grade('\n'.join(log) + '\n', t.SYS_HZ, 2, 1, 2)
    n = {r['path']: r['n'] for r in result['rows']}
    print(f"{name}: findings={len(findings)} adp.advertise_period n={n.get('adp.advertise_period')} "
          f"adp.egress n={n.get('adp.egress')} maap.announce_interval n={n.get('maap.announce_interval')}")
    for f in findings:
        print('  FINDING', f)
