#!/usr/bin/env python3
"""R784-3: what the surviving source mutant sup-any-path does to a realistic grade.

usage: supersede_consequence.py HARNESS_DIR
A hooks-disc-aging log whose ENTITY_AVAILABLE row on interface 1 was measured but whose TMR_NO_ADP row was not, with
the earlier acmp-disc probe of that path refused as well. The harness must report both as refusals: no row of that
path on that interface exists.
"""
import sys, tempfile
from pathlib import Path
from unittest.mock import patch
h = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(h))
import hooks_selftest as t  # noqa: E402
import run  # noqa: E402
lost = dict(probe='acmp.tmr_no_adp.if1', path=['acmp.tmr_no_adp', 1], status='no start', reason='late')
own = dict(probe='hooks-disc-aging.tmr_no_adp.if1', path=['acmp.tmr_no_adp', 1], status='no start', reason='late')
avail = dict(t.row('disc', 2.0, probe='hooks-disc-aging.available.if1'), path=['acmp.entity_available', 1],
             interface=1, status='measured')
got = t.graded_with({'acmp-disc': [lost], 'hooks-disc-aging': [avail, own]})
print('refusals', len(got['refusals']), [x.split(':')[0] for x in got['refusals']])
print('superseded', len(got['superseded']), [x.split(':')[0] for x in got['superseded']])
print('rows', [(r['probe'], r['path'], r['interface']) for r in got['rows']])
