#!/usr/bin/env python3
"""Re-derive PR #155's Vivado figures from the published runs.

Usage: vivado_rederive.py EVIDENCE_DIR [GATE_BASELINE_JSON]
  EVIDENCE_DIR = milan-fpga 28663f5a review-evidence/pp639-r1 (MANIFEST.json beside author-r1/)
  GATE_BASELINE_JSON = milan-fpga syn/ooc/pp_resource_baseline.json (dev fea346e7)
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ev = Path(sys.argv[1])
viv = ev / "author-r1" / "vivado"

# manifest
bad = 0
for e in json.loads((ev / "MANIFEST.json").read_text()):
    if hashlib.sha256((ev / e["file"]).read_bytes()).hexdigest() != e["published_sha256"]:
        bad += 1
        print("MANIFEST MISMATCH", e["file"])
print(f"manifest: {len(json.loads((ev / 'MANIFEST.json').read_text()))} entries, {bad} mismatches")


def util(p: Path) -> dict:
    t = p.read_text()
    def row(label, col=1):
        m = re.search(r"^\|\s*" + re.escape(label) + r"\*?\s*\|\s*([\d.]+)", t, re.M)
        return float(m.group(1)) if m else None
    return {"LUT": row("Slice LUTs"), "LUT_logic": row("LUT as Logic"), "LUT_mem": row("LUT as Memory"),
            "FF": row("Slice Registers"), "Slice": row("Slice"), "RAMB36": row("RAMB36/FIFO"),
            "RAMB18": row("RAMB18"), "DSP": row("DSPs")}


def wns(p: Path):
    lines = p.read_text().splitlines()
    for i, l in enumerate(lines):
        if l.strip().startswith("WNS(ns)"):
            v = lines[i + 2].split()
            return float(v[0]), float(v[4])
    return None


def hier(p: Path, inst: str):
    for l in p.read_text().splitlines():
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if c and c[0] == inst:
            return {"LUT": int(c[2]), "LUTRAM": int(c[4]), "FF": int(c[6]), "RAMB36": float(c[7])}
    return None


meas = {}
for ep in ("route-1x1", "ooc-1x1", "ooc-8x8"):
    for s in ("base", "head"):
        d = viv / s / ep
        u = util(d / "baseline_utilization.rpt")
        w = wns(d / "baseline_timing.rpt")
        meas[(ep, s)] = u
        print(f"{ep:9s} {s}: LUT {u['LUT']:.0f} (logic {u['LUT_logic']:.0f} + mem {u['LUT_mem']:.0f}) "
              f"FF {u['FF']:.0f} Slice {u['Slice']} RAMB36 {u['RAMB36']:.0f} RAMB18 {u['RAMB18']:.0f} "
              f"DSP {u['DSP']:.0f} WNS/WHS {w}")
        for inst in ("(u_pp)", "u_listener", "pp_shadow", "u_notify", "u_originator", "u_adp", "u_maap", "u_srp"):
            h = hier(d / "baseline_hierarchy.rpt", inst)
            if h:
                print(f"    {inst:14s} {h}")
        if ep.startswith("route"):
            rs = (d / "alinx_ax7101_route_status.rpt").read_text()
            m1 = re.search(r"routable nets\.+ :\s+(\d+)", rs)
            m2 = re.search(r"routing errors\.+ :\s+(\d+)", rs)
            print(f"    route status: routable {m1.group(1)}, errors {m2.group(1)}")
    b, h = meas[(ep, "base")], meas[(ep, "head")]
    print(f"  {ep} head-base: " + ", ".join(f"{k} {h[k] - b[k]:+g}" for k in ("LUT", "FF", "Slice", "RAMB36", "RAMB18", "DSP") if b[k] is not None))

for s in ("base", "head"):
    for ep in ("route-1x1", "ooc-1x1", "ooc-8x8"):
        log = (viv / s / ep / "baseline.log").read_text().splitlines()
        hits = sorted({re.sub(r"\s+", " ", l.strip()) for l in log
                       if ("g_armq" in l or "rec_ram_r_reg" in l) and ("RAM32M" in l or "RAMB" in l or "READ_FIRST" in l)})
        print(f"{s} {ep} mapping lines ({len(hits)} distinct):")
        for l in hits:
            print("    " + l[:160])

if len(sys.argv) > 2:
    base = json.loads(Path(sys.argv[2]).read_text())["endpoints"]
    print("gate (committed record at the given parent baseline):")
    for ep, v in base.items():
        f, t = v["record"]["figures"], v["tolerance"]
        for s in ("base", "head"):
            m = meas[(ep, s)]
            print(f"  {ep} {s} vs record: LUT {m['LUT'] - f['LUT']:+.0f} (tol {t['LUT']}), FF {m['FF'] - f['FF']:+.0f} "
                  f"(tol {t['FF']}), RAMB36 {m['RAMB36'] - f['RAMB36']:+.0f} (tol {t['RAMB36']})")
        b, h = meas[(ep, "base")], meas[(ep, "head")]
        imp = [k for k, kk in (("LUT", "LUT"), ("FF", "FF"), ("RAMB36", "RAMB36"), ("Slice", "SLICE"))
               if kk in t and b[k] is not None and b[k] - h[k] > t[kk]]
        reg = [k for k, kk in (("LUT", "LUT"), ("FF", "FF"), ("RAMB36", "RAMB36"), ("Slice", "SLICE"))
               if kk in t and b[k] is not None and h[k] - b[k] > t[kk]]
        print(f"  {ep} head vs base: regressions {reg or 'none'}; improved beyond tolerance {imp}")
