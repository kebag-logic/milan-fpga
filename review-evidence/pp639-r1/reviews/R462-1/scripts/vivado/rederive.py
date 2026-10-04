#!/usr/bin/env python3
"""Re-derive the PR #155 area and timing figures from the published Vivado reports.

usage: rederive.py VIVADO_DIR   (review-evidence/pp639-r1/author-r1/vivado at milan-fpga 28663f5a)
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])


def util(path: Path) -> dict:
    t = path.read_text()
    def num(label):
        m = re.search(r"^\|\s*" + re.escape(label) + r"\*?\s*\|\s*([\d.]+)\s*\|", t, re.M)
        return float(m.group(1)) if m else None
    return {"LUT": num("Slice LUTs"), "LUT_logic": num("LUT as Logic"), "LUT_mem": num("LUT as Memory"),
            "FF": num("Slice Registers"), "Slice": num("Slice"), "RAMB36": num("RAMB36/FIFO"),
            "RAMB18": num("RAMB18"), "DSP": num("DSPs")}


def timing(path: Path) -> tuple:
    lines = path.read_text().splitlines()
    i = next(k for k, l in enumerate(lines) if l.strip().startswith("WNS(ns)"))
    f = lines[i + 2].split()
    return float(f[0]), float(f[4])


def hier(path: Path) -> dict:
    rows = []
    for line in path.read_text().splitlines():
        m = re.match(r"^\|(\s*)(\S+)\s*\|\s*(\S+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|", line)
        if m:
            rows.append((len(m.group(1)), m.group(2), int(m.group(4)), int(m.group(6)), int(m.group(8)),
                         float(m.group(9))))
    out = {}
    for k, (ind, name, lut, lutram, ff, r36) in enumerate(rows):
        if name == "(u_pp)" and name not in out:
            out[name] = {"total": (lut, lutram, ff, r36), "own": (lut, lutram, ff)}
        if name in ("u_pp", "u_listener", "u_notify", "u_originator", "u_adp", "u_maap", "u_srp") and name not in out:
            kids = []
            for ind2, n2, l2, lr2, f2, r2 in rows[k + 1:]:
                if ind2 <= ind:
                    break
                if ind2 == ind + 2:
                    kids.append((l2, lr2, f2))
            own = (lut - sum(x[0] for x in kids), lutram - sum(x[1] for x in kids), ff - sum(x[2] for x in kids))
            out[name] = {"total": (lut, lutram, ff, r36), "own": own}
    return out


for e in ("route-1x1", "ooc-1x1", "ooc-8x8"):
    b, h = util(root / "base" / e / "baseline_utilization.rpt"), util(root / "head" / e / "baseline_utilization.rpt")
    tb, th = timing(root / "base" / e / "baseline_timing.rpt"), timing(root / "head" / e / "baseline_timing.rpt")
    print(f"{e}: " + "; ".join(f"{k} {b[k]:g} -> {h[k]:g} ({h[k]-b[k]:+g})" for k in b if b[k] is not None)
          + f"; WNS/WHS {tb[0]:+.3f}/{tb[1]:+.3f} -> {th[0]:+.3f}/{th[1]:+.3f}")
    for v in ("base", "head"):
        hh = hier(root / v / e / "baseline_hierarchy.rpt")
        for n, d in hh.items():
            print(f"   {v} {n}: total LUT/LUTRAM/FF/RAMB36 {d['total']}")
