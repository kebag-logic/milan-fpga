#!/usr/bin/env python3
"""Check every notification-control anchor and the refreshed patch contexts.
This is a planting audit, not a full mutation campaign.
"""
import importlib.util, json, pathlib, shutil, subprocess, sys, tempfile
repo, packet = map(lambda x:pathlib.Path(x).resolve(),sys.argv[1:])
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location("review_notify_mutants",repo/"tb/pp_top/notify_mutants.py")
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
records=[]
with tempfile.TemporaryDirectory(dir=packet/"scratch",prefix="plant-") as td:
    tree=pathlib.Path(td)
    for arm in m.MUTANTS:
        for rel,_,_ in arm.edits:
            dst=tree/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(repo/rel,dst)
        refusal=m.plant(tree,arm.edits)
        records.append({"arm":arm.name,"refusal":refusal})
patches=["tb/adp_engine/mutations/cfg-nonzero-for-valid.patch", "tb/adp_engine/mutations/cfg-overlay-only.patch", "tb/pp_top/mutations/fanout-never-ends.patch"]
for patch in patches:
    r=subprocess.run(["git","apply","--check",patch],cwd=repo,capture_output=True,text=True)
    records.append({"patch":patch,"rc":r.returncode,"output":r.stdout+r.stderr})
(packet/"receipts/plant-audit.json").write_text(json.dumps(records,indent=2)+"\n")
bad=sum(bool(x.get("refusal") or x.get("rc",0)) for x in records)
print(len(m.MUTANTS),"notification arms;",len(patches),"refreshed patches;",bad,"refusals")
sys.exit(bool(bad))
