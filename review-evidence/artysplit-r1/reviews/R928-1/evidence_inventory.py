#!/usr/bin/env python3
"""Check primary-receipt presence in the published Git tree, not just extraction.
Usage: evidence_inventory.py SOURCE
"""
from pathlib import PurePosixPath
import collections, subprocess, sys
commit='0723eba4bd2175f36b26fa69e1b0b898740853af'
prefix='review-evidence/artysplit-r1/author/receipts/'
paths=subprocess.check_output(['git','-C',sys.argv[1],'ls-tree','-r','--name-only',commit,prefix],text=True).splitlines()
print('Evidence commit',commit)
print('Receipt suffix counts',dict(sorted(collections.Counter(PurePosixPath(x).suffix for x in paths).items())))
for directive in ['ExtraPostPlacementOpt','AltSpreadLogic_high','ExtraTimingOpt']:
 for corner in ['Slow_0C','Slow_85C','Fast_0C','Fast_85C']:
  name=f'build-corrected-images-{directive}-digilent_arty_signoff_{corner}_timing.rpt'
  print('PRESENT' if prefix+name in paths else 'ABSENT',name)
print('Native .log or compressed log files:',sum(x.endswith(('.log','.log.gz')) for x in paths))
print('Receipt index:', 'PRESENT' if prefix+'INDEX.md' in paths else 'ABSENT')
print('The published .txt census files are stimulus inputs, not execution traces.')
print('Derived JSON grades, check_timing and utilization reports are present; they are not the missing corner timing paths or native event traces.')
