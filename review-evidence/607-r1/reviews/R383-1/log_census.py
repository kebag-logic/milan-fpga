#!/usr/bin/env python3
"""Census of emitted diagnostics and #607 hook records in implementation logs.
Usage: log_census.py <vivado.log> [...]"""
import re, sys, collections
for path in sys.argv[1:]:
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    sev = collections.Counter(); ids = collections.Counter()
    for l in lines:
        m = re.match(r"^(CRITICAL WARNING|WARNING|ERROR):\s+\[([^\]]+)\]", l)
        if m:
            sev[m.group(1)] += 1; ids[m.group(2)] += 1
    print("==", path)
    print("  severities:", dict(sev))
    print("  12-4739:", ids["Vivado 12-4739"], " 20-1307:", ids["Designutils 20-1307"], " 12-5201:", ids["Vivado 12-5201"])
    print("  critical IDs:", sorted({re.match(r'^CRITICAL WARNING:\s+\[([^\]]+)\]', l).group(1) for l in lines if l.startswith("CRITICAL WARNING:")}))
    print("  any line mentioning 4739/1307:", sum(("12-4739" in l or "20-1307" in l) for l in lines))
    for i, l in enumerate(lines, 1):
        if l.startswith("CONSTRAINTS:") or "source {" in l and "clock_constraints" in l or l.startswith("# milan_eth_constraints") or l.startswith("# kl_quasi"):
            print(f"  {i}: {l[:300]}")
    # post-route timing summary block
    for i, l in enumerate(lines):
        if "Design Timing Summary" in l:
            last = i
    for l in lines[last:last+8]:
        print("  |", l)
