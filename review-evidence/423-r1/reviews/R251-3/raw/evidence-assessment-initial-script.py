#!/usr/bin/env python3
"""Inspect immutable receipts and compare preserved controls; run no historical matrix."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("checkout",type=Path);p.add_argument("packet",type=Path);a=p.parse_args()
prior=a.packet/"public/reviews/R251-2/raw";manager=a.packet/"public/corrected-source3/manager";raw=a.packet/"raw"
head="4671e582cfa4bba4809b9e3a354ce5b6eb967f99";base="52711029f374650dc93830d5ea28e81cb5c8f410"
source=json.loads((manager/"source.json").read_bytes());assert source["head"]==head and source["base"]==base
banks={}
for name,count in (("manager-builder",49),("full-native",5)):
    commands=json.loads((manager/(name+".json")).read_bytes())
    results=json.loads((manager/name/"results.json").read_bytes())
    complete=json.loads((manager/name/"complete.json").read_bytes())
    assert results["head"]==head and results["base"]==base and complete["head"]==head and complete["exit_code"]==0
    assert len(results["results"])==len(commands["commands"])==count
    assert [row["command"] for row in results["results"]]==commands["commands"]
    rows=[]
    for n,r in enumerate(results["results"],1):
        assert r["exit_code"]==0,r
        log=manager/name/Path(r["log"]).name;assert log.is_file() and log.stat().st_size
        data=log.read_bytes();lines=data.decode("utf-8","replace").splitlines()
        rows.append({"number":n,"command":r["command"],"exit":r["exit_code"],"log":str(log.relative_to(a.packet)),"sha256":hashlib.sha256(data).hexdigest(),"last_lines":lines[-8:]})
    banks[name]={"head":head,"base":base,"passing_commands":len(rows),"rows":rows}
(raw/"manager-evidence-assessment.json").write_text(json.dumps(banks,indent=2)+"\n")
# Compare unchanged historical receipts with the current object's identity proof.
identity=json.loads((raw/"object-identity.json").read_bytes());assert identity["only_changed_path"]=="scripts/merge_containment_selftest_retention.py"
history=json.loads((prior/"history/history.json").read_bytes())
repo=a.checkout/"gptp-processor"
def git(*args):return subprocess.check_output(["git","--no-replace-objects","-C",str(repo),*args])
for oid,record in history["commits"].items():
    stored=git("cat-file","commit",oid)
    parents=[line.split()[1].decode() for line in stored.splitlines() if line.startswith(b"parent ")]
    tree=stored.splitlines()[0].split()[1].decode()
    assert parents==record["parents"] and tree==record["tree"],oid
    assert stored==(prior/"history"/(oid+".commit")).read_bytes(),oid
for pair in history["patch_pairs"]:
    patches=[]
    for oid in (pair["source"],pair["replay"]):
        parent=history["commits"][oid]["parents"][0]
        data=git("diff","--no-ext-diff","--no-textconv","--no-renames",parent,oid)
        assert data==(prior/"history"/(oid+".diff")).read_bytes()
        assert hashlib.sha256(data).hexdigest()==pair["sha256"]
        patches.append(data)
    assert patches[0]==patches[1]
for target in history["targets"]:
    assert target["G"] and target["H"]==[True,None]
    assert target["T_unproved"]==["'tb/tsngen/mutants.py'","'tb/verilator/gaskets/mutants.py'"]
    row=next(r for r in target["commands"] if r["label"]=="source-pr62")
    assert row["exit"]==1 and row["stdout"].split()[0]=="UNKNOWN"
matrix=json.loads((prior/"public-matrix/matrix.json").read_bytes())
assert len(matrix["rows"])==31 and all(r["as_expected"] for r in matrix["rows"])
for r in matrix["rows"]:assert [r["prototype_rc"],r["prototype"].split()[0]]==r["expected"]["prototype"]
# Compare actual current runs with original controls preserved by R251-2.
def assertions(path):
    return [line.split()[1] for line in path.read_text().splitlines() if line.startswith("  ok  ")]
original=json.loads((prior/"public-matrix/existing-arm-preservation.json").read_bytes())["names"]
previous=assertions(prior/"selftest.stdout")
record={"original_145":len(original),"r251_2_assertions":len(previous),"current":{}}
assert len(original)==145 and len(previous)==455
for encoding in ("utf-8","iso8859-1"):
    d=raw/"parent-locales"/("current-"+encoding);names=assertions(d/"full.stdout")
    assert names==previous,(encoding,"assertion names/order changed")
    assert names[:145]==original
    current=json.loads((d/"result.json").read_bytes());old=json.loads((raw/"parent-locales"/("restored-b911-"+encoding)/"result.json").read_bytes())
    assert current["runs"]==old["runs"],encoding
    assert current["fixture_name_hex"]==old["fixture_name_hex"]=="7261772dff"
    assert all(r["pass"] for r in current["rows"])
    record["current"][encoding]={"all_455_names_order_preserved":True,"original_145_pass":True,"focused_22_pass":True,"production_cli_outputs_identical_to_b911_restoration":True,"fixture_hex":"7261772dff"}
precise=[]
for f in sorted((raw/"restorations").glob("*.stdout")):
    lines=f.read_text().splitlines();names=[line.split()[1] for line in lines if line.startswith("  FAIL ")]
    assert names,f
    precise.append({"restoration":f.stem,"actual_failed_assertions":names,"count":len(names)})
(raw/"control-preservation.json").write_text(json.dumps(record,indent=2)+"\n")
(raw/"restorations/precise-failure-index.json").write_text(json.dumps(precise,indent=2)+"\n")
(raw/"accepted-prior-evidence.json").write_text(json.dumps({"covering_round":"R251-2","head":identity["ancestor"],"accepted_at":head,"untouched_production_artifacts":{n:v for n,v in identity["scope_artifacts"].items()},"public_matrix_rows":31,"all_expected_verdicts":True,"donor_commit_objects_and_raw_patches_identical":True,"patch_pairs":history["patch_pairs"],"donor_targets":[{k:t[k] for k in ("target","G","H","T_unproved")} for t in history["targets"]],"fresh_matrix_execution":False},indent=2)+"\n")
print("PASS: manager 49+5 receipts bound to source/base; prior 31-case evidence and donor object identity accepted; all 455 names/order and original 145 controls preserved in both current parents")
print(json.dumps(precise,indent=2))
