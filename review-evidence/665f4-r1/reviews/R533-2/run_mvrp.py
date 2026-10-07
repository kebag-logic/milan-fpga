#!/usr/bin/env python3
"""Check the generic MVRP IN/LV timing through the parent mailbox."""
import argparse,concurrent.futures,sys,traceback
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("--jobs",type=int,default=8);a=p.parse_args()
root=a.source.resolve();packet=Path(__file__).resolve().parent
sys.dont_write_bytecode=True;sys.path.insert(0,str(root/"sw/firmware/ctrl/test"))
import srp_arms,fw_gtest
from ctrl_build import Tree,CTRL
def check(i):
 out=packet/"scratch"/f"mvrp-if{i}"
 try:
  result=srp_arms.arm_srp(Tree(CTRL,out,out/"reuse",fw_gtest.Build(jobs=max(1,a.jobs//2))),
    root/"third_party/lwSRP",i,test=str(packet/"probe_mvrp.cpp"))
  log,rc=result.log,int(result.rc)
 except Exception:log,rc=traceback.format_exc(),2
 (packet/"receipts"/f"mvrp-if{i}.log").write_text(log)
 (packet/"receipts"/f"mvrp-if{i}.rc").write_text(str(rc)+"\n")
 print(i,rc,flush=True);return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(check,(1,2)))
sys.exit(int(any(results)))
