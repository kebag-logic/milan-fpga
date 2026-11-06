#!/usr/bin/env python3
"""The one input the group term decides: the measured row is acmp-disc's, the refusal hooks-disc-aging's.

usage: group_scenario_demo.py <dir holding hooks_selftest.py>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import hooks_selftest as t  # noqa: E402

lost = dict(probe='hooks-disc-aging.tmr_no_adp.if1', path=['acmp.tmr_no_adp', 1], status='no start', reason='late')
again = dict(t.row('disc', 2.0, probe='acmp.tmr_no_adp.if1'), path=['acmp.tmr_no_adp', 1], interface=1,
             status='measured')
got = t.graded_with({'acmp-disc': [again], 'hooks-disc-aging': [lost]})
print('refusals', got['refusals'])
print('superseded', got['superseded'])
