"""Report foreground simulation progress without claiming partial runs as passes."""
from pathlib import Path
import json
import re
import sys
pending = "--pending" in sys.argv
for p in sorted(Path('/tmp').glob('a385-final3-capture-8x8*')):
 if p.is_dir() and not (pending and (p/"measurement.json").exists()):
  rows=re.findall(r'CAPTURE index=(\d+).*?sys_cycles=(\d+)',(p/'capture.log').read_text())
  print(p.name, 'captures',len(rows),'max ms',max((int(c)/100000 for _,c in rows),default=0),'complete',(p/'measurement.json').exists())
for plan in ('all','uart-paced','queued-input','queued-short','device-wait'):
 p=Path('/tmp/a385-final3-service-8x8'+('' if plan=='all' else '-'+plan))
 q=next(p.glob('service-*.log'))
 if q.with_suffix('.json').exists():
  if pending: continue
  d=json.loads(q.with_suffix('.json').read_text())
  print(plan,'COMPLETE',d.get('service_findings'),'HB',d.get('heartbeat_max_gap_ms'),'PHY',d.get('phy'))
 else:
  raw=q.read_text();e=re.findall(r'EVENT cycle=(\d+) kind=(\S+)',raw)
  c=re.findall(r'EVENT cycle=\d+ kind=command_(start|end) index=(\d+)',raw)
  print(plan,'sim ms',round(int(e[-1][0])/100000) if e else 0,'command',c[-1] if c else '-')
