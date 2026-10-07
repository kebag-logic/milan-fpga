#!/usr/bin/env python3
"""Run focused source-head suites with at most twelve compiler jobs."""
import argparse, concurrent.futures, json, os, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
ap=argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
ap.add_argument("--jobs", type=int, default=4)
a=ap.parse_args()
p=Path(__file__).resolve().parent
repo=a.repo.resolve()
os.environ["TMPDIR"]=str(p/"scratch")
sys.path.insert(0,str(repo/"sw/firmware/ctrl/test"))
import ctrl_arms, ctrl_build, ctrl_reuse, fw_gtest
reuse=p/"scratch/reuse"
ctrl_reuse.cut_reuse(reuse)
def one(arm):
 start=time.monotonic()
 try:
  tree=ctrl_build.Tree(repo/"sw/firmware/ctrl",p/"scratch"/arm,reuse,fw_gtest.Build(jobs=a.jobs))
  result=getattr(ctrl_arms,"arm_"+arm)(tree)
  rc,log=result.rc,result.log
 except Exception as e:
  rc,log=2,str(e)
 (p/(arm+".log")).write_text(log)
 (p/(arm+".rc")).write_text(str(rc)+"\n")
 print(arm,"rc",rc,"seconds",round(time.monotonic()-start,2),flush=True)
 return {"arm":arm,"rc":rc,"seconds":round(time.monotonic()-start,2)}
arms=["acmp","acmpif2","acmpwalk","acmpnvm","model","maap","maap_if2","unit"]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(one,arms))
(p/"focused-results.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(any(r["rc"] for r in results))
