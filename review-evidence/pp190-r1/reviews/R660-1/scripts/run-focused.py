#!/usr/bin/env python3
"""Run only the issue-specific campaign and documentation checks concurrently.
Usage: python3 run-focused.py SOURCE PACKET COMPILER
All temporary trees stay in PACKET/scratch; source is read-only.
"""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
src, packet, compiler = map(pathlib.Path, sys.argv[1:])
src=src.resolve(); packet=packet.resolve(); compiler=compiler.resolve()
work=packet/"scratch/focused"; logs=packet/"receipts/focused"
logs.mkdir(parents=True, exist_ok=True)
subprocess.run(["git", "clone", "--quiet", "--shared", str(src), str(work)], check=True)
assert subprocess.check_output(["git","rev-parse","HEAD"], cwd=work,text=True).strip()=="83405d192c451e9fba0ea1fe4e051aafdbb332cc"
env=os.environ.copy(); env.update(TMPDIR=str(packet/"scratch"), REVIEW_COMPILER=str(compiler), MAKEFLAGS="-j16")
wrapper=packet/"scripts/capped-compiler.py"
commands={"docs":["make","-j16","check"], "tspec-mutants":["python3","tb/pp_top/acmp_mutants.py","--jobs","2","--only","tspec_slot_zero","tspec_slot_last","tspec_no_allocator","--output",str(logs/"mutants"),"--verilator",str(wrapper)]}
def run(item):
 name,cmd=item
 with (logs/(name+".log")).open("w") as f:
  f.write(json.dumps(cmd)+"\n"); f.flush()
  start=time.time(); rc=subprocess.run(cmd,cwd=work,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (logs/(name+".rc")).write_text(str(rc)+"\n")
 print(name, "rc",rc,"seconds",round(time.time()-start,2),flush=True)
 return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 results=list(pool.map(run,commands.items()))
sys.exit(bool(any(results)))
