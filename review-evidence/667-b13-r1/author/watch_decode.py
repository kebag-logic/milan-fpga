"""Decode completed rolling captures while their foreground run continues."""
import json,time,sys
from pathlib import Path
from decode_capture import analyze
out=Path(sys.argv[1]);raw=Path('/tmp/667-b13/raw');done=set()
end=time.monotonic()+7500
while time.monotonic()<end:
 index=out/'capture-artifacts.jsonl'
 names={Path(json.loads(x)['file']).name for x in index.read_text().splitlines()} if index.exists() else set()
 for n in sorted(names):
  if not n.endswith('-plain.pcap') or '-soak-' not in n:continue
  tag=n.removeprefix('667-b13-').removesuffix('-plain.pcap')
  vn=n.replace('-plain.pcap','-vlan.pcap')
  if vn not in names or tag in done:continue
  target=out/(tag+'-wire.json')
  if target.exists():x=json.loads(target.read_text())
  else:
   x=analyze([raw/n,raw/vn]);txt=json.dumps(x,indent=2)+'\n'
   if len(txt.encode())>180000:
    controls=x.pop('counter_wire');x['counter_wire_files']=[]
    for i in range(0,len(controls),100):
     part=f'{tag}-counters-{i//100:03d}.json';payload=json.dumps(controls[i:i+100],indent=2)+'\n';assert len(payload.encode())<180000;(out/part).write_text(payload);x['counter_wire_files'].append(part)
    txt=json.dumps(x,indent=2)+'\n'
   assert len(txt.encode())<180000;target.write_text(txt)
  summary={'cycle':tag,'streams':[{'role':r['role'],'subtype':r['subtype'],'stream_unique_id':r['stream_unique_id'],'count':r['count'],'gaps':r['gaps'],'mr_toggles':len(r['mr_toggles']),'tu_toggles':len(r['tu_toggles'])} for r in x['streams']]}
  with (out/'wire-index.jsonl').open('a') as f:f.write(json.dumps(summary)+'\n')
  print(json.dumps(summary),flush=True);done.add(tag)
 events=[json.loads(x) for x in (out/'run-events.jsonl').read_text().splitlines()]
 if any(x.get('event')=='capture_cleanup_complete' for x in events):break
 time.sleep(2)
print('Completed capture decoder',flush=True)
