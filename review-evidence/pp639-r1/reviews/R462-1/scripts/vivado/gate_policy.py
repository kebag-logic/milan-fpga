#!/usr/bin/env python3
"""Apply the parent gate's tolerance policy (syn/ooc/pp_resource_baseline.json at dev 241f9184,
judge() of syn/ooc/pp_resource_gate.py) to the published base and head figures.  Identity and
input-digest checks need the scratch parent and are not re-run here.
usage: gate_policy.py BASELINE_JSON VIVADO_DIR"""
import json, re, sys
from pathlib import Path
b = json.load(open(sys.argv[1]))["endpoints"]; root = Path(sys.argv[2])
GATED = {"route": ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "DSP", "WNS_ns", "WHS_ns"),
         "ooc": ("LUT", "FF", "RAMB36", "RAMB18", "DSP")}
def figs(d):
    t = (d / "baseline_utilization.rpt").read_text()
    def num(l):
        return float(re.search(r"^\|\s*" + re.escape(l) + r"\*?\s*\|\s*([\d.]+)\s*\|", t, re.M).group(1))
    f = {"LUT": num("Slice LUTs"), "FF": num("Slice Registers"), "RAMB36": num("RAMB36/FIFO"),
         "RAMB18": num("RAMB18"), "DSP": num("DSPs"), "BRAM_TILE": num("Block RAM Tile")}
    if "Slice" in t and re.search(r"^\|\s*Slice\s*\|", t, re.M):
        f["SLICE"] = num("Slice")
    lines = (d / "baseline_timing.rpt").read_text().splitlines()
    i = next(k for k, l in enumerate(lines) if l.strip().startswith("WNS(ns)"))
    x = lines[i + 2].split(); f["WNS_ns"], f["WHS_ns"] = float(x[0]), float(x[4])
    return f
def judge(entry, before, after, kind):
    st, imp, out = 0, [], []
    for g in GATED[kind]:
        tol = entry["tolerance"][g]; d = after[g] - before[g]
        fall = -d if g in ("WNS_ns", "WHS_ns") else d
        bad = fall > tol
        if g in (entry.get("floor") or {}) and after[g] < entry["floor"][g]: bad = True
        if bad: st = 1; out.append(f"{g} {before[g]:g}->{after[g]:g} REGRESSION")
        if -fall > tol: imp.append(g)
    for g, c in (entry.get("ceiling") or {}).items():
        if after[g] > c: st = 1; out.append(f"{g} over ceiling")
    return st, imp, out
for ep, kind in (("route-1x1", "route"), ("ooc-1x1", "ooc"), ("ooc-8x8", "ooc")):
    e = b[ep]; rec = e["record"]["figures"]
    base, head = figs(root / "base" / ep), figs(root / "head" / ep)
    for label, bef, aft in (("head vs base", base, head), ("base vs committed", rec, base), ("head vs committed", rec, head)):
        st, imp, out = judge(e, bef, aft, kind)
        print(f"{ep} {label}: exit {st}; re-baseline recommended: {','.join(imp) or '-'}; {'; '.join(out) or 'no regression'}")
