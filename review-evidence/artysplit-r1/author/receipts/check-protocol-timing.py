"""Read protocol timing from the monitors' completed group grades; no simulation."""
import datetime,json,hashlib
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4');records={}
for index,grades,logs in [('watch-completed.json','watch','results'),('watch-extra.json','watch-extra','extra-results')]:
 for row in json.loads((r/index).read_text()):
  path=r/row['arm']/grades/(row['group']+'.json')
  trace=r/row['arm']/logs/(row['group']+'.log')
  assert hashlib.sha256(trace.read_bytes()).hexdigest()==row['trace_sha256']
  data=json.loads(path.read_text());joins=data['passes'].get('joins',{})
  found=joins.get('over',[])+joins.get('failing',[])+joins.get('leave_all',{}).get('failing',[])
  records[(row['arm'],row['group'],row['trace_sha256'])]=dict(arm=row['arm'],group=row['group'],
                 trace_sha256=row['trace_sha256'],grade=str(path),findings=found)
result=dict(status='PASS' if not any(x['findings'] for x in records.values()) else 'FAIL',
            completed_graded_groups=len(records),records=list(records.values()),
            checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
(r/'protocol-timing-completed.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],result['completed_graded_groups'],'completed unique traces')
raise SystemExit(result['status']!='PASS')
