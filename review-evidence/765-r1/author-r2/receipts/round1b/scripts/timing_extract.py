#!/usr/bin/env python3
"""Write timing_summary.txt (design summary to the intra-clock table end) and
worst_setup_path.txt (the first path whose slack is the design WNS) out of one timing report."""
import sys
from pathlib import Path

rpt, out = Path(sys.argv[1]), Path(sys.argv[2])
lines = rpt.read_text().splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith("| Design Timing Summary"))
stop = next(i for i, l in enumerate(lines) if i > start and l.startswith("| Inter Clock Table"))
(out / "timing_summary.txt").write_text("\n".join(lines[start:stop]) + "\n")
wns = lines[start + 6].split()[0]
p = next(i for i, l in enumerate(lines)
         if l.startswith("Slack (") and l.split(":")[1].strip().startswith(wns + "ns"))
q = next(i for i, l in enumerate(lines) if i > p and l.strip().startswith("slack"))
(out / "worst_setup_path.txt").write_text("\n".join(lines[p:q + 1]) + "\n")
