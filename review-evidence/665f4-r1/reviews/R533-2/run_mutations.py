#!/usr/bin/env python3
"""Independent killed-defect probes in disposable copies, never source edits."""
import argparse, concurrent.futures, hashlib, json, shutil, sys, traceback
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument("source",type=Path); p.add_argument("--jobs",type=int,default=8)
a=p.parse_args(); root=a.source.resolve(); packet=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(root/"sw/firmware/ctrl/test"))
from ctrl_build import Tree, CTRL
import fw_gtest, srp_arms, ctrl_arms, srp_mutants
original=root/"third_party/lwSRP"
ctrl_arms.lwsrp_pin(original)
# Explicitly permit only these probe copies after checking the real dependency.
# The library pin is not a behavioral check and is intentionally bypassed for plants.
srp_arms.lwsrp_pin=lambda path: ctrl_arms.lwsrp_pin(original)
mutations=[
("milan-delay-in","library/src/core/mrp_mad.c",
 "if (app->ops->milan_rapid_leave && ev == MRP_EVENT_RLV &&",
 "if (false && app->ops->milan_rapid_leave && ev == MRP_EVENT_RLV &&",
 "Srp.InListenerWithdrawalRevokesLicenceImmediately:Srp.InTalkerWithdrawalImmediatelyWithdrawsListener",
 "Srp.InListenerWithdrawalRevokesLicenceImmediately","active[0]"),
("milan-restart-lv","library/src/core/mrp_mad.c",
 "    if (e->ns != MRP_REG_STATE_COUNT) {",
 "    if (ev == MRP_EVENT_RLV && ai->reg == MRP_REG_STATE_LV) {\n"
 "        shlan_timer_arm(&ai->leave_timer, priv_of(app)->ports[port_id].leave_cs);\n    }\n"
 "    if (e->ns != MRP_REG_STATE_COUNT) {",
 "Srp.LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline",
 "Srp.LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline","active[0]"),
("lifecycle-fence-exclusive","ctrl/mbx/mbx.c",
 "(uint16_t)(mark - rx_tail[ch]) < 0x8000u",
 "(uint16_t)(mark - rx_tail[ch]) > 0u && (uint16_t)(mark - rx_tail[ch]) < 0x8000u",
 "Srp.LinkEventsDiscardOnlyTheirPublishedReceivePrefix",
 "Srp.LinkEventsDiscardOnlyTheirPublishedReceivePrefix","mock function call"),
("shared-clear-on-ineligible","ctrl/srp/srp_mbx.c",
 "desired |= r->desired;",
 "desired = r->desired == 0 ? 0 : (desired | r->desired);",
 "Srp.SharedIdentityReconcilesBothBindingOrdersOnTheWire",
 "Srp.SharedIdentityReconcilesBothBindingOrdersOnTheWire","last"),
]
receipts=packet/"receipts"
def run(spec):
 name,path,old,new,selected,test,needle=spec
 work=packet/"scratch/mutations"/name
 work.mkdir(parents=True,exist_ok=True)
 shutil.copytree(CTRL,work/"ctrl",dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__"))
 shutil.copytree(original/"src",work/"library/src",dirs_exist_ok=True)
 target=work/path; source=target.read_text(); assert source.count(old)==1,(name,source.count(old))
 target.write_text(source.replace(old,new))
 record={"name":name,"path":path,"old":old,"new":new,"test":selected,
   "before_sha256":hashlib.sha256(source.encode()).hexdigest(),
   "after_sha256":hashlib.sha256(target.read_bytes()).hexdigest()}
 try:
  result=srp_arms.arm_srp(Tree(work/"ctrl",work/"build",work/"reuse",fw_gtest.Build(jobs=max(1,a.jobs//2))),
            work/"library",2,test=("srp_mbx.cpp",selected))
  record.update(rc=int(result.rc),caught=srp_mutants.caught(test,needle,result))
  (receipts/(name+".log")).write_text(result.log)
 except Exception:
  record.update(rc=2,caught=False)
  (receipts/(name+".log")).write_text(traceback.format_exc())
 (receipts/(name+".rc")).write_text(str(record["rc"])+"\n")
 return record
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for f in concurrent.futures.as_completed([pool.submit(run,s) for s in mutations]):
  r=f.result(); results.append(r); print(json.dumps(r),flush=True)
(receipts/"mutation-results.json").write_text(json.dumps(results,indent=2)+"\n")
sys.exit(0 if all(r["caught"] for r in results) else 1)
