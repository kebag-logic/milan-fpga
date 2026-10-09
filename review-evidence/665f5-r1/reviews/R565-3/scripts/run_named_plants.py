#!/usr/bin/env python3
"""Grade the three round-3 production plants against their named diagnostics."""
import dataclasses,json,pathlib,shutil,sys
root,packet=map(lambda x:pathlib.Path(x).resolve(),sys.argv[1:3])
sys.path.insert(0,str(root/"sw/firmware/ctrl/test"))
import aecp_arms,aecp_mutants,fw_gtest
from ctrl_build import Tree,CTRL,Refusal
out=packet/"scratch/named-plants";src=out/"ctrl"
shutil.copytree(CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
tree=Tree(src,out/"build",out/"reuse",fw_gtest.Build(jobs=4))
aecp_mutants.controls()
results=[];receipt=packet/"receipts/named-plants";receipt.mkdir(exist_ok=True)
for defect in aecp_mutants.DEFECTS[:3]:
 target=src/defect.path;before=target.read_text();assert before.count(defect.old)==1
 target.write_text(before.replace(defect.old,defect.new))
 try:
  outcome=aecp_arms.core_arm(tree,root/"configs/endstation_ax7101_1x1_tdm8.yaml",2,"app",":".join(dict.fromkeys(t for t,_ in defect.checks)))
 finally:target.write_text(before)
 caught=all(aecp_mutants.caught(t,s,outcome) for t,s in defect.checks)
 (receipt/(defect.name+".log")).write_text(outcome.log)
 results.append({"name":defect.name,"caught":caught,"suite_rc":outcome.rc,"checks":defect.checks})
 print(defect.name,"CAUGHT" if caught else "ESCAPED",flush=True)
(receipt/"results.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(int(not all(r["caught"] for r in results)))
