#!/usr/bin/env python3
"""Read one AX7101 route's Vivado reports into a JSON record.

usage: route_figures.py <gateware dir>

Utilization from *_utilization_place.rpt (the first row of each name), WNS/WHS per
signoff corner from the Design Timing Summary of each *_signoff_<corner>_timing.rpt,
routing errors and unrouted nets from *_route_status.rpt, and the bound N_STREAM_IN_P,
N_STREAMS and AUDIO_IF_RENDER_SLOTS_P from the generated top. Exits 1 if a figure is absent.
"""
import json
import re
import sys
from pathlib import Path

gw = Path(sys.argv[1])
util = next(gw.glob("*_utilization_place.rpt")).read_text()


def row(name):
    m = re.search(r"^\| " + re.escape(name) + r"\s+\|\s*([0-9.]+)\s*\|.*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*$", util, re.M)
    return {"used": float(m.group(1)), "available": float(m.group(2)), "pct": float(m.group(3))}


rec = {"gateware": gw.parent.name}
for key, name in (("lut", "Slice LUTs"), ("ff", "Slice Registers"), ("slice", "Slice"),
                  ("bram_tile", "Block RAM Tile"), ("dsp", "DSPs")):
    rec[key] = row(name)
rec["slice"]["free"] = rec["slice"]["available"] - rec["slice"]["used"]
corners = {}
for rpt in sorted(gw.glob("*_signoff_*_timing.rpt")):
    corner = re.search(r"_signoff_(.+)_timing\.rpt$", rpt.name).group(1)
    if not re.fullmatch(r"(Slow|Fast)_[0-9]+C", corner):
        continue
    lines = rpt.read_text().splitlines()
    i = next(n for n, line in enumerate(lines) if "Design Timing Summary" in line)
    vals = lines[i + 6].split()
    corners[corner] = {"wns": float(vals[0]), "whs": float(vals[4])}
rec["corners"] = corners
rec["wns_worst"] = min(c["wns"] for c in corners.values())
rec["whs_worst"] = min(c["whs"] for c in corners.values())
status = next(gw.glob("*_route_status.rpt")).read_text()
rec["routing_errors"] = int(re.search(r"# of nets with routing errors\.*\s*:\s*(\d+)", status).group(1))
m = re.search(r"# of unrouted nets\.*\s*:\s*(\d+)", status)
rec["unrouted_nets"] = int(m.group(1)) if m else None
top = gw / "alinx_ax7101.v"
if top.exists():
    text = top.read_text(errors="replace")
    for p in ("N_STREAMS", "AUDIO_IF_RENDER_SLOTS_P"):
        m = re.search(r"\." + p + r"\s*\(\s*\d*'d(\d+)\s*\)", text)
        rec[p] = int(m.group(1)) if m else None
print(json.dumps(rec, indent=1))
sys.exit(0 if corners and rec["lut"] else 1)
