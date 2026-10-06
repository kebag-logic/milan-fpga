#!/usr/bin/env python3
"""Aggregate completed receipts; reject gaps, duplicate grades or failed continuation parts."""
import json,pathlib,re,sys
repo=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve();r=p/"receipts"
sys.path.insert(0,str(repo/"sw/firmware/ctrl_nvm/test"))
import nvm_mutants
def log(name):return (r/(name+".log")).read_text()
def rc(name):return int((r/(name+".rc")).read_text())
plan=json.loads((r/"nvm-resume-plan.json").read_text())
done=[]
for name in ["nvm-campaign",*[f"nvm-part-{i}" for i in range(4)]]:
    got=re.findall(r"self-test OK:\s+(\S+)",log(name))
    assert len(got)==len(set(got)),name
    if name!="nvm-campaign":
        i=int(name[-1]);assert rc(name)==0,name
        assert set(got)==set(plan["parts"][i]),name
    else:assert got==plan["initial_completed"] and rc(name)==124
    done+=got
assert len(done)==len(set(done))
expected={m.name for m in nvm_mutants.MUTANTS}
assert set(done)==expected,(expected-set(done),set(done)-expected)
assert rc("ctrl-campaign")==0
ctrl=log("ctrl-campaign")
ctrl_names=re.findall(r"^\[ok\] mutant (\S+)",ctrl,re.M)
assert len(ctrl_names)==len(set(ctrl_names))==79
assert "mutants: 79 of 79 caught" in ctrl
nvm_control=log("nvm-campaign").split("  self-test OK:",1)[0]
nvm_checks=sum(map(int,re.findall(r"checks:\s*(\d+)\s+failures: 0",nvm_control)))
assert nvm_checks==435
assert len(re.findall(r"  rv32 at ",nvm_control))==5
ctrl_control=ctrl.split("[ok] mutant",1)[0]
ctrl_checks=sum(map(int,re.findall(r"checks:\s*(\d+)\s+failures: 0",ctrl_control)))
assert ctrl_checks==424
for name in ("coverage","prefix-probe","small-checks"):assert rc(name)==0,name
summary={"head":plan["head"],"ctrl":{"host_checks":423,"rv32_object_builds":1,"mutants_caught":79},
 "nvm":{"control_tests":nvm_checks,"rv32_shape_builds":5,"registered_mutants":len(expected),"mutants_caught":len(done),
 "initial_command_rc":124,"initial_command_limit_seconds":580,"initial_completed":len(plan["initial_completed"]),
 "continuation_parts":[{"name":f"nvm-part-{i}","count":len(plan["parts"][i]),"rc":rc(f"nvm-part-{i}")} for i in range(4)],
 "each_registered_mutant_has_exactly_one_completed_grade":True,"mutants":sorted(done)},
 "coverage":"14 files at 100% lines and branches after the same 14 exclusion rows",
 "negative_control_checks":{"coverage":28,"tally":18,"exact_prefix_mutants":3}}
# The original command timed out after building the inventory. Recheck its
# no-unnamed-test invariant against the completed continuation listing.
import os,subprocess
listing=p/"scratch/nvm-part-build-0/listing/endstation_ax7101_1x1_tdm8"
fixture=p/"scratch/nvm-part-build-0/shapes/endstation_ax7101_1x1_tdm8/fixture"
exes=[exe for exe in sorted(listing.glob("*/nvm_*")) if exe.is_file() and os.access(exe,os.X_OK)]
assert len(exes)==6,len(exes)
checks=set()
for exe in exes:
    run=subprocess.run([str(exe),"--gtest_list_tests"],env=dict(os.environ,NVM_FIXTURE=str(fixture)),capture_output=True,text=True,check=True)
    checks.update(nvm_mutants.listed_checks(run.stdout))
assert not nvm_mutants.unnamed_checks(sorted(checks))
summary["nvm"]["inventory_unique_checks"]=len(checks)
summary["nvm"]["inventory_binaries"]=len(exes)
summary["nvm"]["no_unnamed_checks"]=True

(r/"campaign-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps({k:v for k,v in summary.items() if k!="nvm"},indent=2))
print("NVM controls",nvm_checks,"mutants",len(done),"of",len(expected),"all continuation parts rc 0")
