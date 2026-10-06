#!/usr/bin/env python3
"""Reproduce focused checks in an exact-commit archive; never edit the checkout."""
import argparse, concurrent.futures, io, json, os, pathlib, subprocess, tarfile, time
p = argparse.ArgumentParser(); p.add_argument("--repo", required=True); p.add_argument("--verilator", required=True); a=p.parse_args()
packet=pathlib.Path(__file__).resolve().parents[1]; scratch=packet/"scratch"; logs=packet/"receipts/focus"; logs.mkdir(parents=True,exist_ok=True)
head="cb730a2f9dd7e4f60a03a38d4b47b569e68da8df"
assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=a.repo,text=True).strip()==head
version=subprocess.check_output([a.verilator,"--version"],text=True); assert "5.050" in version
(logs/"identity.txt").write_text(version)
tree=scratch/"focus-head"; tree.mkdir(exist_ok=True)
raw=subprocess.check_output(["git","archive",head],cwd=a.repo)
with tarfile.open(fileobj=io.BytesIO(raw)) as tf: tf.extractall(tree, filter="data")
wrapper=scratch/"bounded-verilator.py"
wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i,v in enumerate(a[:-1]):\n if v in ('-j','--build-jobs') and a[i+1]=='0': a[i+1]=os.environ.get('R513_COMPILE_JOBS','3')\nos.execv(os.environ['R513_VERILATOR'],[os.environ['R513_VERILATOR'],*a])\n"); wrapper.chmod(0o755)
tmp=scratch/"tmp"; tmp.mkdir(exist_ok=True)
env=os.environ.copy(); env.update(VERILATOR=str(wrapper),R513_VERILATOR=str(pathlib.Path(a.verilator).resolve()),TMPDIR=str(tmp),MAKEFLAGS="-j16",R513_COMPILE_JOBS="3")
units=[("adp", "tb/adp_engine", "run"),("notify","tb/aecp_notify","run"),("top-if2","tb/pp_top","interfaces"),("srp-stream","tb/srp_stream_fsms","run"),("if-guards","tb/pp_top","if-guards")]
def run(u):
 name,d,target=u; cmd=["make","-j16","-C",str(tree/d),target,"VERILATOR="+str(wrapper)]; start=time.monotonic()
 with (logs/(name+".log")).open("w") as f:
  f.write("command: "+repr(cmd)+"\n"); f.flush(); r=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT)
 (logs/(name+".rc")).write_text(str(r.returncode)+"\n")
 result=dict(name=name,rc=r.returncode,seconds=round(time.monotonic()-start,2)); print(json.dumps(result),flush=True); return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(run,units))
(logs/"results.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(any(r["rc"] for r in results))
