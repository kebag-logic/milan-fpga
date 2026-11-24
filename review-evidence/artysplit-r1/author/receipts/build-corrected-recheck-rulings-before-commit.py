"""Read the manager's public rulings again before the final source commit."""
import datetime,json,subprocess,sys
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
command=['gh','issue','view','878','-R','kebag-logic/milan-fpga','--json','number,title,state,body,comments,url']
result=subprocess.run(command,check=True,stdout=subprocess.PIPE,text=True,timeout=120)
issue=json.loads(result.stdout)
comments=[c for c in issue['comments'] if c['body'].lstrip().startswith('[A10]')]
assert len(comments)>=3
record=dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=command,issue=issue,
            latest_manager_comments=comments[-3:])
(r/'manager-rulings-before-commit.json').write_text(json.dumps(record,indent=2)+'\n')
sys.path.insert(0,'<home-path>/milan-fpga-management/2026-09-23');import privacy
for c in comments[-3:]:
 print(c.get('url',c.get('id','')))
 print(privacy.scrub_redact(c['body'].encode()).decode())
 print()
