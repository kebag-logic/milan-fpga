#!/usr/bin/env python3
"""Exercise the fifteen composition mutations, four adapted mutations and two filter controls."""
import argparse, concurrent.futures, json, os, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
ap=argparse.ArgumentParser();ap.add_argument("repo",type=Path);ap.add_argument("--jobs",type=int,default=4);a=ap.parse_args()
p=Path(__file__).resolve().parent;repo=a.repo.resolve();os.environ["TMPDIR"]=str(p/"scratch")
sys.path.insert(0,str(repo/"sw/firmware/ctrl/test"))
import ctrl_arms, ctrl_build, ctrl_mutants, acmp_review_mutants, fw_gtest
names={m.name for m in acmp_review_mutants.MUTANTS[-15:]}
names.update(["app-binds-pool-after-the-mailbox","app-acmp-never-composed", "maap-app-missing-rx-interrupt", "maap-app-channel-closed"])
names.update(m.name for m in ctrl_mutants.MUTANTS if "maap" in m.name and ("irq" in m.name or "filter" in m.name))
selected=[m for m in ctrl_mutants.MUTANTS if m.name in names]
assert len(selected)==21
print("Selected",len(selected),"mutations",flush=True)
def one(m):
 start=time.monotonic();root=p/"scratch/mutations"
 tree=ctrl_build.Tree(ctrl_mutants.plant(m,root),root/m.name/"build",p/"scratch/reuse",fw_gtest.Build(jobs=a.jobs))
 log=[];caught=True
 for arm,test,needle in m.kills():
  try:
   result=getattr(ctrl_arms,"arm_"+arm)(tree)
   ok=ctrl_mutants.caught(test,needle,result)
   log.append(result.log)
  except Exception as e:ok=False;log.append(str(e))
  caught &= ok
 (p/("mutation-"+m.name+".log")).write_text("\n".join(log))
 print(m.name,"CAUGHT" if caught else "ESCAPED",round(time.monotonic()-start,2),flush=True)
 return {"name":m.name,"caught":caught}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,selected))
(p/"mutation-results.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(any(not r["caught"] for r in results))
