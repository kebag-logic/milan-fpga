"""Merge maxima from own-clock censuses; never turn partial evidence into qualification."""
import hashlib,json,sys
from pathlib import Path
out=Path(sys.argv[1]); costs={}; rounds={}; groups=set(); sources=[]
for name in sys.argv[2:]:
 p=Path(name); raw=p.read_bytes(); x=json.loads(raw)
 assert x['cpu_hz']==80_000_000 and x['shape']==[1,1,2]
 sources.append(dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),status=x['status']))
 groups.update(x['groups'])
 for k,v in x['costs'].items():
  if v['cycles']>costs.get(k,{}).get('cycles',-1):costs[k]=v
 for k,v in x['rounds'].items():
  if v['cycles']>rounds.get(k,{}).get('cycles',-1):rounds[k]=v
result=dict(status='PARTIAL MEASUREMENT MAXIMA; NOT QUALIFICATION',cpu_hz=80_000_000,shape=[1,1,2],
            groups=sorted(groups),costs=costs,rounds=rounds,sources=sources)
out.write_text(json.dumps(result,indent=2)+'\n')
print(len(groups),'groups',len(costs),'costs; partial only')
