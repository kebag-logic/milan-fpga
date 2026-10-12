#!/usr/bin/env python3
"""Run independent focused fixtures concurrently; foreground lifetime owns all children."""
import argparse, concurrent.futures, json, os, subprocess, sys, time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("root",type=Path);ap.add_argument("packet",type=Path);ap.add_argument("--verilator",required=True);ap.add_argument("--phase",choices=["clean","plants","f5"],default="clean");a=ap.parse_args()
root=a.root.resolve();packet=a.packet.resolve();scratch=packet/"scratch";receipts=packet/"receipts"
env=dict(os.environ,VERILATOR=a.verilator,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE="1")
items=([(str(s),"clean") for s in (1,8)] if a.phase=="clean" else [("1",v) for v in ("tx-interval","rx-interval","tx-reset","aaf-reset","crf-reset","rx-saturation","late","rate")])
if a.phase=="f5": items=[("1","clean"),("8","clean"),("1","late"),("1","rate")]
def job(item):
    shape,variant=item;name=f"{a.phase}-{shape}-{variant}";work=scratch/name
    script="stream_counter_f5.py" if a.phase=="f5" else "stream_counters.py"
    cmd=[sys.executable,str(root/"tb/verilator/milan_dp"/script),"--shape",shape,"--variant",variant,"--work",str(work)]
    start=time.time()
    with (receipts/(name+".driver.log")).open("w") as f:
        proc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT)
    (receipts/(name+".rc")).write_text(str(proc.returncode)+"\n")
    for leaf in ("run.log","escape.log"):
        if (work/leaf).exists(): (receipts/(name+"."+leaf)).write_bytes((work/leaf).read_bytes())
    result={"job":name,"rc":proc.returncode,"elapsed_seconds":round(time.time()-start,2)}
    print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(job,items))
(receipts/(a.phase+"-results.json")).write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(any(x["rc"] for x in results))
