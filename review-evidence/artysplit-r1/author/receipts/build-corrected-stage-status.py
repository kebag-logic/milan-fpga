"""Keep the author handoff current during final grading, documentation and routing."""
import datetime,json,re,shutil,subprocess,sys
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
p=Path('<home-path>/milan-fpga-management/2026-09-23/artysplit-a829/round4/HANDOFF-r4.md')
phase=sys.argv[1]
def read(path,default=None):
 try:return json.loads(path.read_text())
 except (FileNotFoundError,json.JSONDecodeError):return default
alerts=[]
if phase=='qualification':
 rows=read(r/'final-census/qualification-commands.json',[])
 done=read(r/'final-census/qualification.json')
 failures=[x['name'] for x in rows if x['returncode']]
 summary=f'All 145 native cases passed; final service grading has completed {len(rows)}/13 command checks'
 if done:summary+='; qualification '+done['status']
 alerts+=failures
elif phase=='docs':
 rows=read(r/'docs-after-service/results.json',[])
 done=read(r/'final-service-documentation.json')
 failures=[str(x['command']) for x in rows if x['rc']]
 summary=f'Complete service qualification passed; final documentation gates {len(rows)}/11 complete'
 if done:summary+='; documentation '+done['status']
 alerts+=failures
elif phase=='routes':
 rows=[read(path) for path in (r/'images').glob('*.result.json')]
 rows=[x for x in rows if x]
 done=read(r/'images/results.json')
 summary=f'Service qualification and documentation passed; {len(rows)}/3 routing attempts completed'
 summary+='; '+', '.join(x['directive']+': '+str(x['rc']) for x in rows) if rows else ''
 alerts += [x['directive']+' build exited '+str(x['rc']) for x in rows if x['rc']]
else:raise SystemExit('Unknown phase')
scratch=int(subprocess.check_output(['du','-s','-B1','$VALIDATION_STORAGE/artysplit-a829'],text=True,timeout=30).split()[0])
free=shutil.disk_usage(r).free
if scratch>=28_000_000_000:alerts.append('Scratch is approaching the 30 GB cap')
if free<10_000_000_000:alerts.append('Shared filesystem free space is below 10 GB')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
state=dict(time=now,phase=phase,summary=summary,completed=len(rows),done=bool(done),
           alerts=alerts,scratch_bytes=scratch,disk_free_bytes=free)
(r/(phase+'-live-status.json')).write_text(json.dumps(state,indent=2)+'\n')
text=p.read_text()
text=re.sub(r'^Status: .*$',lambda _:'Status: IN PROGRESS. '+summary+'.',text,count=1,flags=re.M)
text=re.sub(r'^\[A829\] #878 round 4, updated .*$',lambda _:'[A829] #878 round 4, updated '+now+'.',text,flags=re.M)
text=re.sub(r'^Live foreground-gate status: .*$',lambda _:'Live foreground-gate status: '+summary+'.',text,flags=re.M)
p.write_text(text)
print(json.dumps(state))
