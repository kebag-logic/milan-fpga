#!/usr/bin/env python3
"""Run the head's all-fabric census over every extracted published hierarchy report.

Usage: python3 -I -B census_published.py <repo>/syn/ooc <reports-root>
Prints one line per report: kind (ooc if baseline_ooc.tcl was published), problems.
"""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import pp_placement
root = Path(sys.argv[2])
for rpt in sorted(root.rglob("baseline_hierarchy.rpt")):
    listing = (rpt.parent / "listing.txt").read_text().split()
    kind = "ooc" if "baseline_ooc.tcl" in listing else "route" if "baseline_integrated.tcl" in listing else "?"
    routed = any(name.endswith("_route_status.rpt") for name in listing)
    problems = pp_placement.all_fabric_problems(rpt.parent)
    print(f"{kind}\trouted={routed}\t{rpt.relative_to(root).parent}\t{'PASS' if not problems else '; '.join(problems)}")
