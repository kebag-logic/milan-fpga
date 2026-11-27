#!/usr/bin/env python3
"""Repeat prior failed gate causes and merge scheduling checks, without a builder bank."""
import concurrent.futures,json,os,pathlib,subprocess
import yaml
OUT=pathlib.Path(__file__).resolve().parent
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(OUT/"scratch/probes"))
w=yaml.safe_load(pathlib.Path(".github/workflows/docs.yml").read_text())
step=next(s for job in w["jobs"].values() for s in job["steps"] if "python3 scripts/docs_inventory.py --check" in s.get("run",""))
cmds=[("docs-inventory-workflow",["bash","--noprofile","--norc","-e","-o","pipefail","-c",step["run"]]),("tap-clock-docs",["python3","-B","-c",'import sys; sys.path.insert(0,"sw/builder"); import test_clock_contract as t; t.test_tap_clock_docs(); print("PASS configured tap clock table")']),("scheduling-controls",["python3","-B","scripts/suite_shards.py","--selftest"])]
def run(item):
    n,c=item
    with (OUT/(n+".log")).open("w") as log:
        r=subprocess.run(c,env=ENV,stdout=log,stderr=subprocess.STDOUT)
    (OUT/(n+".rc")).write_text(str(r.returncode)+"\n")
    print(n,r.returncode,flush=True)
    return {"name":n,"command":c,"exit":r.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    rows=list(pool.map(run,cmds))
(OUT/"gate-followup-results.json").write_text(json.dumps(rows,indent=2)+"\n")
raise SystemExit(int(any(r["exit"] for r in rows)))
