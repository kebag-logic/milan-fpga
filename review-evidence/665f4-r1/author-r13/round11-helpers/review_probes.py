from pathlib import Path
import importlib.util,shutil,sys,json
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
import srp_arms,fw_gtest
from ctrl_build import CTRL,ROOT,Tree
r=Path(__file__).resolve().parent
src=r/"review-positive/ctrl"
shutil.copytree(CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
p=src/"test/srp_binding.hpp"
with p.open("a") as f:
 for name in ("probe_tk_registered.hpp","probe_invalid_vid.hpp"):
  f.write("\n"+(r/"review"/name).read_text())
saved=srp_arms.HERE
srp_arms.HERE=src/"test"
for n in (1,2):
 o=srp_arms.arm_srp(Tree(src,r/"review-positive/build",r/"review-positive/reuse",fw_gtest.Build(jobs=4)),ROOT/"third_party/lwSRP",n,test=("test_acmp_mbx.cpp","SrpBinding*Probe.*"))
 (r/f"review-positive-if{n}.log").write_text(o.log)
 print(o.log,flush=True)
 assert o.rc==0
srp_arms.HERE=saved
spec=importlib.util.spec_from_file_location("review_plants",r/"review/probe_mutants.py")
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
plants=[line.split("\t") for line in (r/"review/bound_probes.tsv").read_text().splitlines()]
plants += [[name,*value] for name,value in p.PLANTS.items() if name!="control-none"]
build=fw_gtest.Build(jobs=4); records=[]
for name,path,old,new in plants:
 work=r/"review-plant-work";src=work/"ctrl"
 shutil.copytree(CTRL,src,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 target=src/path;s=target.read_text();assert s.count(old)==1,(name,s.count(old));target.write_text(s.replace(old,new))
 for n in (1,2):
  failures=0
  for suite in ("srp_app.cpp","test_acmp_mbx.cpp"):
   o=srp_arms.arm_srp(Tree(src,work/"build",work/"reuse",build),ROOT/"third_party/lwSRP",n,test=suite)
   (r/f"review-{name}-{suite}-if{n}.log").write_text(o.log)
   failures+=o.rc==1 and "[FAIL]" in o.log
  equivalent=name=="rv-poll-per-if" and n==1
  assert failures if not equivalent else failures==0,(name,n,failures)
  record=dict(plant=name,interfaces=n,result="equivalent (one interface)" if equivalent else "caught",failing_suites=failures)
  records.append(record);print(record,flush=True)
(r/"review-probes-results.json").write_text(json.dumps(records,indent=2)+"\n")
shutil.rmtree(r/"review-plant-work")
