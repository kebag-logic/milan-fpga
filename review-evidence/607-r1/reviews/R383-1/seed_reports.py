#!/usr/bin/env python3
"""Summarise each seed's retained interaction and crossing reports.
Usage: seed_reports.py <build dir> [...]"""
import csv, sys
from pathlib import Path
for d in map(Path, sys.argv[1:]):
    acc = d / "acceptance"
    print("==", d.name)
    for rpt in sorted(acc.glob("seed*_interaction.rpt")):
        rows = [l for l in rpt.read_text().splitlines() if "eth_clocks0_rx" in l]
        unsafe = [l for l in rpt.read_text().splitlines() if "Unsafe" in l or "unsafe" in l]
        cons = sorted({" ".join(l.split()[-3:]) if "Max Delay" in l else l.split()[-1] for l in rows})
        print(f"  {rpt.name}: eth rows={len(rows)} unsafe_lines={len(unsafe)} constraints={cons}")
    t = acc / "seed_crossings.tsv"
    if t.exists():
        rows = list(csv.DictReader(t.open(), delimiter="\t"))
        reqs = {r["requirement_ns"] for r in rows}
        worst = min(float(r["slack_ns"]) for r in rows)
        print(f"  crossings.tsv rows={len(rows)} requirements={reqs} worst_slack={worst}")
