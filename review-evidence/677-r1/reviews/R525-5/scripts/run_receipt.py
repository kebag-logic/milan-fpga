#!/usr/bin/env python3
"""Run one foreground gate, keeping its unfiltered output and exit status."""
import argparse, json, os, pathlib, subprocess, time
p=argparse.ArgumentParser()
p.add_argument("--repo",type=pathlib.Path,required=True)
p.add_argument("--packet",type=pathlib.Path,required=True)
p.add_argument("name")
p.add_argument("command",nargs=argparse.REMAINDER)
a=p.parse_args()
a.repo=a.repo.resolve(); a.packet=a.packet.resolve()
scratch=a.packet/"scratch"; (scratch/"tmp").mkdir(parents=True,exist_ok=True)
env=dict(os.environ,TMPDIR=str(scratch/"tmp"),PYTHONDONTWRITEBYTECODE="1",PYTHONUNBUFFERED="1",GIT_NO_REPLACE_OBJECTS="1",MILAN_RV32_CC=str(scratch/"sdk/bin/riscv32-linux-gcc"),MAKEFLAGS="-j4")
start=time.monotonic()
with (a.packet/"receipts"/(a.name+".log")).open("w") as f:
    print("argv: "+json.dumps(a.command),file=f,flush=True)
    result=subprocess.run(a.command,cwd=a.repo,env=env,stdout=f,stderr=subprocess.STDOUT)
(a.packet/"receipts"/(a.name+".rc")).write_text(str(result.returncode)+"\n")
(a.packet/"receipts"/(a.name+".json")).write_text(json.dumps({"argv":a.command,"rc":result.returncode,"elapsed_seconds":round(time.monotonic()-start,3)},indent=2)+"\n")
print(a.name+": rc="+str(result.returncode),flush=True)
raise SystemExit(result.returncode)
