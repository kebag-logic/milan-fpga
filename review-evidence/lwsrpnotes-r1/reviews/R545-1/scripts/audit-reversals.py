#!/usr/bin/env python3
"""Audit saved campaign receipts against every exact-head reversal definition."""
import json, re, runpy, shutil, subprocess, sys
from pathlib import Path
packet=Path(__file__).resolve().parents[1]
repo=Path(sys.argv[1]).resolve()
ns=runpy.run_path(str(repo/"tests/check_reversals.py"))
summary=[]
for profile in ["OFF","ON"]:
    work=packet/"scratch"/("reversals-"+profile)
    dest=packet/"receipts"/"reversals"/profile
    dest.mkdir(parents=True,exist_ok=True)
    records=json.loads((work/"commands.json").read_text())
    bylabel={x["label"]:x for x in records}
    for f in work.glob("*.log"):shutil.copy2(f,dest/f.name)
    shutil.copy2(work/"commands.json",dest/"commands.json")
    for label,path,old,new,kind in ns["CASES"]:
        log=(work/(label+".log")).read_text()
        observed=sorted(set(re.findall(r"Failure: \S+ -> (\w+)",log)))
        required=ns["REQUIRED_FAILURES"].get(label,[])
        item={"profile":profile,"reversal":label,"kind":kind,"rc":bylabel[label]["rc"],
              "required_failed_tests":required,"observed_failed_tests":observed}
        if kind=="unit":
            item["build_rc"]=bylabel[label+"-build"]["rc"]
            item["verified"]=item["build_rc"]==0 and item["rc"]!=0 and bool(observed) and set(required)<=set(observed)
        elif kind=="strict":item["verified"]=item["rc"]!=0 and "uninitialized" in log
        elif kind=="embedded":item["verified"]=item["rc"]!=0 and "undefined reference" in log and "shlan_connect" in log
        else:item["verified"]=item["rc"]!=0 and "hosted headers" in log
        assert item["verified"],item
        if label=="milan-delayed-in-leave":assert "leave_in_lv_keeps_the_original_deadline" not in observed
        if label=="milan-restarted-lv-deadline":assert not any("leave_in_is_immediate" in name for name in observed)
        summary.append(item)
    for label in ["configure","baseline-build","baseline-check","restored-build","restored-check"]:
        assert bylabel[label]["rc"]==0,(profile,label)
    files=subprocess.check_output(["git","-C",str(repo),"ls-files","src","tests","CMakeLists.txt"],text=True).splitlines()
    for rel in files:
        original=repo/rel; copy=work/"source"/rel
        assert copy.read_bytes()==original.read_bytes(),(profile,rel)
        assert copy.stat().st_mode&0o777==original.stat().st_mode&0o777,(profile,rel)
    print(profile,len(ns["CASES"]),"verified; all named failures confirmed; baseline and restoration pass; copied bytes/modes match")
(packet/"receipts"/"reversal-audit.json").write_text(json.dumps(summary,indent=2)+"\n")
