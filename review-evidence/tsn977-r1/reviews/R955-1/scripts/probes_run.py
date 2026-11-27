#!/usr/bin/env python3
"""Run reviewer probes against the acmp, acmp_wide and acmp_walk arms, reusing the head's mutation baseline.
Usage: probes_run.py TREE BASELINE PROBES_JSON WORK OUT_JSON JOBS"""
import json, shutil, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
tree, baseline, probes, work, out, jobs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5]), int(sys.argv[6])
sys.path.insert(0, str(tree / "scripts"))
import mutation as M
from assertion_forms import package_flags
ld = package_flags("--libs")
ARMS = ["acmp", "acmp_wide", "acmp_walk"]
items = [{"name": "r-control-unmutated", "old": "", "new": ""}] + json.loads(probes.read_text())
known = {m["name"]: m for m in json.loads((tree / "tests/mutations.json").read_text())}
items.append(dict(known["acmp-nothing-persisted"], name="r-control-planted-acmp-nothing-persisted"))
def one(p):
    d = work / p["name"]; shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    src = (tree / "src/acmp.c").read_text()
    if p["old"]:
        assert src.count(p["old"]) == 1, p["name"]
        src = src.replace(p["old"], p["new"])
    (d / "acmp.c").write_text(src)
    res = {"name": p["name"], "arms": {}}
    for arm in ARMS:
        log = []
        obj, binary = d / (arm + ".o"), d / arm
        if M.run(["gcc", *M.cflags(arm), "-I" + str(tree / "include"), "-c", str(d / "acmp.c"), "-o", str(obj)], log):
            res["arms"][arm] = {"build": "FAILED", "log": "".join(log)[-2000:]}; continue
        if M.run(["g++", str(obj), str(baseline / (arm + ".cpp.o")), str(baseline / "main.o"), *M.wide(arm), *ld, "-o", str(binary)], log):
            res["arms"][arm] = {"build": "LINK FAILED", "log": "".join(log)[-2000:]}; continue
        rc, failures, count = M.execute(binary, d / (arm + ".xml"), log)
        res["arms"][arm] = {"rc": rc, "tests": count, "failed": sorted(failures)}
        (d / (arm + ".log")).write_text("".join(log))
    res["killed"] = any(a.get("failed") or a.get("rc") not in (0, None) for a in res["arms"].values())
    res["killers"] = sorted({t for a in res["arms"].values() for t in a.get("failed", [])})
    print(("KILLED  " if res["killed"] else "SURVIVED"), p["name"], len(res["killers"]), flush=True)
    return res
with ThreadPoolExecutor(jobs) as pool:
    results = list(pool.map(one, items))
out.write_text(json.dumps(results, indent=1) + "\n")
print(sum(r["killed"] for r in results), "killed of", len(results))
