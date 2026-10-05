"""Compare effective bindings, formats, maps and source selections."""
import hashlib,json,sys
from pathlib import Path
RAW=Path('/tmp/653-b12/raw')
def read(name):return [json.loads(x) for x in (RAW/name).read_text().splitlines() if x.startswith('{')]
def extract(tag):
 out={}
 for name in ('census','peer-descs','dut-descs'):
  for r in read(f'{name}-{tag}.jsonl'):
   what=r.get('what','');role=r.get('role','dut' if '-dut-' in what else 'peer');key=role+':'+what
   if what.startswith(('rx-state-','tx-state-')):
    val={'status':r['status'],'connections':r['conn_count']}
    if r['conn_count']:val.update({k:r[k] for k in ('talker','listener','talker_uid','listener_uid','stream_id')})
    out[('bindings',key)]=val
   elif r.get('cmd')=='GET_STREAM_FORMAT':out[('formats',key)]={'status':r['status'],'format':r['payload'][8:24]}
   elif r.get('cmd')=='GET_CLOCK_SOURCE':out[('clocks',key)]={'status':r['status'],'source':r['payload'][8:12]}
   elif r.get('cmd')=='GET_AUDIO_MAP' or (r.get('cmd')=='READ_DESCRIPTOR' and '-0x0014-' in what):
    out[('maps',key)]={'status':r['status'],'payload':r.get('payload')}
 return out
s,e=extract('start'),extract('end');rows=[];ok=True
for role in ('dut','peer'):
 for cat in ('bindings','formats','maps','clocks'):
  ss={k[1]:v for k,v in s.items() if k[0]==cat and k[1].startswith(role+':')};ee={k[1]:v for k,v in e.items() if k[0]==cat and k[1].startswith(role+':')}
  equal=ss==ee;ok=ok and equal
  rows.append(dict(role=role,category=cat,observations=len(ss),equal=equal,start_sha256=hashlib.sha256(json.dumps(ss,sort_keys=True).encode()).hexdigest(),end_sha256=hashlib.sha256(json.dumps(ee,sort_keys=True).encode()).hexdigest(),different_keys=sorted(k for k in ss.keys()|ee.keys() if ss.get(k)!=ee.get(k))))
print(json.dumps(dict(pass_restore=ok,rows=rows),indent=2))
sys.exit(0 if ok else 1)
