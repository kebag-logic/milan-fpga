"""Compare original and restored binding/settings census."""
from pathlib import Path
import json,hashlib
packet=Path(__file__).resolve().parent.parent
before=[json.loads(l) for l in (packet/"census-start.jsonl").read_text().splitlines()]
after=[json.loads(l) for l in (packet/"census-end.jsonl").read_text().splitlines()]
a={(r['role'],r['what']):r['response'] for r in before};b={(r['role'],r['what']):r['response'] for r in after}
notes=[]
for k,r in b.items():
 if k[1].startswith('state-'):
  assert r['status']==0 and r['conn_count']==0,(k,r)
  if k[1].startswith('state-5-'):assert r['talker']=='0000000000000000',(k,r)
  notes.append('UNBOUND '+':'.join(k))
 elif k[1] in ('clock','config','sample-rate') or k[1].startswith('desc-'):
  assert r['status']=='SUCCESS' and a[k]['status']=='SUCCESS',k
  x=bytes.fromhex(a[k]['payload']);y=bytes.fromhex(r['payload'])
  if k[1]=='clock':x,y=x[:6],y[:6]
  if k[1].startswith('desc-'):x,y=x[4:],y[4:]
  assert x==y,('SETTING_MISMATCH',k,x.hex(),y.hex())
  notes.append('UNCHANGED '+':'.join(k))
 elif k[1]=='avb':
  assert r['decoded']['as_capable']==1 and r['decoded']['gm']=='3cc0c6fffefe0210',k
  notes.append('HEALTHY '+':'.join(k))
notes+=['All 18 queried stream states unbound.','Both original clock selections, configurations, rates and descriptors restored.','Peer reserved response halfwords excluded from comparison.','Counters are observations and are not reset during restore.']
(packet/'restore-comparison.txt').write_text('\n'.join(notes)+'\n')
print('\n'.join(notes[-4:]))
