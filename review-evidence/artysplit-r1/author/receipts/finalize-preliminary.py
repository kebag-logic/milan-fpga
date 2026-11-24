"""Close the complete calibration traces, attest inputs, and derive the pending row."""
import datetime,hashlib,json,shutil,subprocess,sys,time
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4');root=Path.cwd()
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import build
wanted=[r/'arm-later/results'/f'notice-retried-{number}.log' for number in range(8)]
wanted+=[r/'arm-two/held-results/srp-talker-held.log']
def done(path):
 if not path.exists():return False
 with path.open('rb') as stream:stream.seek(max(0,path.stat().st_size-4000));return b'RESULT: PASS' in stream.read()
while not all(map(done,wanted)):
 if any((r/name).exists() for name in ('watch-finding.json','watch-extra-finding.json','remaining-finding.json')):
  raise SystemExit('A completed measured finding takes priority')
 time.sleep(5)
# The independent closure helper handles the historical broad-tree fingerprints
# with byte-identical firmware rebuilds, preserving the original reuse refusals.
# Census is read-only and may proceed while those rebuilds finish.
out=r/'later-last-census';out.mkdir();(out/'results').mkdir();shutil.copy2(r/'arm-later/build.json',out/'build.json')
files=[]
for number in (6,7):
 for ext in ('log','txt'):
  source=r/'arm-later/results'/f'notice-retried-{number}.{ext}'
  (out/'results'/source.name).symlink_to(source)
  files.append(dict(source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
(out/'selection.json').write_text(json.dumps(dict(kind='Read-only complete-group census view; not new native runs',files=files),indent=2)+'\n')
with (r/'census-preliminary-last.log').open('w') as log:
 subprocess.run([sys.executable,'-B',str(r/'census.py'),str(r/'census-preliminary-last.json'),str(out/'results'),str(r/'arm-two/held-results')],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=10800)
subprocess.run([sys.executable,'-B',str(r/'merge-census.py'),str(r/'census-preliminary-complete.json'),str(r/'census-merged-later-six.json'),str(r/'census-preliminary-last.json')],check=True)
with (r/'model-preliminary-complete.json').open('w') as log:
 subprocess.run([sys.executable,'-B',str(r/'derive-own.py'),str(r/'census-preliminary-complete.json')],stdout=log,check=True,timeout=3600)
x=json.loads((r/'model-preliminary-complete.json').read_text())
while not (r/'preliminary-input-closure.json').exists():time.sleep(5)
closure=json.loads((r/'preliminary-input-closure.json').read_text())
assert closure['status']=='PASS' and len(closure['arms'])==9
print(x['status'],x['load'],x['choices'],flush=True)
