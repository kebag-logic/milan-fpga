from pathlib import Path
import sys,os
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
from ctrl_build import CTRL,ROOT,Tree
import srp_arms,fw_gtest
r=Path(__file__).resolve().parent
for cc,cxx in (("gcc","g++"),("clang","clang++")):
 os.environ.update(CC=cc,CXX=cxx)
 for n in (1,2):
  build=fw_gtest.Build(jobs=4,address_sanitizer=True)
  out=r/"park-check"/cc
  o=srp_arms.arm_srp(Tree(CTRL,out,out/"reuse",build),ROOT/"third_party/lwSRP",n,test=("test_acmp_mbx.cpp","SrpBinding.ParkedReplacementRetiresThePreviouslyAcceptedBinding"))
  print(o.log,flush=True)
  assert o.rc==0
