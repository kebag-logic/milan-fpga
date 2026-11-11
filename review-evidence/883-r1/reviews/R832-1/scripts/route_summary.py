#!/usr/bin/env python3
"""Summarise the author's published Vivado route reports, read-only.

Usage: python3 -I route_summary.py <extracted vivado receipts dir>

For each directive directory w__ax7101__gateware (ExtraPostPlacementOpt),
w__ax7101-ExtraTimingOpt and w__ax7101-AltSpreadLogic_high, print each
signoff corner's WNS/WHS from the *_operating.rpt design timing summary, the
placed Slice / Slice LUT / Slice Register rows, and the route status lines.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
DIRS = [("ExtraPostPlacementOpt", "w__ax7101__gateware"),
        ("ExtraTimingOpt", "w__ax7101-ExtraTimingOpt"),
        ("AltSpreadLogic_high", "w__ax7101-AltSpreadLogic_high")]
CORNERS = ["Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C"]


def timing_summary(text: str) -> tuple[str, str]:
    """WNS and WHS from the first Design Timing Summary table."""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip().startswith("WNS(ns)") and "WHS(ns)" in ln:
            hdr = ln.split()
            for row in lines[i + 1:i + 4]:
                vals = row.split()
                if len(vals) >= len(hdr) and re.match(r"^-?\d", vals[0]):
                    d = dict(zip(hdr, vals))
                    return d.get("WNS(ns)", "?"), d.get("WHS(ns)", "?")
    return "?", "?"


for name, d in DIRS:
    p = root / d
    print(f"== {name} ({d})")
    for c in CORNERS:
        f = p / f"alinx_ax7101_signoff_{c}_operating.rpt"
        if f.exists():
            wns, whs = timing_summary(f.read_text(errors="replace"))
            print(f"  {c:9s} WNS {wns:>7s}  WHS {whs:>7s}")
        else:
            print(f"  {c:9s} report missing")
    u = p / "alinx_ax7101_utilization_place.rpt"
    if u.exists():
        for ln in u.read_text(errors="replace").splitlines():
            if re.match(r"^\| (Slice LUTs|Slice Registers|Slice|Block RAM Tile|DSPs)\s+\|", ln):
                print("  " + re.sub(r"\s+", " ", ln.strip()))
    r = p / "alinx_ax7101_route_status.rpt"
    if r.exists():
        for ln in r.read_text(errors="replace").splitlines():
            if re.search(r"routing errors|unrouted|fully routed nets", ln):
                print("  " + re.sub(r"\s+", " ", ln.strip()))
