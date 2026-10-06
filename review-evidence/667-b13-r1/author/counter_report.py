"""Render every valid counter's initial, final, and modulo delta."""
import csv,json,sys
from pathlib import Path
from datetime import datetime,timezone
p=Path(sys.argv[1]);files=sorted(p.glob('counters-soak-*.jsonl'))
if not files:raise SystemExit('no soak observations')
def load(f):return {(r['role'],r['descriptor_type'],r['descriptor_index']):r for r in map(json.loads,f.read_text().splitlines())}
a,b=load(files[0]),load(files[-1]);assert set(a)==set(b)
names={9:['LINK_UP','LINK_DOWN','FRAMES_TX','FRAMES_RX','RX_CRC_ERROR','GPTP_GM_CHANGED'],36:['LOCKED','UNLOCKED'],5:['MEDIA_LOCKED','MEDIA_UNLOCKED','STREAM_INTERRUPTED','SEQ_NUM_MISMATCH','MEDIA_RESET','TIMESTAMP_UNCERTAIN','TIMESTAMP_VALID','TIMESTAMP_NOT_VALID','UNSUPPORTED_FORMAT','LATE_TIMESTAMP','EARLY_TIMESTAMP','FRAMES_RX','FRAMES_TX'],6:['STREAM_START','STREAM_STOP','MEDIA_RESET','TIMESTAMP_UNCERTAIN','FRAMES_TX']}
desc={0:'ENTITY',9:'AVB_INTERFACE',36:'CLOCK_DOMAIN',5:'STREAM_INPUT',6:'STREAM_OUTPUT'}
rows=[]
for k,x in a.items():
 y=b[k]
 if x['status']=='NOT_SUPPORTED':
  assert y['status']==x['status'];continue
 assert x['status']==y['status']=='SUCCESS';assert x['valid_mask']==y['valid_mask'];assert x['counters'].keys()==y['counters'].keys()
 for bit,s in x['counters'].items():
  n=int(bit);label=names[k[1]][n] if n<len(names.get(k[1],[])) else 'BIT_'+bit;e=y['counters'][bit]
  rows.append(dict(role=k[0],descriptor=desc[k[1]],index=k[2],counter=label,bit=n,start=s,end=e,delta=(e-s)%(1<<32)))
with (p/'counter-deltas.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={'start_file':files[0].name,'end_file':files[-1].name,'polls':len(files),'valid_counters':len(rows),'unsupported':[{'role':k[0],'descriptor':desc[k[1]],'index':k[2],'status':r['status']} for k,r in a.items() if r['status']!='SUCCESS']}
(p/'counter-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
