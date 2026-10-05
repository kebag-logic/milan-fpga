#!/usr/bin/env python3
"""Recheck merge equality, unchanged build inputs, port counts, and policy."""
import argparse, ast, hashlib, json, os, subprocess, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("source",type=Path);a=p.parse_args();root=a.source.resolve()
env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"}
def git(*args):return subprocess.check_output(["git","-C",str(root),*args],env=env).decode().strip()
head="3880c1eb6e2f927a07f98150d5b05a228f8f4efd";r1="42f654478c11bd8f2b070969d83140587190f276";dev="fa450d301805881ad713b67521477bf042ddadfd"
assert git("rev-parse","HEAD")==head
merge=git("merge-tree","--write-tree",head+"^1",head+"^2");assert merge==git("rev-parse",head+"^{tree}")
prior=git("merge-tree","--write-tree",r1,dev);assert prior=="57cc8b8afa04c315e99e5aa2f4bb84469f24df06"
model_paths=["hdl","tb/verilator","sw/firmware","configs","syn","sw/litex","protocol-processor","gptp-processor","third_party","scripts"]
assert not git("diff","--name-only",prior,head,"--",*model_paths)
comment_only=[]
for path in ["avdecc/gen_aemi_image.py","sw/builder/test_builder.py"]:
 before=git("show",prior+":"+path);after=(root/path).read_text()
 assert ast.dump(ast.parse(before),include_attributes=False)==ast.dump(ast.parse(after),include_attributes=False)
 comment_only.append(path)
source_paths=["scripts/pp_srcs.py","syn/ooc/dp_srcs.py","syn/ooc/pp_resource_gate.py","syn/ooc/pp_baseline.py","syn/ooc/pp_baseline.tcl","syn/ooc/pp_shadow_ooc.tcl","tb/verilator/milan_dp/Makefile","syn/yosys/run.sh","syn/yosys/ooc.sh","sw/litex/milan_soc.py","sw/firmware","configs","protocol-processor","gptp-processor","third_party/verilog-axis"]
assert not git("diff","--name-only",r1,head,"--",*source_paths)
rtl=git("diff","--name-only",r1,head,"--","hdl").splitlines();assert rtl==["hdl/milan/KL_nvm_backend.sv"]
sys.path.insert(0,str(root/"scripts"));from sv_ports import declarations
pins=["631eeb342ca1e3fa80e734077a56a943aee76ff1","ead8036035affd53ef4b29979190f2f4f67084c0"]
ports=[];params=[]
for pin in pins:
 txt=git("-C",str(root/"protocol-processor"),"show",pin+":hdl/top/protocol_processor_top.sv")
 rows=list(declarations(txt));ports.append([n for m,n,d,w,k in rows if m=="protocol_processor_top" and k=="port"]);params.append([n for m,n,d,w,k in rows if m=="protocol_processor_top" and k=="param"])
assert ports[0]==ports[1] and len(ports[0])==212
assert set(params[1])-set(params[0])=={"NVM_MEM_TMO_CYC_P"}
old=json.loads(git("show","506d91db:syn/ooc/pp_resource_baseline.json"));new=json.loads((root/"syn/ooc/pp_resource_baseline.json").read_text())
for name,e in new["endpoints"].items():
 olde=old["endpoints"][name]
 for k in ("tolerance","floor","ceiling"):assert e.get(k)==olde.get(k),(name,k)
 for k in ("identity","kind"):assert e["record"][k]==olde["record"][k],(name,k)
print(json.dumps({"result":"PASS","head":head,"tree":merge,"clean_remerge_equal":True,"prior_reviewed_candidate_tree":prior,"gptp_model_input_paths_unchanged":model_paths,"python_ast_equal":comment_only,"round2_build_inputs_unchanged":source_paths,"round2_only_parent_rtl_delta":rtl,"ports":212,"parameter_counts":[len(p) for p in params],"added_parameter":"NVM_MEM_TMO_CYC_P","baseline_policy_and_identity_equal":True},indent=2))
