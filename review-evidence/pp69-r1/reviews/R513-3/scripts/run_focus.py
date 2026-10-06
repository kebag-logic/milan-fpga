#!/usr/bin/env python3
"""Foreground coordinator for the review's independent, bounded focused runs.
Usage: python3 run_focus.py SOURCE PACKET [SIMULATOR]
All builds and temporary copies stay under PACKET/scratch. No source writes.
"""
import concurrent.futures as cf
import hashlib, json, os, pathlib, subprocess, sys, tarfile, time
src=pathlib.Path(sys.argv[1]).resolve()
out=pathlib.Path(sys.argv[2]).resolve()
simulator=sys.argv[3] if len(sys.argv)>3 else "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator"
head="669ded57b1fabc2bbf274b8ad05493c7593e0a0a"
assert subprocess.check_output(["git","-C",str(src),"rev-parse","HEAD"],text=True).strip()==head
scratch=out/"scratch"; receipts=out/"receipts"
for d in (scratch,receipts,scratch/"tmp",scratch/"bin"):d.mkdir(parents=True,exist_ok=True)
version=subprocess.check_output([simulator,"--version"],text=True)
assert "Verilator 5.050" in version, version
(receipts/"simulator-identity.txt").write_text(version+"launcher sha256 "+hashlib.sha256(pathlib.Path(simulator).read_bytes()).hexdigest()+"\n")
archive=scratch/"source.tar"
with archive.open("wb") as f:subprocess.run(["git","-C",str(src),"archive",head],stdout=f,check=True)
tree=scratch/"source";tree.mkdir(exist_ok=True)
with tarfile.open(archive) as t:t.extractall(tree,filter="data")
wrapper=scratch/"bin"/"bounded-simulator"
wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=='-j': a[i+1]=os.environ.get('PP69_BUILD_JOBS','3')\nos.execv("+repr(simulator)+",["+repr(simulator)+"]+a)\n")
wrapper.chmod(0o755)
env=os.environ.copy();env.update(TMPDIR=str(scratch/"tmp"),PYTHONDONTWRITEBYTECODE="1",MAKEFLAGS="-j16",PP69_BUILD_JOBS="3")
jobs=[("notify",[sys.executable,"tb/pp_top/notify_mutants.py","--output",str(receipts/"notify"),"--verilator",str(wrapper),"--jobs","4"],tree,{}),
      ("adp",["make","-j16","run","VERILATOR="+str(wrapper)],tree/"tb/adp_engine",{"PP69_BUILD_JOBS":"2"}),
      ("if-guards",["make","-j16","if-guards","VERILATOR="+str(wrapper)],tree/"tb/pp_top",{"PP69_BUILD_JOBS":"1"})]
def run(job):
 name,argv,cwd,extra=job;e=env|extra;start=time.time()
 with (receipts/(name+".log")).open("w") as log:
  log.write("command: "+json.dumps(argv)+"\n");log.flush()
  rc=subprocess.run(argv,cwd=cwd,env=e,stdout=log,stderr=subprocess.STDOUT,check=False).returncode
 elapsed=round(time.time()-start,3)
 (receipts/(name+".rc")).write_text(str(rc)+"\n")
 result={"job":name,"rc":rc,"seconds":elapsed};print(json.dumps(result),flush=True);return result
with cf.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,jobs))
(receipts/"focused-results.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(0 if all(x["rc"]==0 for x in results) else 1)
