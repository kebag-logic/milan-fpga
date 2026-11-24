"""Run the remaining frozen-image calibration in the foreground, four slots."""
import concurrent.futures,datetime,fcntl,json,os,subprocess,sys
from pathlib import Path
root=Path.cwd();r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/refined')
assert root==Path('$LANES/arty-split')
prior=json.loads((r/'pipeline-results.json').read_text())
assert len(prior)==8 and not any(row['returncode'] for row in prior)
for path in Path('/proc').glob('[0-9]*/cmdline'):
 try:exe=path.read_bytes().split(b'\0')[0]
 except OSError:continue
 assert not (exe.startswith(b'$VALIDATION_STORAGE/artysplit-a829/') and exe.endswith(b'/native/Vsim')),exe
for number in range(4):
 with (r/'final-slots'/f'{number}.lock').open('a+') as handle:
  fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
  fcntl.flock(handle,fcntl.LOCK_UN)
env=dict(os.environ,PYTHONHASHSEED='0',PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(r/'work-tmp'))
def command(name,argv):
 with (r/(name+'.log')).open('w') as stream:
  p=subprocess.run(argv,cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=172800)
 record=dict(command=argv,returncode=p.returncode,log=str(r/(name+'.log')))
 (r/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
 print(name,p.returncode,flush=True)
 return record
closure=command('close-before-continuation-command',[sys.executable,'-B',str(r/'close-before-continuation.py')])
assert closure['returncode']==0
(r/'calibration-continuation-launch.json').write_text(json.dumps(dict(
 status='RUNNING CALIBRATION ONLY',time=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source_firmware_unchanged=True,scope='Remaining groups only; previous results preserved; fresh final qualification still required.'),indent=2)+'\n')
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 futures=[pool.submit(command,name,[sys.executable,'-B',str(r/script)]) for name,script in (
  ('calibration-continuation-command','continue-calibration.py'),
  ('watch-calibration-costs-command','watch-calibration-costs.py'))]
 records=[f.result() for f in concurrent.futures.as_completed(futures)]
(r/'calibration-pipeline-results.json').write_text(json.dumps(records,indent=2)+'\n')
raise SystemExit(any(row['returncode'] for row in records))
