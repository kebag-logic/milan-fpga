#!/usr/bin/env python3
"""Independent re-check of the published map.json against the route-1x1 record.

Usage: check_map_json.py <map.json> <pp_resource_baseline.json> <blocks_ranked.tsv> <rows_all.tsv>
Recomputes, without importing the lane's scripts: leaf partition sums, per-parent
ancestry (additive columns exact, LUT columns non-positive adjustment), the
record totals and every recorded processor scope, block counts, and the
rest-of-datapath and SoC-side splits the page quotes.
"""
import json, sys
mp, bl, rk, ra = sys.argv[1:5]
m = json.load(open(mp)); r = json.load(open(bl))["endpoints"]["route-1x1"]["record"]
t, root, leaves = m["table"], m["root"], m["leaves"]
fails = []
cols = ("LUT", "logic_LUT", "LUTRAM", "SRL", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4", "IOB_FF")
kids = {}
for k in t:
    if "/" in k: kids.setdefault(k.rsplit("/", 1)[0], []).append(k)
assert sorted(leaves) == sorted(k for k in t if k not in kids), "leaf set"
for c in ("FF", "RAMB36", "RAMB18", "DSP", "CARRY4", "IOB_FF"):
    for p, ks in kids.items():
        if t[p][c] != sum(t[k][c] for k in ks): fails.append(f"ancestry {p} {c}")
adj = {p: t[p]["LUT"] - sum(t[k]["LUT"] for k in ks) for p, ks in kids.items()}
pos = {p: a for p, a in adj.items() if a > 0}
if pos: fails.append(f"positive LUT adjustment {pos}")
nz = {p.removeprefix(root + "/"): a for p, a in adj.items() if a}
for c, want in (("LUT", 50767), ("FF", 59634), ("RAMB36", 79), ("RAMB18", 27), ("DSP", 14), ("CARRY4", 3506)):
    if t[root][c] != want or r["figures"][c] != want: fails.append(f"total {c} {t[root][c]} rec {r['figures'][c]}")
if abs(t[root]["SLICE"] - r["figures"]["SLICE"]) > 1e-6: fails.append("slice")
if abs(sum(t[l]["SLICE"] for l in leaves) - 15832) > 1e-6: fails.append("slice shares")
w = f"{root}/milan_datapath/pp_shadow"
nscope = 0
for s, vals in r["scopes"].items():
    key = w if s == "wrapper" else f"{w}/{s}"
    if key not in t: fails.append(f"scope missing {s}"); continue
    nscope += 1
    for c, v in vals.items():
        if t[key][c] != v: fails.append(f"scope {s} {c} rec {v} map {t[key][c]}")
dp = t[f"{root}/milan_datapath"]
print("leaves", len(leaves), "depth", m["depth"], "scopes matched", nscope, "of", len(r["scopes"]))
print("nonzero LUT sharing adjustments:", nz)
print("rest of datapath LUT/FF/slices", dp["LUT"] - t[w]["LUT"], dp["FF"] - t[w]["FF"], round(dp["SLICE"] - t[w]["SLICE"], 1))
print("SoC side LUT", t[root]["LUT"] - dp["LUT"])
# rest-of-datapath blocks under 1,100 LUT (summary claim): direct children of milan_datapath
direct = [k for k in kids[f"{root}/milan_datapath"]]
big = sorted(((t[k]["LUT"], k.removeprefix(root + "/")) for k in direct), reverse=True)
print("datapath direct children", len(direct), "top5", big[:5])
others = [x for x in big if not x[1].endswith(("pp_shadow", "u_gptp_shadow", "/csr", "/@own"))]
print("others (excl pp, gptp, csr, @own):", len(others), "max", others[0])
rows = [l.split("\t") for l in open(rk).read().splitlines()]
print("blocks_ranked rows", len(rows) - 1)
print("FAILURES" if fails else "ALL CHECKS PASS", fails)
sys.exit(1 if fails else 0)
