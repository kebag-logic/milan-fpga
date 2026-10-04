#!/usr/bin/env python3
"""Re-derive the #230 u_srp sub-block figures and (8x8-1x1)/7 marginal costs
from the published Vivado hierarchical utilization reports."""
import re, sys, os
root = sys.argv[1]  # .../author-r1/vivado
blocks = ["u_srp", "(u_srp)", "u_admission", "u_decoder", "u_domain",
          "u_encoder", "u_listener", "u_talker", "u_vlan"]
def parse(p):
    out = {}; insrp = False
    for line in open(p):
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 9: continue
        inst, mod = cells[1], cells[2]
        if mod == "KL_srp_top" and inst == "u_srp": insrp = True
        if insrp and inst in blocks and mod.startswith("KL_srp"):
            out[inst] = (int(cells[3]), int(cells[5]), int(cells[7]))  # total LUT, LUTRAM, FF
        if insrp and mod and not mod.startswith("KL_srp"): insrp = False
    return out
res = {}
for side in ("base", "head"):
    for shp in ("ooc-1x1", "ooc-8x8"):
        res[(side, shp)] = parse(os.path.join(root, side, shp, "baseline_hierarchy.rpt"))
for side in ("base", "head"):
    print(f"== {side}")
    for b in blocks:
        a, c = res[(side, "ooc-1x1")].get(b), res[(side, "ooc-8x8")].get(b)
        print(f"{b:14s} 1x1 LUT/LUTRAM/FF {a}  8x8 {c}  per-ctx LUT {(c[0]-a[0])/7:.1f} FF {(c[2]-a[2])/7:.1f}")
for side in ("base", "head"):
    r1, r8 = res[(side, "ooc-1x1")], res[(side, "ooc-8x8")]
    tk = [(r8["u_talker"][i]-r1["u_talker"][i])/7 for i in (0,2)]
    ad = [(r8["u_admission"][i]-r1["u_admission"][i])/7 for i in (0,2)]
    ls = [(r8["u_listener"][i]-r1["u_listener"][i])/7 for i in (0,2)]
    wh = [(r8["u_srp"][i]-r1["u_srp"][i])/7 for i in (0,2)]
    print(f"{side}: talker {tk} adm {ad} talker+adm {[tk[0]+ad[0], tk[1]+ad[1]]} listener {ls} whole {wh}")
