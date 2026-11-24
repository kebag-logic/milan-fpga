"""An explicitly incomplete prefix can expose an owner failure, never qualify an image."""
import datetime,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4');source=r/'arm-two/held-results/srp-talker-held.log'
while True:
 if (r/'watch-finding.json').exists():raise SystemExit('A measured finding takes priority')
 if source.exists():
  with source.open('rb') as stream:
   stream.seek(max(0,source.stat().st_size-6000));tail=stream.read().decode(errors='replace')
  cycles=re.findall(r'^CALL (\d+) ',tail,re.M)
  if 'RESULT: PASS' in tail or cycles and int(cycles[-1])>=280_000_000:break
 time.sleep(5)
out=r/'snapshots/full-mrpdu-prefix';out.mkdir();(out/'results').mkdir()
shutil.copy2(r/'arm-two/build.json',out/'build.json')
raw=source.read_bytes();raw=raw[:raw.rfind(b'\n')+1];target=out/'results'/source.name;target.write_bytes(raw)
record=dict(status='INCOMPLETE PREFIX; NOT QUALIFICATION',source=str(source),bytes=len(raw),
            sha256=hashlib.sha256(raw).hexdigest(),captured_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
(out/'prefix.json').write_text(json.dumps(record,indent=2)+'\n')
with (r/'census-full-mrpdu-prefix.log').open('w') as log:
 subprocess.run([sys.executable,'-B',str(r/'census.py'),str(r/'census-full-mrpdu-prefix.json'),str(out/'results')],
                env=dict(os.environ,CENSUS_INCLUDE_RUNNING='1'),stdout=log,stderr=subprocess.STDOUT,check=True,timeout=7200)
subprocess.run([sys.executable,'-B',str(r/'merge-census.py'),str(r/'census-merged-full-mrpdu-prefix.json'),
                str(r/'census-merged-valid-complete.json'),str(r/'census-full-mrpdu-prefix.json')],check=True)
with (r/'model-full-mrpdu-prefix.json').open('w') as log:
 subprocess.run([sys.executable,'-B',str(r/'derive-own.py'),str(r/'census-merged-full-mrpdu-prefix.json')],stdout=log,check=True,timeout=3600)
x=json.loads((r/'model-full-mrpdu-prefix.json').read_text())
print(x['status'],x['load'],x['choices'],flush=True)
