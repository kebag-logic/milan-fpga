#!/usr/bin/env python3
"""Reproduce exact-head linked-size figures and self-checks concurrently."""
import argparse, concurrent.futures, os, subprocess, time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("repo",type=Path);a=ap.parse_args()
p=Path(__file__).resolve().parent;repo=a.repo.resolve()
env={**os.environ,"TMPDIR":str(p/"scratch"),"MILAN_RV32_CC":str(p/"scratch/sdk/bin/riscv32-linux-gcc")}
tasks=[("image",["python3","-B","sw/firmware/ctrl/test/ctrl_image.py","--base","e21c1ca024d37ea188ad15b5c8f9c2dae18628df","--out",str(p/"scratch/image")]),("image-selftest",["python3","-B","sw/firmware/ctrl/test/ctrl_image_selftest.py","--require-rv32"])]
def one(task):
 name,cmd=task;start=time.monotonic()
 with (p/(name+".log")).open("w") as f:r=subprocess.run(cmd,cwd=repo,env=env,stdout=f,stderr=subprocess.STDOUT)
 (p/(name+".rc")).write_text(str(r.returncode)+"\n")
 print(name,"rc",r.returncode,"seconds",round(time.monotonic()-start,2),flush=True)
 return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(one,tasks))
raise SystemExit(any(results))
