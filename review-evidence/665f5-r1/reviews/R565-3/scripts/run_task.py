#!/usr/bin/env python3
"""Run a single foreground gate and retain its actual exit code and command."""
import json, os, pathlib, subprocess, sys, time
root, packet, name = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve(), sys.argv[3]
args=sys.argv[4:]; start=time.monotonic()
env=dict(os.environ,TMPDIR=str(packet/"scratch"),PYTHONDONTWRITEBYTECODE="1")
with (packet/f"receipts/{name}.log").open("w") as out:
 result=subprocess.run(args,cwd=root,env=env,stdout=out,stderr=subprocess.STDOUT)
record={"name":name,"argv":args,"rc":result.returncode,"seconds":round(time.monotonic()-start,2)}
(packet/f"receipts/{name}.json").write_text(json.dumps(record,indent=2)+"\n")
(packet/f"receipts/{name}.rc").write_text(str(result.returncode)+"\n")
print(json.dumps(record),flush=True)
raise SystemExit(result.returncode)
