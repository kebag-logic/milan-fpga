#!/usr/bin/env python3
"""Compare default gateware exports and fragments, with disposable registered submodules."""
import concurrent.futures,hashlib,json,os,pathlib,re,shlex,subprocess,sys
p=pathlib.Path(__file__).resolve().parents[1];source=pathlib.Path(sys.argv[1]).resolve();r=p/'scratch/export-tree';out=p/'scratch/default-exports';out.mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
def cmd(argv,cwd=source):return subprocess.check_output(argv,cwd=cwd,env=env,text=True)
if not r.exists():
 subprocess.run(['git','clone','--quiet','--shared','--no-hardlinks',str(source),str(r)],check=True,env=env)
 opts=[]
 for sub in ['protocol-processor','gptp-processor','third_party/verilog-axis']:opts+=['-c',f'submodule.{sub}.url={source/sub}']
 subprocess.run(['git','-c','protocol.file.allow=always',*opts,'submodule','update','--init','protocol-processor','gptp-processor','third_party/verilog-axis'],cwd=r,env=env,check=True,stdout=subprocess.DEVNULL)
base='fa450d301805881ad713b67521477bf042ddadfd';head='0bfef4987eede4b022b17c7b2f56d079ff84893b'
basepath=r/'sw/litex/review_base_soc.py';basepath.write_bytes(subprocess.check_output(['git','show',base+':sw/litex/milan_soc.py'],cwd=r))
sys.path.insert(0,str(r/'sw/builder'));import endstation_builder as eb
jobs=[];fragments=[]
for cfg in sorted((r/'configs').glob('endstation_*.yaml')):
 art=eb._derive_artifacts(str(cfg));eb._write_artifact_dir(art,r/'sw/builder/out')
 # The builder, configs and tracked fragments are byte-identical to base.
 fragment={'config':cfg.name,'argv':art.argv,'sweep_sha256':hashlib.sha256(art.sweep.encode()).hexdigest(),'adp_sha256':hashlib.sha256(art.adp_svh.encode()).hexdigest()};fragments.append(fragment)
 for kind,script in [('base',basepath),('head',r/'sw/litex/milan_soc.py')]:
  d=out/cfg.stem/kind
  args=[sys.executable,str(script),*art.argv,'--entity-gen-dir',str(r/'configs/generated'/cfg.stem),'--no-compile','--output-dir',str(d)]
  jobs.append((cfg.stem,kind,args,d))
def run(j):
 cfg,kind,args,d=j;log=p/'receipts'/('default-'+cfg+'-'+kind+'.log')
 with log.open('w') as f:
  print('COMMAND: '+shlex.join(args),file=f,flush=True);rc=subprocess.run(args,cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=500).returncode
 (log.with_suffix('.rc')).write_text(str(rc)+'\n');print(cfg,kind,rc,flush=True)
 return cfg,kind,rc,d
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,jobs))
(p/'scratch/export-results.json').write_text(json.dumps([(a,b,c,str(d)) for a,b,c,d in results]))
(p/'receipts/default-fragments.json').write_text(json.dumps(fragments,indent=2)+'\n')
for a,b,c,d in results:
 if c: print('NOT RUN comparison:',a,b,'export rc',c)
