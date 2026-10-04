#!/usr/bin/env python3
"""Re-derive the PR #154 / 10 §5.1 area and timing figures from the published Vivado receipts
(milan-fpga 06fe795b, review-evidence/pp230-r1/author-r1/vivado). usage: vivado_rederive.py <vivado dir>"""
import re, sys
from pathlib import Path
V = Path(sys.argv[1])
def row(path, inst):
    lines = Path(path).read_text().splitlines()
    if inst != "u_srp":   # a sub-instance: scan only the u_srp block (other blocks reuse names such as u_listener)
        k = next(i for i, l in enumerate(lines) if re.match(r'^\|\s+u_srp\s+\|', l))
        lines = lines[k + 1:k + 12]
    for l in lines:
        if re.match(r'^\|\s+' + re.escape(inst) + r'\s+\|', l):
            c = [x.strip() for x in l.strip('|').split('|')]
            return int(c[2]), int(c[4]), int(c[6])          # total LUT, LUTRAM, FF
    raise SystemExit(f"{inst} not in {path}")
def util(path, name):
    for l in Path(path).read_text().splitlines():
        if re.match(r'^\|\s+' + re.escape(name) + r'\*?\s+\|', l):
            return int(l.split('|')[2])
def wns(path):
    t = Path(path).read_text().splitlines()
    for i, l in enumerate(t):
        if re.match(r'^\s+WNS\(ns\)', l):
            v = t[i + 2].split(); return float(v[0]), float(v[4])
for s in ("base", "head"):
    r = V / s / "route-1x1"
    lut, lr, ff = row(r / "alinx_ax7101_utilization_hierarchical_place.rpt", "u_srp")
    w, h = wns(r / "baseline_timing.rpt")
    print(f"route {s}: LUT {util(r/'baseline_utilization.rpt','Slice LUTs')} FF {util(r/'baseline_utilization.rpt','Slice Registers')} "
          f"u_srp LUT {lut} (LUTRAM {lr}) FF {ff}  WNS {w:+.3f} WHS {h:+.3f}")
    for o in ("1x1", "8x8"):
        d = V / s / f"ooc-{o}"
        w, h = wns(d / "baseline_timing.rpt")
        print(f"ooc {o} {s}: LUT {util(d/'baseline_utilization.rpt','Slice LUTs')} FF {util(d/'baseline_utilization.rpt','Slice Registers')} "
              f"u_srp {row(d/'baseline_hierarchy.rpt','u_srp')} WNS(est) {w:+.3f}")
print("marginal per context, (8x8 - 1x1) / 7, LUT / FF:")
for inst in ("u_talker", "u_listener", "u_admission", "u_decoder", "u_vlan", "(u_srp)", "u_srp"):
    out = []
    for s in ("base", "head"):
        a = row(V / s / "ooc-1x1" / "baseline_hierarchy.rpt", inst)
        b = row(V / s / "ooc-8x8" / "baseline_hierarchy.rpt", inst)
        out.append(f"{s} {(b[0]-a[0])/7:.1f} / {(b[2]-a[2])/7:.1f}")
    print(f"  {inst:12s} " + "   ".join(out))
