#!/usr/bin/env python3
import concurrent.futures,json,sys,traceback
from pathlib import Path
root=Path(sys.argv[1]).resolve();packet=Path(sys.argv[2]).resolve()
sys.path.insert(0,str(root/"sw/firmware/ctrl/test"))
import ctrl_arms,ctrl_mutants,acmp_mutants,ctrl_reuse,fw_gtest
from ctrl_build import CTRL,Tree
work=packet/"scratch/sample";reuse=work/"reuse";ctrl_reuse.cut_reuse(reuse)
receipts=packet/"receipts"
armnames=("acmp","acmpwalk","acmpnvm")
def baseline(arm):
 tree=Tree(CTRL,work/("baseline-"+arm),reuse,fw_gtest.Build(jobs=2))
 o=getattr(ctrl_arms,"arm_"+arm)(tree)
 (receipts/("baseline-"+arm+".log")).write_text(o.log)
 (receipts/("baseline-"+arm+".rc")).write_text(str(o.rc)+"\n")
 return o.rc
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 assert not any(pool.map(baseline,armnames)),"positive control failed"
names={"acmp-duplicate-takes-a-new-sequence-id","acmp-retry-zeroes-the-status","acmp-response-keyed-on-the-source",
"acmp-disconnect-always-succeeds","acmp-probe-tx-any-interface","acmp-restart-on-a-smaller-index-only",
"acmp-valid-time-in-seconds","acmp-discovery-on-every-interface","acmp-stale-tag-taken",
"acmp-change-not-held-for-its-response","acmp-record-unique-id-little-endian","acmp-nvm-bindings-to-the-others"}
selected=[m for m in acmp_mutants.MUTANTS if m.name in names];assert len(selected)==len(names)
def mutant(m):
 tree=Tree(ctrl_mutants.plant(m,work/"mutants"),work/"mutants"/m.name/"build",reuse,fw_gtest.Build(jobs=2))
 rows=[];log=[]
 for arm,test,needle in m.kills():
  o=getattr(ctrl_arms,"arm_"+arm)(tree)
  ok=ctrl_mutants.caught(test,needle,o)
  rows.append({"arm":arm,"test":test,"assertion":needle,"rc":o.rc,"caught":ok})
  log.append(o.log)
 (receipts/("mutation-"+m.name+".log")).write_text("\n".join(log))
 (receipts/("mutation-"+m.name+".rc")).write_text(str(int(not all(r["caught"] for r in rows)))+"\n")
 return {"name":m.name,"path":m.path,"old":m.old,"new":m.new,"results":rows}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: rows=list(pool.map(mutant,selected))
(receipts/"sample-mutations.json").write_text(json.dumps(rows,indent=2)+"\n")
assert all(r["caught"] for m in rows for r in m["results"])
print("PASS: three positive arms and twelve planted defects; every named assertion caught its defect")
