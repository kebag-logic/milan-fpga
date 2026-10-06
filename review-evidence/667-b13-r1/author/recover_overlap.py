"""Locate complete overlapping wire evidence for segment-local gaps."""
import json,sys
from pathlib import Path
from decode_capture import records,header
out=Path(sys.argv[1]);raw=Path('/tmp/667-b13/raw');result=[]
for f in sorted(out.glob('soak-*-wire.json')):
 data=json.loads(f.read_text());index=int(f.name.split('-')[1])
 for stream in data['streams']:
  for gap in stream['gap_examples']:
   b,a=gap['before'],gap['after'];recovered=None
   for neighbor in (index-1,index+1):
    name=b['capture'].replace(f'soak-{index:03d}',f'soak-{neighbor:03d}');path=raw/name
    if not path.exists():continue
    rs=[]
    for n,t,port,avtp in records(path):
     if t>a['tap_ns']:break
     if t<b['tap_ns'] or port!=b['port'] or avtp[0]!=stream['subtype'] or int.from_bytes(avtp[10:12],'big')!=stream['stream_unique_id']:continue
     rs.append(dict(record=n,tap_ns=t,**header(avtp)))
    if len(rs)>1 and rs[0]['tap_ns']==b['tap_ns'] and rs[-1]['tap_ns']==a['tap_ns'] and rs[0]['sequence']==b['sequence'] and rs[-1]['sequence']==a['sequence'] and all(y['sequence']==(x['sequence']+1)%256 for x,y in zip(rs,rs[1:])):
     recovered=dict(capture=name,packets=rs);break
   result.append(dict(segment=f.stem,role=stream['role'],subtype=stream['subtype'],before=b,after=a,recovered=recovered))
summary=dict(segment_gaps=len(result),recovered_gaps=sum(r['recovered'] is not None for r in result),unrecovered_gaps=sum(r['recovered'] is None for r in result),gaps=result)
text=json.dumps(summary,indent=2)+'\n';assert len(text.encode())<200000;(out/'overlap-recovery.json').write_text(text)
print(json.dumps({k:v for k,v in summary.items() if k!='gaps'}))
