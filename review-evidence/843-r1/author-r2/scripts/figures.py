"""figures.py <scratch>: LUT, FF, slices, RAMB36/RAMB18, DSP and per-corner WNS/WHS of each route directory of the
head and dev sets, read from the Vivado reports themselves; prints JSON (the docs and the HANDOFF quote it)."""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
DIRS = {"ExtraPostPlacementOpt": "ax7101/gateware", "AltSpreadLogic_high": "ax7101-AltSpreadLogic_high",
        "ExtraTimingOpt": "ax7101-ExtraTimingOpt"}


def util(path):
    text = path.read_text()
    def row(name):
        m = re.search(r"^\|\s+" + re.escape(name) + r"\s+\|\s+([0-9.]+) \|", text, re.M)
        return float(m.group(1)) if m else None
    return dict(LUT=int(row("Slice LUTs")), FF=int(row("Slice Registers")), SLICE=int(row("Slice")),
                RAMB36=int(row("RAMB36/FIFO*")), RAMB18=int(row("RAMB18")), DSP=int(row("DSPs")),
                BRAM_TILE=row("Block RAM Tile"))


def corner(path):
    lines = path.read_text().splitlines()
    for i, line in enumerate(lines):
        if "WNS(ns)" in line and "TNS(ns)" in line:
            cells = lines[i + 2].split()
            return float(cells[0]), float(cells[4])
    raise SystemExit(f"no design timing summary in {path}")


out = {}
for tag in ("head", "dev"):
    for directive, rel in DIRS.items():
        d = root / f"route-{tag}" / "w" / rel
        if not (d / "baseline.log.rc").exists():
            continue
        rec = util(next(d.glob("*_utilization_place.rpt")))
        rec["corners"] = {c: corner(d / f"alinx_ax7101_signoff_{c}_timing.rpt")
                          for c in ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C")}
        rec["WNS_worst"] = min(v[0] for v in rec["corners"].values())
        rec["WHS_worst"] = min(v[1] for v in rec["corners"].values())
        status = next(d.glob("*_route_status.rpt")).read_text()
        rec["routing_errors"] = int(re.search(r"nets with routing errors\.+ :\s+(\d+)", status).group(1))
        rec["rc_seconds"] = (d / "baseline.log.rc").read_text().split()
        out.setdefault(tag, {})[directive] = rec
print(json.dumps(out, indent=1))
