import hashlib, json, os, re, subprocess
from pathlib import Path
m=Path(__file__).parent
e=Path(os.environ["EVIDENCE"])
repo=Path(os.environ["REPO"])
head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=repo,text=True).strip()
required=["all-functional","all-measurements","capture-coherence","source/all"]
for name in required:
    assert int((m/(name+".rc")).read_text())==0, name
result={"head":head,"required_rc":{n:0 for n in required},"timing":{}}
for directive in ["ExtraPostPlacementOpt","AltSpreadLogic_high","ExtraTimingOpt"]:
    row=json.loads((e/"timing-current"/directive/"timing-summary.json").read_text())
    assert row["process_rc"]==0 and row["constraint_check_rc"]==0
    assert set(row["critical_warning_codes"]) <= {"Route 35-39"}, row["critical_warning_codes"]
    result["timing"][directive]=row
result["area"]=json.loads((m/"area-route/candidate_area_comparison.json").read_text())
result["ooc"]={}
for name in ["settle_base","settle_head","cmc_base","cmc_head"]:
    p=m/"area-ooc"/("util_"+name+".rpt")
    t=p.read_text()
    counts={}
    for field in ["Slice LUTs","Slice Registers","Block RAM Tile"]:
        match=re.search(r"^\| "+re.escape(field)+r"\*?\s*\|\s*([0-9.]+)\s*\|",t,re.M)
        assert match, (name,field)
        counts[field]=float(match[1])
    result["ooc"][name]={"resources":counts,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size}
(e/"measurement-summary.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
