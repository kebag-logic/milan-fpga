import argparse, json, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--packet",type=Path,required=True);p.add_argument("--jobs",type=int,default=4);p.add_argument("--mode",choices=["mutations","lifecycle","bounds"],required=True);a=p.parse_args()
sys.path.insert(0,str(a.repo.resolve()/"sw/firmware/ctrl/test"))
import ctrl_build as b, ctrl_arms, ctrl_reuse, fw_gtest
out=a.packet.resolve()/"scratch"/a.mode;out.mkdir(parents=True,exist_ok=True)
b.stack_pin(); reuse=ctrl_reuse.cut_reuse(out/"reuse")
if a.mode=="bounds":
 r=ctrl_arms.arm_service_bounds(b.Tree(b.CTRL,out/"build",reuse,fw_gtest.Build(jobs=a.jobs)))
 print(r.log);sys.exit(r.rc)
if a.mode=="lifecycle":
 import ctrl_pin,ctrl_pin_lifecycle
 clone=ctrl_pin.Clone(out,b.stack_pin())
 bad,count=ctrl_pin_lifecycle.controls(clone);print(f"Lifecycle: {count-bad}/{count} passed");sys.exit(bool(bad))
import ctrl_mutants as m
selected=[d for d in m.MUTANTS if d.name.startswith(("f3b-","pin-adp-","pub-maap-gate-","rv-maap-gate-"))]
print("Focused controls selected",len(selected),flush=True)
build=fw_gtest.Build(jobs=a.jobs);rows=[]
arms={"adp":ctrl_arms.arm_adp,"acmp":ctrl_arms.arm_acmp,"acmpif2":ctrl_arms.arm_acmpif2,"maap":ctrl_arms.arm_maap,"maap_if2":ctrl_arms.arm_maap_if2}
for defect in selected:
 src,stack=m.plant(defect,out)
 tree=b.Tree(src,out/"work/build",reuse,build,stack)
 for name,test,needle in defect.kills():
  result=arms[name](tree)
  caught=m.caught(test,needle,result)
  rows.append({"mutant":defect.name,"arm":name,"test":test,"needle":needle,"caught":caught,"rc":result.rc})
  print(json.dumps(rows[-1]),flush=True)
  (out/f"{defect.name}-{name}.log").write_text(result.log)
(a.packet/"receipts/focused-mutation-results.json").write_text(json.dumps(rows,indent=2)+"\n")
print(f"Focused mutations: {len(selected)} mutants, {len(rows)} checks, {sum(not r['caught'] for r in rows)} escapes",flush=True)
sys.exit(any(not r["caught"] for r in rows))
