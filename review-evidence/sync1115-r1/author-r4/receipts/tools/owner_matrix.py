#!/usr/bin/env python3
"""Supplemental owner matrix at the supplied checkout; no product or repository edits."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(sys.argv[1])/'tb/verilator/ctrl_service_budget'))
import selftest
import selftest_leaveall as checks
import mrpdu_grade

grade=checks.harness(selftest.synthetic,100_000_000,50_000_000,selftest.tx_record)
la,join=checks.LA,checks.JOIN
count=0
for interface in (0,1):
 for app in (checks.MSRP,checks.MVRP):
  other=checks.MVRP if app==checks.MSRP else checks.MSRP
  who=f'if{interface} '+mrpdu_grade.APPLICATIONS[app]
  peer=f'if{interface} '+mrpdu_grade.APPLICATIONS[other]
  first=((1000,app,False,interface),(1040,other,False,interface))
  timers=((1050,la,who),(1180,join,who),(1190,la,peer),(1220,join,peer))
  rows,held=grade(first+((1181,app,False,interface),(1221,other,True,interface),(1371,app,True,interface)),timers+((1370,join,who),))
  assert checks.by(held)=={'sent':1,'skipped':1} and [x['who'] for x in held['leave_all']['failing']]==[who]
  assert checks.row(rows,'leaveall',interface)==191.0
  assert '1180.000 ms' in checks.named(case=held)[0]
  print('PASS',who,'overlap skipped at own 1180 ms opportunity; 191 ms')
  rows,held=grade(first+((1181,app,True,interface),(1221,other,True,interface)),timers)
  assert checks.by(held)=={'sent':2} and not held['leave_all']['failing']
  print('PASS',who,'clean overlap')
  rows,held=grade(((900,other,False,interface),(1000,app,False,interface),(1101,other,True,interface),(1181,app,True,interface)),((1050,la,who),(1100,la,peer),(1180,join,who)))
  assert checks.by(held)=={'sent':2} and not held['leave_all']['failing']
  print('PASS',who,'legitimately reordered clean output')
  rows,held=grade(first+((1221,other,True,interface),(1240,app,True,interface)),timers)
  assert checks.by(held)=={'sent':1,'late':1} and [x['who'] for x in held['leave_all']['failing']]==[who]
  print('PASS',who,'late output named for its actual owner')
  rows,held=grade(first+((1221,other,True,interface),),timers,ordinary=(1500,))
  assert checks.by(held)=={'sent':1,'absent':1} and [x['who'] for x in held['leave_all']['failing']]==[who]
  print('PASS',who,'absent output not answered by the other application')
  rows,held=grade(((1000,app,False,interface),(1000,app,False,1-interface),(1181,app,True,1-interface),(1183,app,False,interface),(1373,app,True,interface)),((1050,la,who),(1180,join,who),(1370,join,who)))
  assert checks.by(held)=={'skipped':1} and [x['who'] for x in held['leave_all']['failing']]==[who]
  print('PASS',who,'same application on the other interface cannot satisfy expiry')
  count+=6
print(f'{count} controls; 0 failures')
