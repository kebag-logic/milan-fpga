#!/usr/bin/env python3
"""Run scoped checks concurrently in disposable exact-head extractions."""
import argparse, concurrent.futures, hashlib, json, os, pathlib, subprocess, time
P=pathlib.Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=P,required=True);ap.add_argument('--packet',type=P,required=True);ap.add_argument('--compiler',type=P,required=True);ap.add_argument('--prepare-only',action='store_true');ap.add_argument('--prepared',action='store_true');a=ap.parse_args()
a.repo=a.repo.resolve();a.packet=a.packet.resolve();a.compiler=a.compiler.resolve()
scratch=a.packet/'scratch'; receipts=a.packet/'receipts';scratch.mkdir(exist_ok=True);receipts.mkdir(exist_ok=True)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.repo,text=True).strip()
assert head=='669ded57b1fabc2bbf274b8ad05493c7593e0a0a',head
identity=subprocess.check_output([str(a.compiler),'--version'],text=True).strip();assert '5.050' in identity,identity
(receipts/'compiler-identity.txt').write_text(identity+'\nsha256 '+hashlib.sha256(a.compiler.read_bytes()).hexdigest()+'\n')
wrapper=scratch/'compiler-cap'
if not a.prepared:
 wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=="-j" and a[i+1]=="0": a[i+1]="2"\nos.execv('+repr(str(a.compiler))+', ['+repr(str(a.compiler))+']+a)\n');wrapper.chmod(0o755)
if not a.prepared:
 archive=subprocess.check_output(['git','archive',head],cwd=a.repo)
 for name in ['campaign-tree','adp-tree','guards-tree']:
  dest=scratch/name;dest.mkdir(exist_ok=True)
  subprocess.run(['tar','-xf','-','-C',str(dest)],input=archive,check=True)
if a.prepare_only: raise SystemExit(0)
env=dict(os.environ,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE='1',MAKEFLAGS='-j16')
ns={'__file__':str(scratch/'campaign-tree/tb/pp_top/notify_mutants.py'),'__name__':'focus_catalog'}
# Import the catalog without running its command-line entry point.
import types,sys
mod=types.ModuleType('focus_catalog');mod.__dict__.update(ns);sys.modules[mod.__name__]=mod
exec(compile((scratch/'campaign-tree/tb/pp_top/notify_mutants.py').read_text(),ns['__file__'],'exec'),mod.__dict__)
names=[m.name for m in mod.DOMAIN_NOTIFY+mod.INTERFACE_ROWS+mod.INTERFACE_DEPTH_PROBES]
assert len(names)==30,len(names)
checks=[('notify-focus',scratch/'campaign-tree',['python3','tb/pp_top/notify_mutants.py','--output',str(receipts/'notify-focus'),'--verilator',str(wrapper),'--jobs','2','--only',*names]),('adp',scratch/'adp-tree/tb/adp_engine',['make','-j16','run','VERILATOR='+str(wrapper)]),('if-guards',scratch/'guards-tree/tb/pp_top',['make','-j16','if-guards','VERILATOR='+str(wrapper)])]
def run(item):
 name,cwd,cmd=item;start=time.time()
 with (receipts/(name+'.log')).open('w') as out:
  rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=out,stderr=subprocess.STDOUT).returncode
 (receipts/(name+'.rc')).write_text(str(rc)+'\n')
 result={'name':name,'rc':rc,'seconds':round(time.time()-start,2),'head':head,'command':cmd,'cwd':str(cwd)}
 (receipts/(name+'-run.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 codes=list(pool.map(run,checks))
raise SystemExit(any(codes))
