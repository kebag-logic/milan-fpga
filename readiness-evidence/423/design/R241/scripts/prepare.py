from pathlib import Path
import subprocess,hashlib,json,os
ROOT=Path(__file__).resolve().parents[1]
TRUSTED=Path('$VALIDATION_STORAGE/reviews/r241-423-design/scripts/check_merge_containment.py')
def run(name,cmd,cwd):
 p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(ROOT/'fixtures')})
 (ROOT/'logs'/f'{name}.log').write_text('COMMAND '+repr(cmd)+'\nEXIT '+str(p.returncode)+'\n'+p.stdout+p.stderr)
 print(name,'exit',p.returncode); print((p.stdout+p.stderr)[-1500:]);p.check_returncode()
pub=ROOT/'public/readiness-evidence/423'
rows=[]
for entry in json.loads((pub/'MANIFEST.json').read_text()):
 actual=hashlib.sha256((pub/entry['file']).read_bytes()).hexdigest()
 assert actual==entry['published_sha256']
 if not entry['path_redacted']: assert actual==entry['original_sha256']
 rows.append({'file':entry['file'],'sha256':actual,'verified':True})
(ROOT/'logs/manifest-verification.json').write_text(json.dumps(rows,indent=2)+'\n');print('Manifest: 6/6 entries verified')
run('trusted-selftest',['rtk','proxy','python3','-B',str(TRUSTED),'--selftest'],TRUSTED.parent.parent)
run('public-fixture',['rtk','proxy','python3','-B',str(pub/'probe/probe_ff_merge.py'),str(TRUSTED)],ROOT/'fixtures')
if not (ROOT/'fixtures/donor.git').exists():
 run('clone-donor',['rtk','proxy','git','-c','credential.helper=','clone','--bare','https://github.com/Mister-M-alt/FPGA-gPTP.git',str(ROOT/'fixtures/donor.git')],ROOT/'fixtures')
