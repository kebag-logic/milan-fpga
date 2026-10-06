"""Combine bounded segment receipts without double-counting overlap."""
import json,re,sys
from pathlib import Path
out=Path(sys.argv[1]);streams={};issues=[];segments=sorted(out.glob('soak-*-wire.json'))
for path in segments:
 data=json.loads(path.read_text())
 if data['nonmonotonic_records']:issues.append({'cycle':path.stem,'nonmonotonic_records':data['nonmonotonic_records']})
 for r in data['streams']:
  key=(r['role'],r['subtype'],r['stream_unique_id'])
  first,last=r['first'][0],r['last'][-1]
  s=streams.setdefault(key,dict(role=r['role'],subtype=r['subtype'],stream_unique_id=r['stream_unique_id'],segments=0,first_tap_ns=first['tap_ns'],last_tap_ns=first['tap_ns'],packet_observations=0,sequence_gaps=0,mr_toggles=0,tu_toggles=0,uncovered_boundaries=[]))
  if s['segments'] and first['tap_ns']>s['last_tap_ns']:
   s['uncovered_boundaries'].append({'cycle':path.stem,'ns':first['tap_ns']-s['last_tap_ns']})
  s['segments']+=1;s['last_tap_ns']=max(s['last_tap_ns'],last['tap_ns']);s['packet_observations']+=r['count'];s['sequence_gaps']+=r['gaps'];s['mr_toggles']+=len(r['mr_toggles']);s['tu_toggles']+=len(r['tu_toggles'])
  s['covered_span_s']=(s['last_tap_ns']-s['first_tap_ns'])/1e9
captures=[]
for path in sorted(out.glob('667-b13-soak-*.pcap.json')):
 r=json.loads(path.read_text());d=[int(m.group(1)) for line in r['summary'] if (m:=re.search(r'(\d+) packets dropped by kernel',line))]
 captures.append({'capture':r['capture'],'rc':r['rc'],'kernel_dropped':d[0] if len(d)==1 else None})
 if len(d)!=1 or d[0] or r['rc'] not in (0,130):issues.append(captures[-1])
result={'decoded_segments':len(segments),'streams':list(streams.values()),'capture_receipts':len(captures),'kernel_drop_total':sum(r['kernel_dropped'] or 0 for r in captures),'issues':issues,'count_definition':'Packet observations include overlapping segments; they are not unique packet totals.'}
(out/'soak-wire-summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
