#!/usr/bin/env python3
"""Run independent foreground commands concurrently and retain each exit."""
import concurrent.futures, json, os, subprocess, sys, time
from pathlib import Path
root=Path(sys.argv[1]).resolve();packet=Path(sys.argv[2]).resolve();spec=Path(sys.argv[3])
commands=json.loads(spec.read_text())
def run(item):
 name=item["name"]; scratch=packet/"scratch"/name;scratch.mkdir(parents=True,exist_ok=True)
 env=dict(os.environ,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE="1",PYTHONHASHSEED="0",MAKEFLAGS="-j16")
 env.update(item.get("env",{}));cmd=[s.replace("{ROOT}",str(root)).replace("{PACKET}",str(packet)).replace("{MD_PYTHON}",os.environ.get("MD_PYTHON","python3")) for s in item["argv"]]
 start=time.monotonic()
 with (packet/"receipts"/(name+".log")).open("wb") as f:
  try:r=subprocess.run(cmd,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=item.get("timeout",540));rc=r.returncode
  except subprocess.TimeoutExpired:rc=124;f.write(b"\nREVIEW TIMEOUT\n")
 (packet/"receipts"/(name+".rc")).write_text(str(rc)+"\n")
 result={"name":name,"command":item["argv"],"rc":rc,"seconds":round(time.monotonic()-start,3)}
 print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,commands))
(packet/"receipts"/(spec.stem+"-results.json")).write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(any(x["rc"]!=0 for x in results))
