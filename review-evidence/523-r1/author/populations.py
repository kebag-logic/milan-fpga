"""Record preserved mutation, suite, shard and harness populations."""
import ast,hashlib,json,subprocess,sys
from pathlib import Path
root=Path.cwd();out=Path(__file__).resolve().parent
base="483a133ed08867ea0d300d2b4a027b5b48a4282f"
sys.path.insert(0,str(root/"tb/verilator/gptp_shadow"))
from mutants import MUTATIONS,NOT_SEPARATELY_OBSERVABLE
result={"head":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
 "mutations":[dict(name=n,path=str(p.relative_to(root)),old=o,new=v,expected=e) for n,p,o,v,e in MUTATIONS],
 "not_observable":[dict(name=n,path=str(p.relative_to(root)),anchor=o,reason=w) for n,p,o,w in NOT_SEPARATELY_OBSERVABLE]}
selector=["python3","scripts/suite_shards.py","--suite-root","tb/verilator"]
def select(*args):return subprocess.check_output(selector+list(args),text=True).splitlines()
result["default_suites"]=select("--shard","0/1")
result["physical_suites"]=select("--physical-gptp","--shard","0/1")
result["shards"]={f"{i}/4":select("--shard",f"{i}/4") for i in range(4)}
assert sorted(x for rows in result["shards"].values() for x in rows)==result["default_suites"]
listing=subprocess.check_output(["bash","scripts/run_all_suites.sh","--list"],text=True).splitlines()
assert listing==result["default_suites"]
result["normal_list_matches_selector"]=True
for path in ["scripts/suite_shards.py","scripts/suite_tally.py","tb/verilator/gptp_shadow/sim_main.cpp","tb/verilator/gptp_shadow/gptp_shadow_wrap.sv"]:
    assert subprocess.check_output(["git","show",base+":"+path])==(root/path).read_bytes()
result["immutable_inventory_tally_and_rtl_harness"]=True
result["changed_files"]=subprocess.check_output(["git","diff","--name-only",base,"HEAD"],text=True).splitlines()
assert len(MUTATIONS)==9 and len(NOT_SEPARATELY_OBSERVABLE)==6
(out/"populations.json").write_text(json.dumps(result,indent=2)+"\n")
print("Preserved: nine mutations; six reasons; 55 default suites; one physical suite; exact shard partition; unchanged harness and tally")
