#!/usr/bin/env python3
"""Run an exact-head cold default in a disposable tree, in the foreground."""
import argparse, hashlib, json, os, pathlib, subprocess, tarfile, time
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);p.add_argument("name");p.add_argument("cpus");p.add_argument("simulator");p.add_argument("--parallel",action="store_true");a=p.parse_args()
head="8e4b1e53e9b5a8ef5f9854095347436ab84259b6"
work=a.packet/"scratch"/a.name;work.mkdir(parents=True,exist_ok=False)
archive=work/"source.tar"
with archive.open("wb") as f: subprocess.run(["git","-C",str(a.source),"archive",head],stdout=f,check=True)
with tarfile.open(archive) as t:t.extractall(work,filter="data")
archive.unlink()
env=os.environ.copy()
for k in ("MAKEFLAGS","MFLAGS","GNUMAKEFLAGS"):env.pop(k,None)
env["VERILATOR"]=a.simulator;env["PATH"]=str(pathlib.Path(a.simulator).parent)+os.pathsep+env["PATH"]
cmd=["taskset","-c",a.cpus,"make"]+(["-j16"] if a.parallel else [])+["-C","tb/verilator/follow_ring"]
meta={"head":head,"command":cmd,"MAKEFLAGS":"unset","cold":True,"simulator":subprocess.check_output([a.simulator,"--version"],text=True).strip(),"simulator_sha256":hashlib.sha256(pathlib.Path(a.simulator).read_bytes()).hexdigest()}
start=time.monotonic()
with (a.packet/"receipts"/(a.name+".log")).open("w") as f:
 rc=subprocess.run(cmd,cwd=work,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
meta.update(rc=rc,wall_seconds=time.monotonic()-start)
(a.packet/"receipts"/(a.name+".rc")).write_text(str(rc)+"\n")
(a.packet/"receipts"/(a.name+".json")).write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta),flush=True)
raise SystemExit(rc)
