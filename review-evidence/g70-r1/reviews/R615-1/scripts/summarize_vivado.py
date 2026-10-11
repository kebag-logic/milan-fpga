#!/usr/bin/env python3
"""Summarize reviewer Vivado receipts: figures, log order, timing equality.

usage: python3 -I summarize_vivado.py RECEIPTS_VIVADO_DIR
"""
import hashlib
import re
import sys
from pathlib import Path

R = Path(sys.argv[1])


def util(path):
    t = path.read_text()
    def cell(label):
        m = re.search(r"^\|\s*" + re.escape(label) + r"\s*\|\s*([0-9.]+)\s*\|", t, re.M)
        return m.group(1) if m else "?"
    return {k: cell(k) for k in ("Slice LUTs*", "LUT as Logic", "LUT as Memory",
                                  "Slice Registers", "Block RAM Tile", "DSPs")}


def timing(path):
    t = path.read_text()
    m = re.search(r"WNS\(ns\).*?\n[- ]+\n\s*([-0-9.]+)\s+([-0-9.]+)\s+(\d+)\s+(\d+)", t, re.S)
    clk = re.search(r"^clk\s+\{([^}]*)\}\s+([0-9.]+)\s+([0-9.]+)", t, re.M)
    return (m.groups() if m else None), (clk.groups() if clk else None)


def body(path):
    """Report body without the header block (dates, host, command line)."""
    lines = path.read_text().splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("Timing Report") or
                  l.startswith("Utilization Design Information") or l.startswith("1. ")), 0)
    return "\n".join(l for l in lines[start:] if "Date" not in l and "Design State" not in l)


def order(log):
    lines = log.read_text(errors="replace").splitlines()
    pats = [r"^# Vivado v", r"^# read_xdc ", r"^Command: synth_design", r"^Starting synth_design",
            r"^Parsing XDC File \[", r"^Start Technology Mapping", r"^synth_design completed",
            r"^# create_clock", r"^Synthesis finished with", r"^SW Build", r"^# synth_design"]
    out = []
    for i, l in enumerate(lines, 1):
        for p in pats:
            if re.search(p, l):
                out.append(f"  {log.name}:{i}: {l[:150]}")
                break
    return out


for arm in ("main", "head"):
    d = R / arm
    print(f"== {arm} ({'unconstrained, create_clock after synth_design' if arm == 'main' else 'constrained, XDC before synth_design'})")
    for top in ("ucpu", "engine"):
        u = util(d / f"{top}_util.rpt")
        (w, clk) = timing(d / f"{top}_timing.rpt")
        print(f"  {top}: {u}  WNS/TNS/failing/total={w}  clock={clk}")
        print("\n".join(order(d / f"{top}_ooc.log")))
for top in ("ucpu", "engine"):
    for kind in ("util", "util_hier", "timing"):
        a, b = body(R / "main" / f"{top}_{kind}.rpt"), body(R / "head" / f"{top}_{kind}.rpt")
        print(f"== body {top}_{kind}.rpt main vs head: {'IDENTICAL' if a == b else 'DIFFERENT'}"
              f"  sha256 main {hashlib.sha256(a.encode()).hexdigest()[:16]} head {hashlib.sha256(b.encode()).hexdigest()[:16]}")
print("== hierarchical engine rows differing main vs head")
ha = (R / "main/engine_util_hier.rpt").read_text().splitlines()
hb = (R / "head/engine_util_hier.rpt").read_text().splitlines()
for x, y in zip(ha, hb):
    if x != y and x.startswith("|"):
        print("  main:", x.strip()[:150])
        print("  head:", y.strip()[:150])
p = R / "plant-usedinsynth"
if p.is_dir():
    print("== plant USED_IN_SYNTHESIS false (ucpu)")
    u = util(p / "ucpu_util.rpt")
    (w, clk) = timing(p / "ucpu_timing.rpt")
    print(f"  ucpu: {u}  WNS/TNS/failing/total={w}  clock={clk}")
    print("\n".join(order(p / "ucpu_ooc.log")))
