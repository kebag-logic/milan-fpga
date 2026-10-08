#!/usr/bin/env python3
"""Run a bounded foreground command and save its complete output and status."""
import datetime, json, os, pathlib, subprocess, sys, time
packet=pathlib.Path(__file__).resolve().parents[1]
name,cwd,*command=sys.argv[1:]
start=time.monotonic(); env=os.environ.copy(); env["TMPDIR"]=str(packet/"scratch")
env["PYTHONDONTWRITEBYTECODE"]="1"; env["MAKEFLAGS"]="-j16"
log=packet/"receipts"/(name+".log")
with log.open("w") as f:
    f.write("COMMAND " + json.dumps(command)+"\n"); f.flush()
    try: rc=subprocess.run(command,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=570).returncode
    except subprocess.TimeoutExpired: rc=124
(packet/"receipts"/(name+".rc")).write_text(str(rc)+"\n")
record={"command":command,"cwd":cwd,"rc":rc,"seconds":round(time.monotonic()-start,3),"finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
(packet/"receipts"/(name+".json")).write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record)); print(log.read_text()[-5000:])
sys.exit(rc)
