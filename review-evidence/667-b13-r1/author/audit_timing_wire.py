"""Audit retained DUT advertisements and interface timing responses."""
import hashlib,json,sys
from pathlib import Path
from decode_capture import records
p=Path(sys.argv[1]);artifacts=[json.loads(x) for x in (p/'capture-artifacts.jsonl').read_text().splitlines()]
base=next(json.loads(x)['gm_fingerprint'] for x in (p/'timing-prebind.jsonl').read_text().splitlines() if json.loads(x)['command']=='GET_AVB_INFO' and json.loads(x)['role']=='dut')
rows=[];changes=[]
for item in artifacts:
 path=Path(item['file'])
 if not path.name.startswith('667-b13-soak-') or not path.name.endswith('-plain.pcap'):continue
 counts={'ADP':0,'GET_AVB_INFO':0};first=None;last=None
 for n,t,port,a in records(path):
  if port!=3 or len(a)<48:continue
  kind=None;capable=None
  if a[0]==0xfa and a[1]&15==0:kind='ADP';gm=a[40:48]
  elif a[0]==0xfb and a[1]&15==1 and int.from_bytes(a[22:24],'big')&32767==0x27 and a[2]>>3==0:
   kind='GET_AVB_INFO';gm=a[28:36];capable=bool(a[41]&1)
  if kind is None:continue
  counts[kind]+=1
  if first is None:first=t
  last=t
  if hashlib.sha256(gm).hexdigest()!=base or capable is False:changes.append({'capture':path.name,'record':n,'tap_ns':t,'kind':kind,'gm_changed':hashlib.sha256(gm).hexdigest()!=base,'as_capable':capable})
 rows.append({'capture':path.name,'counts':counts,'first_tap_ns':first,'last_tap_ns':last})
x={'captures':rows,'changes':changes};txt=json.dumps(x,indent=2)+'\n';assert len(txt.encode())<180000;(p/'timing-wire-audit.json').write_text(txt)
print(json.dumps({'captures':len(rows),'ADP':sum(r['counts']['ADP'] for r in rows),'GET_AVB_INFO':sum(r['counts']['GET_AVB_INFO'] for r in rows),'changes':changes}))
raise SystemExit(1 if changes else 0)
