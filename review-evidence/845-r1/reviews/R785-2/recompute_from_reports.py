#!/usr/bin/env python3
"""Recompute each endpoint's figures and sub-block scopes from the published Vivado reports, with the gate's own
parsers, and compare them with the record. CARRY4 needs the cell census, which is not published.
usage: recompute_from_reports.py <repo> <receipts-root>"""
import json, re, sys
from pathlib import Path
repo, root = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_resource_gate as g
from pp_baseline_rank import hierarchy
base = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]
sets = {"route-1x1": ("route", root/"a738d/receipts/gate/route-selected", "route-1x1-ETO"),
        "ooc-1x1": ("ooc", root/"a738c/receipts/gate/ooc", "ooc-1x1"),
        "ooc-8x8": ("ooc", root/"a738d/receipts/gate/ooc8", "ooc-8x8")}
bad = 0
for ep, (kind, folder, stem) in sets.items():
    rec = base[ep]["record"]
    util = (folder/f"{stem}-baseline_utilization.rpt").read_text()
    fig = g.utilization(util, kind)
    tt = (folder/f"{stem}-timing-design-tables.txt").read_text()
    try:
        fig.update(g.timing(tt))
    except Exception as e:
        print(ep, "timing parser:", e)
    wrong = {k: (fig[k], rec["figures"][k]) for k in fig if fig[k] != rec["figures"][k]}
    ident = {"tool": re.match(r"(.+? Build \d+)", g.header(util, "Tool Version"))[1], "device": g.header(util, "Device"),
             "design": g.header(util, "Design"), "state": g.header(util, "Design State")}
    wrong_id = {k: (ident[k], rec["identity"][k]) for k in ident if ident[k] != rec["identity"][k]}
    rows = hierarchy(folder/f"{stem}-baseline_hierarchy.rpt")
    r = g.ROOTS[kind]; sc = {}
    for key, c in rows.items():
        if (key == r or key.startswith(r+"/")) and not key.endswith("/@own") and key.count("/") <= r.count("/")+3:
            sc[key.removeprefix(r).lstrip("/") or "wrapper"] = {n: c[n] for n in ("LUT","FF","RAMB36","RAMB18","DSP")}
    miss = sorted(set(sc) ^ set(rec["scopes"]))
    diff = [k for k in sc if k in rec["scopes"] and any(sc[k][n] != rec["scopes"][k][n] for n in sc[k])]
    print(f"{ep}: figures read {len(fig)}, differ {wrong or 'none'}; identity differ {wrong_id or 'none'}; scopes {len(sc)} of {len(rec['scopes'])}, set-difference {miss or 'none'}, count-difference {diff or 'none'}")
    bad += bool(wrong or wrong_id or miss or diff)
print("RESULT", "EQUAL" if not bad else "DIFFERENT")
sys.exit(1 if bad else 0)
