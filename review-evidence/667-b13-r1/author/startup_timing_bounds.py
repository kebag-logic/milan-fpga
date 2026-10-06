"""Correlate startup counters using only the controller's clock."""
import csv,json,sys
from datetime import datetime,timezone
from pathlib import Path
out=Path(sys.argv[1]);rows=[];formats=[];holds=[]
for f in sorted(out.glob('start-[0-9][0-9][0-9].json')):
 x=json.loads(f.read_text());bu={r['ev']:r for r in x['bind_unbind']};bind,unbind=bu['bind'],bu['unbind'];assert bind['status'].startswith('Success') and unbind['status'].startswith('Success')
 holds.append((unbind['t_cmd']-bind['t'])/1000)
 for fmt in x['formats']:
  assert fmt['ev']=='formats' and fmt['talker_status'].startswith('Success') and fmt['listener_status'].startswith('Success') and fmt['talker_format']==fmt['listener_format'];formats.append(fmt)
 for counter in ('EARLY','LATE'):
  observed=[r for r in x['polls'] if r['phase']!='pre-bind' and r['counters'].get(counter,0)]
  if not observed:continue
  first=observed[0];rows.append(dict(cycle=x['cycle'],counter=counter,value=first['counters'][counter],phase=first['phase'],first_response_utc=datetime.fromtimestamp(first['t_rsp']/1e6,timezone.utc).isoformat(),bind_command_to_response_ms=(first['t_rsp']-bind['t_cmd'])/1000,response_to_unbind_command_ms=(unbind['t_cmd']-first['t_rsp'])/1000))
with (out/'startup-counter-timing.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=dict(format_pairs_read=len(formats),all_formats_matched=True,hold_ms=dict(min=min(holds),max=max(holds)),counter_observations=rows)
(out/'startup-validation.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
