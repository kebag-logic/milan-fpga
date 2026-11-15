#!/usr/bin/env python3
"""Reviewer probe: in the answering-ports arm's aecp-fanout, a SET_CONFIGURATION record whose response is committed
after the next record starts is named unanswered by record_classes.named(); is it still held?

usage: python3 -I record_classes_unanswered_probe.py REPO
The synthetic pass is record_classes.synthetic()'s, with one more arm-B record of 40,000 CPU cycles (420 us by the
rule, over the paced 300 and the ordinary 235) whose SET_CONFIGURATION response lands after the following record.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / 'tb/verilator/ctrl_service_budget'))
import record_classes as rc  # noqa: E402

legs, arm, stated = rc.synthetic()
at = lambda point: stated  # noqa: E731
base, _ = rc.findings(legs, arm, at)
print('synthetic pass findings:', base)
# arm B: SET_NAME 0, SET_CONFIGURATION 10 (answered), SET_STREAM_INFO 19, then a 40,000-cycle record at 30 ms whose
# SET_CONFIGURATION response is committed at 30.6 ms, after the next record (ADD, 30.5 ms) starts
legs[1].groups['aecp-fanout'] = rc.fanout(
    [(0, 33_000), (10, 28_000), (19, 20_000), (30, 40_000), (30.5, 15_000)],
    [(0.1, 0x10, 0), (10.4, 0x06, 0), (19.1, 0x0E, 0), (30.6, 0x06, 0), (30.7, 0x2B, 0)])
r = legs[1].groups['aecp-fanout'][3]
print('the 40,000-cycle record named:', r.command, r.status)
found, reported = rc.findings(legs, arm, at)
print('held findings:', found)
print('reported lines naming it:', [x for x in reported if '40,000' in x or '420' in x])
print('VERDICT:', 'held (refused)' if found else 'not held: reported only')
