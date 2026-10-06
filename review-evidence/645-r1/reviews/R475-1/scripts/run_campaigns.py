#!/usr/bin/env python3
"""Run the four frozen arrival campaigns and INTERNAL holds concurrently."""
import concurrent.futures, os, subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
C=P/"scratch/tb/verilator/follow_ring"
O=P/"receipts/campaigns"
O.mkdir(exist_ok=True)
exe=C/"obj_dir/Vfollow_ring"
items=[("none",["b8","--jitter-us","0"]),("uniform5",["b8","--jitter-us","5"]),("tail24",["b8","--jitter-us","2","--tail-us","24","--tail-p","1e-4"]),("uniform60",["b8","--jitter-us","60"]),("internal",["pullin","--hold-us","52","56"])]
def run(item):
    name,args=item
    command=["python3","-B","sweep.py",*args,"--exe",str(exe),"--out",str(O/name),"--jobs",("2" if name=="internal" else "3"),"--phases","16"]
    if name!="internal": command += ["--hold-s","40","--switch-hold-s","20","--extra","--dwell-s","1.0"]
    with (O/(name+".log")).open("w") as log:
        print("COMMAND",command,file=log,flush=True)
        rc=subprocess.run(command,cwd=C,stdout=log,stderr=subprocess.STDOUT).returncode
    (O/(name+".rc")).write_text(str(rc)+"\n")
    print(name,rc,flush=True)
    return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results=list(pool.map(run,items))
raise SystemExit(int(any(results)))
