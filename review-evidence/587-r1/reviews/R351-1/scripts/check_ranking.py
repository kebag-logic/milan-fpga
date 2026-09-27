#!/usr/bin/env python3
"""Internal-consistency check of the committed 50 MHz ranking against its manifest.

Usage: check_ranking.py REPO
Checks: measurement labels, children + reconciliation == total in every column,
zero storage/DSP reconciliation, LUT/FF ranks follow the maintained ordering,
and each @total equals the manifest metric for the same scope.
"""
import csv, json, sys
from collections import defaultdict
from pathlib import Path
repo = Path(sys.argv[1])
F = ("LUT", "logic_LUT", "LUTRAM", "SRL", "FF", "RAMB36", "RAMB18", "DSP")
rows = list(csv.DictReader(open(repo / "docs/findings/PP_SHADOW_BASELINE_50MHZ_RANKING.tsv"), delimiter="\t"))
man = json.loads((repo / "docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json").read_text())
errs = []
groups = defaultdict(list)
for r in rows:
    groups[(r["measurement"], r["scope"])].append(r)
print("measurements:", sorted({r["measurement"] for r in rows}), "rows:", len(rows))
for (meas, scope), rs in groups.items():
    kids = [r for r in rs if r["instance"] not in ("@reconciliation", "@total")]
    rec = [r for r in rs if r["instance"] == "@reconciliation"]
    tot = [r for r in rs if r["instance"] == "@total"]
    if len(rec) != 1 or len(tot) != 1:
        errs.append(f"{meas}/{scope}: reconciliation/total count"); continue
    for f in F:
        s = sum(int(k[f]) for k in kids) + int(rec[0][f])
        if s != int(tot[0][f]): errs.append(f"{meas}/{scope} {f}: {s} != {tot[0][f]}")
    for f in ("FF", "RAMB36", "RAMB18", "DSP"):
        if int(rec[0][f]): errs.append(f"{meas}/{scope}: nonzero {f} reconciliation")
    lut = sorted(kids, key=lambda k: (-int(k["LUT"]), k["instance"]))
    ff = sorted(kids, key=lambda k: (-int(k["FF"]), k["instance"]))
    for i, k in enumerate(lut, 1):
        if int(k["LUT_rank"]) != i: errs.append(f"{meas}/{scope}/{k['instance']} LUT_rank")
    for i, k in enumerate(ff, 1):
        if int(k["FF_rank"]) != i: errs.append(f"{meas}/{scope}/{k['instance']} FF_rank")
    variant = meas.split("-")[0]
    key = "milan_datapath/pp_shadow" + ("" if scope == "wrapper" else "/" + scope)
    metric = man["measurements"][variant]["metrics"].get(key)
    if metric:
        for f in F:
            if int(tot[0][f]) != metric[f]: errs.append(f"{meas}/{scope} total {f} {tot[0][f]} != manifest {metric[f]}")
    else:
        errs.append(f"{meas}/{scope}: no manifest metric")
    print(f"{meas}/{scope}: {len(kids)} children, total LUT {tot[0]['LUT']}")
print("errors:", len(errs)); [print(" ", e) for e in errs]
sys.exit(1 if errs else 0)
