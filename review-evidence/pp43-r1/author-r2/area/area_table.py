#!/usr/bin/env python3
"""Summarise OOC util.rpt / util_hier.rpt / timing.rpt for base, r1, cand."""
import re, sys
from pathlib import Path
A = Path(sys.argv[1])
def tot(d):
    t = (A / d / "util.rpt").read_text()
    g = lambda k: int(re.search(r"^\|\s*" + re.escape(k) + r"\*?\s*\|\s*(\d+)", t, re.M).group(1))
    return {"LUT": g("Slice LUTs"), "LUTL": g("LUT as Logic"), "LUTM": g("LUT as Memory"),
            "FF": g("Slice Registers"), "BRAM": float(re.search(r"^\|\s*Block RAM Tile\s*\|\s*([\d.]+)", t, re.M).group(1))}
def wns(d):
    t = (A / d / "timing.rpt").read_text()
    m = re.search(r"WNS\(ns\)[^\n]*\n[^\n]*\n\s*([-\d.]+)", t)
    return m.group(1) if m else "?"
def hier(d):
    rows = {}
    for line in (A / d / "util_hier.rpt").read_text().splitlines():
        if not line.startswith("|") or "Instance" in line: continue
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) < 4 or not c[2].replace(".", "").isdigit(): continue
        key = line.split("|")[1].rstrip()
        rows[key] = (int(c[2]), int(c[6]) if c[6].isdigit() else 0)
    return rows
for shape in ("8x8", "1x1"):
    print(f"== {shape}")
    T = {n: tot(f"{n}-{shape}") for n in ("base", "r1", "cand")}
    for k in ("LUT", "LUTL", "LUTM", "FF", "BRAM"):
        b, r, c = T["base"][k], T["r1"][k], T["cand"][k]
        print(f"{k:5} base {b:>8} r1 {r:>8} cand {c:>8} | cand-base {c-b:+} r1-base {r-b:+} cand-r1 {c-r:+}")
    print("WNS", {n: wns(f"{n}-{shape}") for n in ("base", "r1", "cand")})
    H = {n: hier(f"{n}-{shape}") for n in ("base", "r1", "cand")}
    keys = sorted(set().union(*[set(h) for h in H.values()]), key=lambda k: list(H["cand"]).index(k) if k in H["cand"] else 9999)
    print(f"{'instance':50} {'dLUT c-b':>9} {'dFF c-b':>8} {'dLUT c-r1':>9} {'dFF c-r1':>8}")
    for k in keys:
        b = H["base"].get(k, (0, 0)); r = H["r1"].get(k, (0, 0)); c = H["cand"].get(k, (0, 0))
        if (c[0]-b[0], c[1]-b[1], c[0]-r[0], c[1]-r[1]) != (0, 0, 0, 0):
            print(f"{k[:50]:50} {c[0]-b[0]:>+9} {c[1]-b[1]:>+8} {c[0]-r[0]:>+9} {c[1]-r[1]:>+8}")
