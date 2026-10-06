#!/usr/bin/env python3
"""Replay focused source checks in disposable trees; foreground supervisor waits for every child."""
import argparse,concurrent.futures,os,pathlib,subprocess,tarfile,time,io
ap=argparse.ArgumentParser();ap.add_argument("--repo",type=pathlib.Path,required=True);ap.add_argument("--packet",type=pathlib.Path,required=True);ap.add_argument("--verilator",required=True);a=ap.parse_args()
r=a.repo.resolve();p=a.packet.resolve();s=p/"scratch";logs=p/"receipts"/"focused";logs.mkdir(parents=True,exist_ok=True)
assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=r,text=True).strip()=="cd9825c947cf67b735d26cc1c42541ccd9d7f637"
identity=subprocess.check_output([a.verilator,"--version"],text=True);assert "Verilator 5.050" in identity
(logs/"identity.txt").write_text(identity)
tree=s/"focused-source";tree.mkdir(parents=True,exist_ok=True)
archive=subprocess.check_output(["git","archive","HEAD"],cwd=r)
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:tf.extractall(tree,filter="data")
shim=s/"bin";shim.mkdir(exist_ok=True)
# Cap the per-build compiler fan-out: four concurrent units at two workers stay below 16.
(shim/"verilator-capped").write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i,x in enumerate(a[:-1]):\n if x == '-j': a[i+1]='2'\nos.execv(os.environ['REVIEW_VERILATOR'],[os.environ['REVIEW_VERILATOR']]+a)\n")
(shim/"make").write_text("#!/usr/bin/env python3\nimport os,sys\nos.execv('/usr/bin/make',['/usr/bin/make','-j16']+sys.argv[1:])\n")
for f in shim.iterdir():f.chmod(0o755)
env=os.environ.copy();env.update(PATH=str(shim)+os.pathsep+env['PATH'],TMPDIR=str(s),REVIEW_VERILATOR=str(pathlib.Path(a.verilator).resolve()))
v=str(shim/"verilator-capped")
def run(name,cmd,cwd):
 start=time.monotonic()
 with (logs/(name+".log")).open('w') as f:
  f.write('COMMAND '+repr(cmd)+'\n');f.flush()
  rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (logs/(name+".rc")).write_text(str(rc)+'\n')
 print(name,'rc',rc,'seconds',round(time.monotonic()-start,1),flush=True)
 return rc
jobs=[('withdraw-campaign',['python3','tb/pp_top/notify_mutants.py','--output',str(logs/'withdraw-campaign'),'--verilator',v,'--jobs','3','--only','withdraw_unregistered','withdraw_abort_ignored','cancel_one_clock_late'],tree),('arbiter',['make','-j16','run','VERILATOR='+v],tree/'tb/tx_arbiter'),('originator',['make','-j16','run','VERILATOR='+v],tree/'tb/originator')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(lambda j:run(*j),jobs))
raise SystemExit(any(results))
