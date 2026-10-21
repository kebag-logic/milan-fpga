#!/usr/bin/env python3
"""Run independent focused checks in disposable copies; never edit the source tree."""
import argparse, concurrent.futures, os, pathlib, subprocess, tarfile, io
p=argparse.ArgumentParser()
p.add_argument('--source',type=pathlib.Path,required=True)
p.add_argument('--packet',type=pathlib.Path,required=True)
p.add_argument('--compiler',default='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
a=p.parse_args(); a.source=a.source.resolve(); a.packet=a.packet.resolve()
s=a.packet/'scratch'; s.mkdir(exist_ok=True)
tree=s/'focused-tree'; tree.mkdir(exist_ok=True)
data=subprocess.check_output(['git','archive','HEAD'],cwd=a.source)
with tarfile.open(fileobj=io.BytesIO(data)) as t: t.extractall(tree,filter='data')
wrapper=s/'compiler-cap.py'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i,x in enumerate(a[:-1]):\n if x=="-j": a[i+1]=os.environ.get("REVIEW_BUILD_JOBS","2")\nos.execv('+repr(a.compiler)+', ['+repr(a.compiler)+']+a)\n')
wrapper.chmod(0o755)
env=dict(os.environ,VERILATOR=str(wrapper),TMPDIR=str(s),MAKEFLAGS='-j16')
def run(name,cmd,cwd,jobs='2'):
 with (a.packet/(name+'.log')).open('w') as log:
  r=subprocess.run(cmd,cwd=cwd,env=dict(env,REVIEW_BUILD_JOBS=jobs),stdout=log,stderr=subprocess.STDOUT)
 (a.packet/(name+'.rc')).write_text(str(r.returncode)+'\n')
 print(name, r.returncode,flush=True)
 return r.returncode
def controls():
 names=['listener-repark-takes-matcher-pairs','listener-two-parks-grouped','listener-walk-ends-owing-a-transmit','listener-walk-marks-only-served-slots','listener-walk-marks-group-only-on-retire','listener-handover-forgets-walk-mark']
 return run('focused-controls',['python3','tb/srp_top/mutants.py','--jobs','4','--only',','.join(names),'--output',str(a.packet/'controls')],tree)
def merged_suite():
 r=run('merged-pp-build',['make','-j16','gsi-build'],tree/'tb/pp_top','8')
 if r: return r
 return run('merged-pp-default',['./obj_dir/Vpp_top_sim'],tree/'tb/pp_top','8')
with concurrent.futures.ThreadPoolExecutor(2) as pool:
 fs=[pool.submit(controls),pool.submit(merged_suite)]
 results=[f.result() for f in fs]
raise SystemExit(any(results))
