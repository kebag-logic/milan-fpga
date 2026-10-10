"""Render per-bind counters and first-header timestamp distributions.

Lane B13's startup_report.py (sha256 in ORIGIN-B13.sha256) with B14's raw path and capture names.
"""
import collections,csv,json,statistics,sys
from pathlib import Path
from decode_capture import analyze
out=Path(sys.argv[1]);raw=Path('/tmp/608-b14/raw/item4');rows=[];headers=[]
for path in sorted(out.glob('start-[0-9][0-9][0-9].json')):
 tag=path.stem;data=json.loads(path.read_text());target=out/(tag+'-wire.json')
 if target.exists():wire=json.loads(target.read_text())
 else:
  wire=analyze([raw/f'608-b14-{tag}-plain.pcap',raw/f'608-b14-{tag}-vlan.pcap']);txt=json.dumps(wire,indent=2)+'\n';assert len(txt.encode())<200000;target.write_text(txt)
 stream=[s for s in wire['streams'] if s['role']=='dut' and s['subtype']==2]
 assert len(stream)==1
 s=stream[0];assert len(s['first'])==10
 row=dict(cycle=tag,result=data['result']['result'],early=data['early'],late=data['late'],packets=s['count'],sequence_gaps=s['gaps'],first_sequence=s['first'][0]['sequence'],first_step_ns=s['first_step_ns'],steady_period_ns=s['steady_period_ns'],first_offset_from_steady_ns=s['first_offset_from_steady_ns'],tv=''.join(str(x['tv']) for x in s['first']),tu=''.join(str(x['tu']) for x in s['first']),mr=''.join(str(x['mr']) for x in s['first']))
 rows.append(row)
 for i,x in enumerate(s['first']):headers.append(dict(cycle=tag,pdu=i+1,sequence=x['sequence'],tv=x['tv'],tu=x['tu'],mr=x['mr'],avtp_timestamp=x['avtp_timestamp'],relative_to_tenth_pdu_trend_ns=x['relative_to_tenth_pdu_trend_ns'],raw_header=x['header']))
for name,data in [('startup-cycles.csv',rows),('startup-first-ten.csv',headers)]:
 with (out/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 assert (out/name).stat().st_size<200000
steps=[r['first_step_ns'] for r in rows];offsets=[r['first_offset_from_steady_ns'] for r in rows]
summary=dict(cycles=len(rows),successful_cycles=sum(r['result']=='OK' for r in rows),early_positive_cycles=sum(r['early']>0 for r in rows),late_positive_cycles=sum(r['late']>0 for r in rows),early_total=sum(r['early'] for r in rows),late_total=sum(r['late'] for r in rows),sequence_gaps=sum(r['sequence_gaps'] for r in rows),first_step_ns=dict(min=min(steps),median=statistics.median(steps),max=max(steps),distinct=sorted(set(steps)),histogram=dict(sorted(collections.Counter(steps).items()))),first_offset_from_steady_ns=dict(min=min(offsets),median=statistics.median(offsets),max=max(offsets)),all_first_ten_tv_one=all(r['tv']=='1'*10 for r in rows),all_first_ten_tu_zero=all(r['tu']=='0'*10 for r in rows),absolute_gptp_correlation='NOT RUN')
(out/'startup-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
