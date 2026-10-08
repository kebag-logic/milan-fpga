from pathlib import Path
import os,shutil,sys
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
from ctrl_build import ROOT,CTRL,Tree
from ctrl_reuse import cut_reuse
import ctrl_arms,srp_arms,fw_gtest
r=Path(__file__).resolve().parent
for cc,cxx in (("gcc","g++"),("clang","clang++")):
 os.environ.update(CC=cc,CXX=cxx)
 for sanitized in (False,True):
  label=cc+("-asan" if sanitized else "-plain")
  build=fw_gtest.Build(jobs=4,address_sanitizer=sanitized)
  for planted in (False,True):
   work=r/"asan"/label/("plant" if planted else "base");src=work/"ctrl"
   shutil.copytree(CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
   if planted:
    p=src/"acmp/acmp.c";s=p.read_text();old="cfg->n_sources > ACMP_MAX_SOURCES) {";assert s.count(old)==1
    p.write_text(s.replace(old,"cfg->n_sources > ACMP_MAX_SOURCES + 1u) {"))
   reuse=work/"reuse";cut_reuse(reuse)
   o=ctrl_arms.arm_acmp(Tree(src,work/"build",reuse,build))
   (r/(label+("-plant" if planted else "-base")+".log")).write_text(o.log)
   assert o.rc==(1 if planted else 0),(label,planted,o.log)
   assert "ERROR: AddressSanitizer" not in o.log
   if planted: assert "A0 more sources than ACMP_MAX_SOURCES" in o.log
   print(label,"planted" if planted else "base","rc",o.rc,"expected",flush=True)
  if sanitized:
   for n in (1,2):
    for suite in ("srp_mbx.cpp","srp_rx_retry.cpp","srp_app.cpp","test_acmp_mbx.cpp","srp_latency.cpp","srp_walk.cpp"):
     out=r/"asan"/label/"srp"
     o=srp_arms.arm_srp(Tree(CTRL,out,out/"reuse",build),ROOT/"third_party/lwSRP",n,test=suite)
     (r/f"{label}-{suite}-if{n}.log").write_text(o.log)
     assert o.rc==0,(label,n,suite,o.log)
     print(label,n,suite,"PASS",flush=True)
