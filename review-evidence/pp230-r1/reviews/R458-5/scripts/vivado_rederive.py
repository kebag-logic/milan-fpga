#!/usr/bin/env python3
"""Re-derive PR #154's area and timing figures from the published Vivado runs.

usage: vivado_rederive.py <dir>
<dir> holds milan-fpga 06fe795b review-evidence/pp230-r1/author-r1/vivado/
({base,head}/{ooc-1x1,ooc-8x8,route-1x1}/baseline_hierarchy.rpt and
route-1x1/baseline_timing.rpt), fetched unchanged.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])


def rows(p):
    out = []
    for line in p.read_text().splitlines():
        c = [x.strip() for x in line.split("|")]
        if len(c) >= 11 and c[3].isdigit():
            out.append((line, c))
    return out


def srp_blocks(p):
    blocks, inside = {}, False
    for line, c in rows(p):
        if c[1] == "u_srp" and c[2] == "KL_srp_top":
            blocks["u_srp"] = (int(c[3]), int(c[5]), int(c[7])); inside = True; continue
        if inside:
            if not line.startswith("|       "):
                inside = False; continue
            blocks[c[1]] = (int(c[3]), int(c[5]), int(c[7]))
    return blocks


for s in ("base", "head"):
    for e in ("ooc-1x1", "ooc-8x8", "route-1x1"):
        r = rows(root / s / e / "baseline_hierarchy.rpt")
        top = r[0][1]
        b = srp_blocks(root / s / e / "baseline_hierarchy.rpt")
        print(f"{s} {e}: top {top[1]} LUT {top[3]} FF {top[7]} RAMB36/18 {top[8]}/{top[9]} DSP {top[10]}; "
              f"u_srp LUT {b['u_srp'][0]} (LUTRAM {b['u_srp'][1]}) FF {b['u_srp'][2]}")
    t = (root / s / "route-1x1" / "baseline_timing.rpt").read_text()
    m = re.search(r"WNS\(ns\).*?\n\s*-+.*\n\s*(\S+)\s+(\S+)\s+\S+\s+\S+\s+(\S+)", t)
    print(f"{s} route-1x1 timing: WNS {m.group(1)} TNS {m.group(2)} WHS {m.group(3)}; "
          f"{'all constraints met' if 'All user specified timing constraints are met.' in t else 'NOT MET'}")
print("per-context (8x8 - 1x1) / 7, LUT / FF:")
for s in ("base", "head"):
    a = srp_blocks(root / s / "ooc-1x1" / "baseline_hierarchy.rpt")
    z = srp_blocks(root / s / "ooc-8x8" / "baseline_hierarchy.rpt")
    print("  " + s + ": " + "; ".join(f"{k} {(z[k][0]-a[k][0])/7:.1f}/{(z[k][2]-a[k][2])/7:.1f}" for k in a))
    tla = sum(a[k][0] for k in ("u_talker", "u_listener", "u_admission"))
    tlf = sum(a[k][2] for k in ("u_talker", "u_listener", "u_admission"))
    tza = sum(z[k][0] for k in ("u_talker", "u_listener", "u_admission"))
    tzf = sum(z[k][2] for k in ("u_talker", "u_listener", "u_admission"))
    print(f"  {s}: talker+listener+admission 1x1 {tla} LUT {tlf} FF; 8x8 {tza} LUT {tzf} FF")
