"""Run the corrected candidate's gates in the foreground, sharing four harness slots."""
import concurrent.futures,hashlib,json,os,subprocess,sys,time
from pathlib import Path
from harness_slots import slot
root=Path.cwd();r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/refined')
assert root==Path('$LANES/arty-split')
refined=json.loads((r/'refinement.json').read_text())
assert refined['status']=='APPLIED; FRESH QUALIFICATION REQUIRED'
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'));import build
assert build.tree_digest([root/p for p in build.FIRMWARE_TREES])==refined['firmware_tree']
for path in Path('/proc').glob('[0-9]*/cmdline'):
 try:exe=path.read_bytes().split(b'\0')[0]
 except OSError:continue
 assert not (exe.startswith(b'$VALIDATION_STORAGE/artysplit-a829/') and exe.endswith(b'/native/Vsim')),exe
env=dict(os.environ,PYTHONHASHSEED='0',PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(r/'work-tmp'))
def command(name,argv,needs_slot=False):
 def run():
  with (r/(name+'.log')).open('w') as stream:
   return subprocess.run(argv,cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=172800).returncode
 if needs_slot:
  with slot(name):code=run()
 else:code=run()
 record=dict(command=argv,returncode=code,environment={key:env[key] for key in ('PYTHONHASHSEED','TMPDIR')},
             log=str(r/(name+'.log')))
 (r/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
 print(name,code,flush=True)
 return dict(name=name,**record)
def exports():
 while not (r/'identity-final-compare.json').exists():
  failure=r/'products-pipeline-command.json'
  if failure.exists() and json.loads(failure.read_text())['returncode']:
   return dict(name='identity-final-export-command',returncode=2,reason='Product prerequisite failed')
  time.sleep(2)
 assert json.loads((r/'identity-final-compare.json').read_text())['status']=='PASS'
 return command('identity-final-export-command',[sys.executable,'-B',str(r/'identity-final-export.py')],True)
jobs=[
 ('final-census-command',[sys.executable,'-B',str(r/'run-final-census.py')],False),
 ('firmware-pipeline-command',[sys.executable,'-B',str(r/'run-final-other-gates.py'),'firmware'],False),
 ('boot-pipeline-command',[sys.executable,'-B',str(r/'run-final-other-gates.py'),'boot'],False),
 ('products-pipeline-command',[sys.executable,'-B',str(r/'final-product-identity.py')],False),
 ('docs-pipeline-command',[sys.executable,'-B',str(r/'final-product-docs.py')],False),
 ('final-service-selftest',[sys.executable,'-B','tb/verilator/ctrl_service_budget/selftest.py'],True),
 ('watch-final-costs-command',[sys.executable,'-B',str(r/'watch-final-costs.py')],False),
]
records=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 futures=[pool.submit(command,*job) for job in jobs]+[pool.submit(exports)]
 for future in concurrent.futures.as_completed(futures):
  records.append(future.result())
  (r/'pipeline-results.json').write_text(json.dumps(records,indent=2)+'\n')
assert build.tree_digest([root/p for p in build.FIRMWARE_TREES])==refined['firmware_tree']
raise SystemExit(any(row['returncode'] for row in records))
