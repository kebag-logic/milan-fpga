#!/usr/bin/env python3
"""Independent full-catalog union audit with build failures kept separate."""
import argparse, concurrent.futures, json, os, pathlib, shutil, sys, time
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);p.add_argument("--jobs",type=int,default=8);p.add_argument("--workers",type=int,default=2);a=p.parse_args()
src=a.source.resolve();pkt=a.packet.resolve();scratch=pkt/"scratch"/"mutations";receipts=pkt/"receipts"/"mutations";receipts.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(src/"sw/firmware/ctrl/test"))
import ctrl_mutants as cm, ctrl_arms as ca, ctrl_build as cb, ctrl_reuse, fw_gtest
os.environ["CTRL_RV32_CC"]="riscv64-elf-gcc"
assert 1<=a.workers<=a.jobs<=16
arms={"model":ca.arm_model,"port":ca.arm_port,"adp":ca.arm_adp,"unit":ca.arm_unit,"walk":ca.arm_walk,"entity":ca.arm_entity,"maap":ca.arm_maap,"maap_debug":ca.arm_maap_debug,"maap_if2":ca.arm_maap_if2,"rv32":lambda t:ca.arm_rv32(t,True)}
def clean(t): return t.replace(str(src),"<source>").replace(str(pkt),"<packet>").replace(str(pathlib.Path.home()),"<home>")
def worker(index):
 root=scratch/str(index);root.mkdir(parents=True,exist_ok=True);reuse=root/"reuse";ctrl_reuse.cut_reuse(reuse)
 build=fw_gtest.Build(jobs=max(1,a.jobs//a.workers));records=[]
 for ordinal in range(index,len(cm.MUTANTS),a.workers):
  m=cm.MUTANTS[ordinal];start=time.monotonic();tree=cb.Tree(cm.plant(m,root),root/m.name/"build",reuse,build);results=[];logs=[]
  for arm,test,needle in m.kills():
   try: out=arms[arm](tree)
   except cb.Refusal as exc: out=cb.Outcome(arm,2,str(exc))
   hit=cm.caught(test,needle,out)
   results.append({"arm":arm,"test":test,"needle":needle,"rc":out.rc,"caught":hit})
   logs.append(f"arm={arm} rc={out.rc} expected_test={test} expected_text={needle!r} caught={hit}\n"+out.log)
  record={"index":ordinal,"name":m.name,"path":m.path,"seconds":round(time.monotonic()-start,3),"kills":results}
  records.append(record);(receipts/(m.name+".log")).write_text(clean("\n".join(logs)))
  print(index,ordinal,m.name,all(r["caught"] for r in results),flush=True)
  # Preserve cached C++ objects until this worker completes; other workers never share them.
 (receipts/f"partition-{index}.json").write_text(json.dumps(records,indent=2)+"\n")
 return records
with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as executor: parts=list(executor.map(worker,range(a.workers)))
records=sorted([r for part in parts for r in part],key=lambda r:r["index"])
assert [r["index"] for r in records]==list(range(len(cm.MUTANTS)))
assert len({r["name"] for r in records})==len(cm.MUTANTS)
summary={"catalog":len(cm.MUTANTS),"maap_name_prefix_count":sum(m.name.startswith("maap-") for m in cm.MUTANTS),"executed":len(records),"caught":sum(all(k["caught"] for k in r["kills"]) for r in records),"build_refusals":sum(k["rc"]==2 for r in records for k in r["kills"]),"complete_disjoint":True}
(receipts/"union.json").write_text(json.dumps(summary,indent=2)+"\n");print(summary,flush=True)
raise SystemExit(0 if summary["caught"]==summary["catalog"] else 1)
