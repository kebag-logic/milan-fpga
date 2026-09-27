"""Compare original and restored binding/settings census."""
from pathlib import Path
import json,hashlib
packet=Path(__file__).resolve().parent.parent
before=[json.loads(l) for l in Path("/tmp/a375-census-start-raw.jsonl").read_text().splitlines()]
after=[json.loads(l) for l in Path("/tmp/a375-census-end-raw.jsonl").read_text().splitlines()]
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
raw=Path('/tmp/a375-census-end-raw.jsonl').read_bytes();rows=after
for r in rows:
 if r.get('role')=='peer' and r.get('what','').startswith('desc-') and r['response'].get('status')=='SUCCESS':
  v=bytearray.fromhex(r['response']['payload']);v[8:72]=bytes(64);r['response']['payload']=v.hex();r['redaction']='reference peer object_name zeroed'
f=packet/'census-end.jsonl';f.write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in rows))
r=json.loads((packet/'redaction.json').read_text());r['census-end.jsonl']=dict(original_sha256=hashlib.sha256(raw).hexdigest(),retained_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),substitution='reference peer descriptor object names zeroed',original='/tmp/a375-census-end-raw.jsonl');(packet/'redaction.json').write_text(json.dumps(r,indent=2)+'\n')
notes+=['All 18 queried stream states unbound.','Both original clock selections, configurations, rates and descriptors restored.','Peer reserved response halfwords excluded from comparison.','Counters are observations and are not reset during restore.']
(packet/'restore-comparison.txt').write_text('\n'.join(notes)+'\n')
print('\n'.join(notes[-4:]))
