#!/usr/bin/env python3
"""Remove the actual reentry refusal, then require the named debug check to fail."""
import argparse,json,pathlib,sys
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args();src=a.source.resolve();pkt=a.packet.resolve()
sys.path.insert(0,str(src/"sw/firmware/ctrl/test"))
import ctrl_mutants as cm,ctrl_build as cb,ctrl_arms as ca,fw_gtest
m=cm.Mutant("review-guard-removed","maap/maap.c","if (m->in_call) {","if (false && m->in_call) {","maap_debug","MaapDebug.SynchronousExpiryAsserts","debug reentry assertion")
root=pkt/"scratch/guard-removal";root.mkdir(parents=True,exist_ok=True)
tree=cb.Tree(cm.plant(m,root),root/"build",root/"reuse",fw_gtest.Build(jobs=2))
try:out=ca.arm_maap_debug(tree)
except cb.Refusal as exc:out=cb.Outcome("maap_debug",2,str(exc))
log=out.log.replace(str(src),"<source>").replace(str(pkt),"<packet>")
(pkt/"receipts/reentry-guard-removed.log").write_text(log)
record={"mutation":m.name,"arm_rc":out.rc,"named_check":m.test,"caught":cm.caught(m.test,m.needle,out)}
(pkt/"receipts/reentry-guard-removed.json").write_text(json.dumps(record,indent=2)+"\n");print(record)
raise SystemExit(0 if record["caught"] else 1)
