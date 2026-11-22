#!/usr/bin/env python3
"""route_receipt.py <build_dir> <label>: one route's receipt, printed: its start, end and exit status, the placed
utilization, the top of the placed hierarchy, each signoff corner's WNS and WHS with failing endpoints, and the
worst setup path at the slowest corner. Reads only the build's own reports; writes nothing."""
import re
import sys
from pathlib import Path

build, label = Path(sys.argv[1]), sys.argv[2]
gw = build / "gateware"


def text(p: Path) -> str:
    return p.read_text(errors="replace") if p.is_file() else ""


start = text(build.with_name(build.name + ".start")).strip()
end = text(build.with_name(build.name + ".end")).strip()
rc = text(build.with_name(build.name + ".rc")).strip()
print(f"# route {label}: {start} to {end}, rc {rc}")
print("## placed utilization (alinx_ax7101_utilization_place.rpt)")
util = text(gw / "alinx_ax7101_utilization_place.rpt")
for key in ("Slice LUTs", "Slice Registers", "Slice  ", "LUT as Memory", "Block RAM Tile", "RAMB18", "DSPs"):
    for line in util.splitlines():
        if line.startswith("| " + key) or line.startswith("|   " + key.strip()) and key.strip() == "RAMB18":
            cells = [c.strip() for c in line.strip("|").split("|")]
            print(f" {cells[0]:28} {cells[1]:>8}  of {cells[-2]:>8}")
            break
print("## hierarchy (utilization_hierarchical_place.rpt: instance, LUT, LUTRAM, FF, RAMB36, RAMB18)")
hier = text(gw / "alinx_ax7101_utilization_hierarchical_place.rpt")
for line in hier.splitlines():
    m = re.match(r"^\|(\s+)(\S+)\s+\|\s+\S+\s+\|\s+(\d+)\s+\|\s+\d+\s+\|\s+(\d+)\s+\|\s+\d+\s+\|\s+(\d+)\s+\|\s+(\d+)"
                 r"\s+\|\s+(\d+)", line)
    if m and (len(m.group(1)) - 1) // 2 <= 1:
        print(f"   {m.group(2):66} {m.group(3):>6} {m.group(4):>6} {m.group(5):>7} {m.group(6):>4} {m.group(7):>4}")
print("## signoff corners (WNS, WHS ns)")
for corner in ("Slow_85C", "Slow_0C", "Fast_85C", "Fast_0C"):
    rpt = text(gw / f"alinx_ax7101_signoff_{corner}_timing.rpt")
    m = re.search(r"WNS\(ns\).*?\n[- ]+\n\s*(-?[\d.]+)\s+(-?[\d.]+)\s+(\d+)\s+(\d+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(\d+)", rpt)
    print(f"{corner}: " + (f"WNS {m.group(1)} failing {m.group(3)} WHS {m.group(5)} failing {m.group(7)}" if m
                           else "no report"))
print("## worst setup path, Slow_85C")
rpt = text(gw / "alinx_ax7101_signoff_Slow_85C_timing.rpt")
# every clock group's setup section: from its "Max Delay Paths" to the next "Min Delay Paths"
setup = "".join(seg.split("Min Delay Paths")[0] for seg in rpt.split("Max Delay Paths")[1:])
blocks = [(float(m.group(1)), m.start()) for m in re.finditer(r"Slack \((?:MET|VIOLATED)\)\s*:\s*(-?[\d.]+)ns", setup)]
if blocks:
    at = min(blocks)[1]
    for line in setup[at:].splitlines()[:14]:
        if line.strip().startswith(("Slack", "Source:", "Destination:", "Path Group:", "Data Path Delay:",
                                    "Logic Levels:")):
            print(" " + line.strip())
