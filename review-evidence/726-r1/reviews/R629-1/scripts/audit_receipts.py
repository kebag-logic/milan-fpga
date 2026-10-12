#!/usr/bin/env python3
"""Check regenerated packet windows and all named mutation/omission receipts."""
import json,re,sys
from pathlib import Path
p=Path(sys.argv[1]);r=p/"receipts";out={}
for shape in (1,8):
 t=(r/f"clean-{shape}-clean.run.log").read_text()
 rows=[s.split(',') for s in t.splitlines() if re.match(rf"^{shape},[56],",s)]
 graded=[x for x in rows if 2<=int(x[4])<=4]
 assert len(graded)==12*(shape+1) and all(x[5]=='1' for x in graded)
 out[f"shape-{shape}"]={"recorded_windows":len(rows),"graded_windows":len(graded),"min_gap_ms":min(float(x[6]) for x in rows),"max_gap_ms":max(float(x[7]) for x in rows),"max_service_ms":max(int(s.split(',')[2])/1000 for s in t.splitlines() if s.startswith('SERVICE,'))}
groups={'tx-interval':'TX','rx-interval':'RX','tx-reset':'TX_RESET','aaf-reset':'RX_RESET','crf-reset':'RX_RESET','rx-saturation':'RX','late':'CADENCE','rate':'RATE'}
for name,group in groups.items():
 t=(r/f"plants-1-{name}.run.log").read_text();f=[s for s in t.splitlines() if '[FAIL]' in s]
 assert f and all(f'[726 {group}]' in s for s in f)
 e=(r/f"plants-1-{name}.escape.log").read_text();assert '[FAIL]' not in e and 'RESULT: PASS' in e
 assert (r/f"plants-1-{name}.rc").read_text().strip()=='0'
 out['plant-'+name]={"failures":len(f),"group":group,"escape":"PASS"}
for name,group in {'late':'CADENCE','rate':'RATE'}.items():
 t=(r/f"f5-1-{name}.run.log").read_text();f=[s for s in t.splitlines() if '[FAIL] Mailbox.' in s]
 assert f and all(f'[F5 {group}]' in s for s in f)
 e=(r/f"f5-1-{name}.escape.log").read_text();assert '[FAIL] Mailbox.' not in e
 assert (r/f"f5-1-{name}.rc").read_text().strip()=='0'
 out['firmware-'+name]={"failures":len(f),"group":group,"escape":"PASS"}
print(json.dumps(out,indent=2))
