#!/usr/bin/env python3
"""Read-only source review runs; all generated files stay under packet/scratch."""
import argparse, concurrent.futures, json, os, shutil, sys, traceback
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument("source",type=Path); p.add_argument("--jobs",type=int,default=8)
a=p.parse_args(); root=a.source.resolve(); packet=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(root/"sw/firmware/ctrl/test"))
from ctrl_build import Tree, CTRL
import fw_gtest, srp_arms, ctrl_arms
scratch=packet/"scratch/focused"; scratch.mkdir(parents=True,exist_ok=True)
receipts=packet/"receipts"; receipts.mkdir(exist_ok=True)

def run(name,interfaces,test=None,rv32=False):
    out=scratch/name
    try:
        tree=Tree(CTRL,out,out/"reuse",fw_gtest.Build(jobs=max(1,a.jobs//2)))
        if rv32:
            result=srp_arms.arm_srp_rv32(tree,root/"third_party/lwSRP",interfaces,
                root/"configs/endstation_ax7101_8x8.yaml")
        else:
            result=srp_arms.arm_srp(tree,root/"third_party/lwSRP",interfaces,test=test)
        (receipts/(name+".log")).write_text(result.log)
        (receipts/(name+".rc")).write_text(str(int(result.rc))+"\n")
        return {"name":name,"rc":int(result.rc)}
    except Exception:
        (receipts/(name+".log")).write_text(traceback.format_exc())
        (receipts/(name+".rc")).write_text("2\n")
        return {"name":name,"rc":2}

specs=[(f"srp-if{i}",i,"srp_mbx.cpp",False) for i in (1,2)]
specs += [(f"walk-if{i}",i,"srp_walk.cpp",False) for i in (1,2)]
specs += [(f"latency-if{i}",i,"srp_latency.cpp",False) for i in (1,2)]
specs += [(f"rv32-largest-if{i}",i,None,True) for i in (1,2)]
specs += [(f"probe-rebind-if{i}",i,str(packet/"probe_shared_rebind.cpp"),False) for i in (1,2)]
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures=[pool.submit(run,*s) for s in specs]
    for f in concurrent.futures.as_completed(futures):
        r=f.result(); results.append(r); print(json.dumps(r),flush=True)
(receipts/"focused-results.json").write_text(json.dumps(results,indent=2)+"\n")
# Probe failures are evidence under review, never interpreted as a passing gate.
sys.exit(0 if all(r["rc"]==0 for r in results if not r["name"].startswith("probe-")) else 1)
