#!/usr/bin/env python3
"""Replay the gate's judgement from published reports, using the gate's own judge().
Part 1: report-derived candidates against the twelfth record must reproduce exit 1; against the thirteenth, exit 0.
Part 2: order and type evidence that the record is the gate's output (scopes in hierarchy-report order, key order of
RECORD, int/float types as whole()/real() return them).
Part 3: a thirteenth-record route is still comparable with a route placed at another recipe directive.
Part 4: a hand-moved policy cell or figure is refused by check-baseline.
usage: gate_replay.py <repo> <receipts-root> <scratch-dir>"""
import copy, json, re, subprocess, sys
from pathlib import Path
repo, root, tmp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(repo/"syn/ooc"))
import pp_resource_gate as g
from pp_baseline_rank import hierarchy
head = json.loads((repo/"syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]
twelfth = json.loads(subprocess.check_output(["git","-C",str(repo),"show","b16f0175ac402e124314a40d1ea9573e431684dc:syn/ooc/pp_resource_baseline.json"]))["endpoints"]
sets = {"route-1x1": ("route", root/"a738d/receipts/gate/route-selected", "route-1x1-ETO"),
        "ooc-1x1": ("ooc", root/"a738c/receipts/gate/ooc", "ooc-1x1"),
        "ooc-8x8": ("ooc", root/"a738d/receipts/gate/ooc8", "ooc-8x8")}
def tables(text):
    out = {}
    for name, body in re.findall(r"== (\S+)\n(.*?)(?=\n== |\Z)", text, re.S):
        rows = [l for l in body.splitlines() if re.match(r"\s*-?\d", l)]
        if rows:
            v = rows[0].split(); out[name] = (float(v[0]), float(v[4]))
    return out
fails = 0
for ep, (kind, folder, stem) in sets.items():
    util = (folder/f"{stem}-baseline_utilization.rpt").read_text()
    t = tables((folder/f"{stem}-timing-design-tables.txt").read_text())
    fig = g.utilization(util, kind); fig["WNS_ns"], fig["WHS_ns"] = t["baseline_timing.rpt"]
    fig["CARRY4"] = head[ep]["record"]["figures"]["CARRY4"]   # the census is not published
    rows = hierarchy(folder/f"{stem}-baseline_hierarchy.rpt"); r = g.ROOTS[kind]; sc = {}
    for key, c in rows.items():
        if (key == r or key.startswith(r+"/")) and not key.endswith("/@own") and key.count("/") <= r.count("/")+3:
            sc[key.removeprefix(r).lstrip("/") or "wrapper"] = {n: c[n] for n in ("LUT","FF","RAMB36","RAMB18","DSP")}
    rec = head[ep]["record"]
    cand = {"kind": kind, "identity": rec["identity"], "inputs_sha256": "report-derived", "figures": fig,
            "scopes": {k: {**sc[k], "CARRY4": rec["scopes"][k]["CARRY4"]} for k in sc}}
    corners = None
    if kind == "route":
        corners = {f"{m}_{j}C": dict(zip(("WNS_ns","WHS_ns"), t[f"alinx_ax7101_signoff_{m}_{j}C_timing.rpt"])) for m in ("Slow","Fast") for j in (0,85)}
    s12, l12 = g.judge(twelfth[ep], cand, [] if kind=="route" else None, None, corners)
    s13, l13 = g.judge(head[ep], cand, [] if kind=="route" else None, None, corners)
    print(f"{ep}: twelfth exit {s12}: {[l.split()[0]+' '+l.split()[-1] for l in l12 if 'REGRESSION: grew' in l]}; thirteenth exit {s13}")
    order = list(sc) == list(rec["scopes"])
    keys = list(rec) == list(g.RECORD)
    types = all(type(v) is type(twelfth[ep]["record"]["figures"][k]) for k, v in rec["figures"].items())
    print(f"  order: scopes in report order {order}; record keys in gate order {keys}; figure types as the twelfth {types}; figure key order {list(rec['figures'])==list(twelfth[ep]['record']['figures'])}")
    fails += (s12 != 1) + (s13 != 0) + (not order) + (not keys) + (not types)
    for w in ("KL_maap",):
        pass
e = head["route-1x1"]; c = copy.deepcopy(e["record"]); c["inputs_sha256"] = "other"
c["identity"]["flow"] = [l.replace("ExtraTimingOpt","ExtraPostPlacementOpt") for l in c["identity"]["flow"]]
sl = {"Slow_0C": {"WNS_ns":.198,"WHS_ns":.04}, "Fast_0C": {"WNS_ns":1.0,"WHS_ns":.015}}
s, _ = g.judge(e, c, [], None, sl); print("comparable across directive: exit", s); fails += s != 0
c2 = copy.deepcopy(c); c2["identity"]["flow"] = [l.replace("ExtraPostPlacementOpt","Default") for l in c2["identity"]["flow"]]
s, l = g.judge(e, c2, [], None, sl); print("directive outside the recipe: exit", s, l[0][:60]); fails += s != 2
base = json.loads((repo/"syn/ooc/pp_resource_baseline.json").read_text())
for name, edit in (("tolerance LUT 500->520", lambda b: b["endpoints"]["route-1x1"]["tolerance"].__setitem__("LUT", 520)),
                   ("ooc-8x8 tolerance FF 339->400", lambda b: b["endpoints"]["ooc-8x8"]["tolerance"].__setitem__("FF", 400)),
                   ("ceiling 121.5->130", lambda b: b["endpoints"]["route-1x1"]["ceiling"].__setitem__("BRAM_TILE", 130)),
                   ("record BRAM over ceiling", lambda b: b["endpoints"]["route-1x1"]["record"]["figures"].__setitem__("BRAM_TILE", 122))):
    b = copy.deepcopy(base); edit(b); p = tmp/"mut.json"; p.write_text(json.dumps(b, indent=1)+"\n")
    r = subprocess.run([sys.executable, "-B", str(repo/"syn/ooc/pp_resource_gate.py"), "check-baseline", "--baseline", str(p)], capture_output=True, text=True)
    print(f"check-baseline {name}: exit {r.returncode}"); fails += r.returncode != 2
print("RESULT", "PASS" if not fails else f"FAIL {fails}")
sys.exit(1 if fails else 0)
