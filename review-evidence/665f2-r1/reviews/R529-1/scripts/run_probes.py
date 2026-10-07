#!/usr/bin/env python3
"""Build unchanged firmware with reviewer-owned regression probes."""
import argparse,json,os,pathlib,sys
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args();src=a.source.resolve();pkt=a.packet.resolve()
sys.path.insert(0,str(src/"sw/firmware/ctrl/test"))
import ctrl_build as cb, fw_gtest
out=pkt/"scratch"/"probes";out.mkdir(parents=True,exist_ok=True);results=[]
for n in (1,2):
 root=out/str(n);tree=cb.Tree(cb.CTRL,root,root/"reuse",fw_gtest.Build(jobs=2));extra=()
 if n==2:
  result=cb.run([sys.executable,str(src/"sw/mailbox/gen_mailbox.py"),"--variant-interfaces","2","--out",str(root/"gen")]);assert result.returncode==0
  extra=("-include" + str(root / "gen/mbx_contract.h"),)
 objs=cb.compile_c(tree,cb.sources(tree,cb.PORTABLE),"firmware",extra)
 objs+=cb.compile_c(tree,cb.sources(tree,cb.HOST),"host",extra,measured=False)
 objs+=fw_gtest.compile_tests(tree.build,[*cb.includes(tree),*extra],[pkt/"scripts/review_probes.cpp"],root/"tests")
 exe=cb.link(tree,"review_probes",objs);outcome=cb.execute("review-probes",exe)
 log=outcome.log.replace(str(src),"<source>").replace(str(pkt),"<packet>")
 (pkt/"receipts"/f"review-probes-if{n}.log").write_text(log)
 results.append({"interfaces":n,"rc":outcome.rc,"failure_lines":[x for x in log.splitlines() if "[FAIL]" in x]});print(log,flush=True)
(pkt/"receipts"/"review-probes.json").write_text(json.dumps(results,indent=2)+"\n")
assert all(x["rc"]==1 and len(x["failure_lines"])==1 and "accepted MAAP RX" in x["failure_lines"][0] for x in results)
print("DEFECT REPRODUCED at one and two interfaces; runtime enable-bit control passes")
