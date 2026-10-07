#!/usr/bin/env python3
"""Independent merge-sensitive controls; only disposable copies are mutated."""
import argparse, os, shutil, subprocess, sys
from pathlib import Path
from unittest.mock import patch
ap=argparse.ArgumentParser(); ap.add_argument("mode",choices=["maap","rv32"]); ap.add_argument("--repo",type=Path,required=True); ap.add_argument("--out",type=Path,required=True); ap.add_argument("--jobs",type=int,default=4); a=ap.parse_args()
root=a.repo.resolve(); out=a.out.resolve(); out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(root/"sw/firmware/ctrl/test"))
import ctrl_arms, ctrl_build, ctrl_mutants, fw_gtest, fw_rv32
build=fw_gtest.Build(jobs=a.jobs)
def tree(src,tag): return ctrl_build.Tree(src,out/tag,out/"reuse",build)
def receipt(name,result):
 (out/(name+".log")).write_text(result.log)
 print("CASE",name,"rc",result.rc,flush=True); print(result.log,flush=True)
 return result

def copy(tag,edits):
 dst=out/tag/"ctrl"; shutil.copytree(ctrl_build.CTRL,dst,ignore=shutil.ignore_patterns("__pycache__"))
 for path,old,new in edits:
  f=dst/path; s=f.read_text(); assert s.count(old)==1,(tag,path,s.count(old)); f.write_text(s.replace(old,new))
 return dst
if a.mode=="maap":
 baseline=tree(ctrl_build.CTRL,"baseline")
 for name,fn in (("maap",ctrl_arms.arm_maap),("maap_if2",ctrl_arms.arm_maap_if2),("maap_debug",ctrl_arms.arm_maap_debug)):
  assert receipt("baseline-"+name,fn(baseline)).rc==0
 plants=[
  ("saved-range-retained","maap/maap.c","m->preferred = 0;","/* one-use preference not consumed */;",ctrl_arms.arm_maap,"MaapCore.LinkBounceDrawsAfterSuppliedRange","link bounce draws after consuming supplied range"),
  ("debug-assert-disabled","maap/maap.c","assert(!m->in_call);","assert(true);",ctrl_arms.arm_maap_debug,"MaapDebug.SynchronousExpiryAsserts","debug reentry assertion"),
  ("release-counter-removed","maap/maap.c","m->reentries++;","m->reentries += 0u;",ctrl_arms.arm_maap,"MaapCore.ReentrantPortsAreCountedAndIgnored","all input guards fire"),
 ]
 for name,path,old,new,fn,test,needle in plants:
  dst=copy(name,[(path,old,new)])
  got=receipt(name,fn(tree(dst,name+"-build")))
  assert ctrl_mutants.caught(test,needle,got),(name,"escaped or failed for another reason")
  print("CAUGHT named failure:",name,test,needle,flush=True)
 print("PASS: 3 baseline arms and 3 independently planted compiled controls")
else:
 cc=fw_rv32.compiler(); assert cc
 assert receipt("baseline-rv32",ctrl_arms.arm_rv32(tree(ctrl_build.CTRL,"baseline"),True)).rc==0
 objects=list((out/"baseline/rv32").glob("*.o"))
 names={x.name for x in objects}
 assert {"maap_maap.o","maap_maap_mbx.o","maap_maap_csr.o"}<=names,names
 print("PASS: merged RV32 set includes all three MAAP objects; total",len(objects))
 orig=(ctrl_build.CTRL/"maap/maap.c").read_text()
 plants=[("maap-unknown-runtime",orig+'\nextern void __review_unexpected_service(void);\nvoid review_runtime_probe(void) { __review_unexpected_service(); }\n'),
         ("hosted-assert-include-restored",orig.replace("#ifndef NDEBUG\n#include <assert.h>\n#endif","#include <assert.h>"))]
 for name,new in plants:
  dst=copy(name,[("maap/maap.c",orig,new)])
  if name=="maap-unknown-runtime":
   f=dst/"port/ctrl_debug.c"; f.write_text(f.read_text()+'\n__attribute__((used)) static void __review_unexpected_service(void) {}\n')
  got=receipt(name,ctrl_arms.arm_rv32(tree(dst,name+"-build"),True))
  if name=="maap-unknown-runtime":
   assert got.rc==1 and "symbols outside the C library" in got.log and "__review_unexpected_service" in got.log
  else:
   assert got.rc==1 and "assert.h" in got.log and "does not build" in got.log
  print("CAUGHT expected RV32 refusal:",name,flush=True)
 with patch.dict(os.environ,{},clear=True), patch.object(fw_rv32,"CANDIDATES",()):
  os.environ["CTRL_RV32_CC"]=cc
  old=fw_rv32.compiler()
  os.environ["MILAN_RV32_CC"]=cc
  new=fw_rv32.compiler()
 assert old is None and new==cc
 print("DOCUMENTED SELECTOR PROBE: CTRL_RV32_CC alone ignored; MILAN_RV32_CC selects requested compiler")
 print("PASS: exact-head RV32 objects and two independently planted controls; stale selector reproduced")
