#!/usr/bin/env python3
"""Run five small suites, with a joined pool and bounded compile workers."""
import concurrent.futures,os,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]).resolve()
compiler=pathlib.Path(sys.argv[3]).resolve()
wrapper=out/'scratch'/'bounded-compiler.py'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=="-j": a[i+1]="4"\nos.execv('+repr(str(compiler))+',['+repr(str(compiler))+']+a)\n')
wrapper.chmod(0o755)
env=dict(os.environ,TMPDIR=str(out/'scratch'/'tmp'),PATH=str(compiler.parent)+':'+os.environ['PATH'])
def run(name):
 with (out/('suite-'+name+'.log')).open('w') as f:
  r=subprocess.run(['make','-j16','-C','tb/'+name,'VERILATOR='+str(wrapper)],cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
 (out/('suite-'+name+'.rc')).write_text(str(r.returncode)+'\n'); print(name,r.returncode,flush=True)
 return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 rc=list(ex.map(run,['prng','dispatch','desc_store','timer_map','dyn_state']))
sys.exit(any(rc))
