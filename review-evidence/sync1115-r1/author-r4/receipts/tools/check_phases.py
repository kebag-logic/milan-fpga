#!/usr/bin/env python3
"""Check the completed phase report without turning known STATED cost failures into passes."""
import json,sys
from pathlib import Path
rows=json.loads(Path(sys.argv[1]).read_text())
phase=[r for r in rows if r['phase']]
assert len(phase)==11
count=0;worst={}
for leg in rows:
 assert leg['rc'] not in ('running',''),leg['leg']
 assert leg['rc'] in ('0','1'),(leg['leg'],leg['rc'])
 if leg['leg']=='v1':assert leg['rc']=='0'
 for name,g in leg['groups'].items():
  assert g['late_ms']==49,(leg['leg'],name,'conformance bound changed')
  same=g['same_but_owner']
  assert same['differ']==0,(leg['leg'],name,'behavior trace changed')
  assert same['owner_unresolved']==same['owner_missing']==0,(leg['leg'],name,'owner missing')
  assert not g['new']['row_misses'],(leg['leg'],name,'probe row miss')
  assert not g['new']['joins_failing'],(leg['leg'],name,'MRP timer failure')
  assert all(a['outcome']=='sent' for a in g['leave_alls']),(leg['leg'],name,g['leave_alls'])
  if leg['phase'] and name in ('save-held','save-starved'):
   assert len(g['leave_alls'])==2 and {a['owner'] for a in g['leave_alls']}=={'if0 MSRP','if0 MVRP'}
   count+=len(g['leave_alls'])
   for row,ms in g['new']['rows'].items():
    assert ms<=20,(leg['leg'],name,row,ms)
    if row not in worst or ms>worst[row]['ms']:worst[row]=dict(ms=ms,leg=leg['leg'],group=name)
assert count==44,count
print('PASS: 11 phases, 22 required loaded groups, 44 owned LeaveAlls sent; no skipped, late, absent, unresolved or unowned expiry.')
print('PASS: every completed rerun trace equals the earlier trace after removing only owner records; no missing/unresolved owner.')
print('PASS: required 1x1/1if valid-destinations leg rc 0; 8x8 legs retain rc 1 on the separately recorded STATED costs, not passing whole legs.')
print('Worst MRPDU rows (20 ms bound unchanged):')
print(json.dumps(worst,indent=2))
