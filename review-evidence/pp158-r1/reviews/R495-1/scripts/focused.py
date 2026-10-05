#!/usr/bin/env python3
"""Focused independent reproduction; disposable sources stay below packet/scratch."""
import argparse, concurrent.futures, hashlib, io, json, os, pathlib, subprocess, tarfile, time
p=argparse.ArgumentParser();p.add_argument("--repo",type=pathlib.Path,required=True);p.add_argument("--packet",type=pathlib.Path,required=True);p.add_argument("--simulator",required=True);a=p.parse_args()
repo=a.repo.resolve();packet=a.packet.resolve();scratch=packet/"scratch";receipts=packet/"receipts"
head="79571006b803a4ab4af65358f0d87bc3af73180e";base="054d01c79e59c3f80454ad9cdefd8e914b540bb4"
env=os.environ.copy();env.update(TMPDIR=str(scratch),MAKEFLAGS="-j16",PYTHONDONTWRITEBYTECODE="1")
version=subprocess.check_output([a.simulator,"--version"],text=True)
assert "5.050" in version,version
(receipts/"simulator-identity.txt").write_text(version+"wrapper_sha256 "+hashlib.sha256(pathlib.Path(a.simulator).read_bytes()).hexdigest()+"\n")
wrapper=packet/"scripts/simulator-bounded.py"
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i] == "-j": a[i+1]="2"\nos.execv(os.environ["REVIEW_SIMULATOR"],[os.environ["REVIEW_SIMULATOR"]]+a)\n');wrapper.chmod(0o755);env["REVIEW_SIMULATOR"]=str(pathlib.Path(a.simulator).resolve())
for name,rev in (("red",base),("head",head)):
 tree=scratch/name;tree.mkdir(exist_ok=True)
 archive=subprocess.check_output(["git","-C",str(repo),"archive",rev])
 with tarfile.open(fileobj=io.BytesIO(archive)) as t:t.extractall(tree,filter="data")
 if name=="red":
  (tree/"tb/aecp_notify/sim_main.cpp").write_bytes(subprocess.check_output(["git","-C",str(repo),"show",head+":tb/aecp_notify/sim_main.cpp"]))

def run(name,cmd,cwd):
 start=time.monotonic()
 with (receipts/(name+".log")).open("w") as log:
  log.write("COMMAND "+json.dumps(cmd)+"\n");log.flush()
  rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 (receipts/(name+".rc")).write_text(str(rc)+"\n")
 result=dict(name=name,rc=rc,seconds=round(time.monotonic()-start,2));print(json.dumps(result),flush=True);return result
controls=["dereg_mid_round_no_hold","dereg_pending_stops_follow","dereg_lost_at_round_end","counter_spacing_from_selection_tw","counter_stamp_at_send_only","counter_stamp_first_job_only"]
tasks=[("red",["make","-j16","run","VERILATOR="+str(wrapper)],scratch/"red/tb/aecp_notify"),("controls",["python3","tb/pp_top/notify_mutants.py","--jobs","4","--verilator",str(wrapper),"--output",str(receipts/"controls"),"--only",*controls],scratch/"head"),("docs-focused",["make","-j16","ids","figures","links","matrix","modmatrix","params","stale"],repo)]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(lambda t:run(*t),tasks))
(receipts/"focused-results.json").write_text(json.dumps(results,indent=2)+"\n")
red=(receipts/"red.log").read_text();assert "41 checks, 3 failures" in red
for check in ("DR1:","DR2:","DR3:"):assert "FAIL: "+check in red
assert "FAIL: DR1b:" not in red and "FAIL: DR2b:" not in red
assert results[0]["rc"]==2 and all(x["rc"]==0 for x in results[1:])
