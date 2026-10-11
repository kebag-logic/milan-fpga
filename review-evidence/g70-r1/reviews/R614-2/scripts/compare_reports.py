#!/usr/bin/env python3
"""Compare the two retained OOC measurements. Usage: compare_reports.py PACKET"""
from pathlib import Path
import re
import sys

packet = Path(sys.argv[1]).resolve()
def timing_body(text):
    # report_clocks is appended as a second independently headed report.
    text = text.split("Copyright 1986-2022 Xilinx", 2)[1]
    return "\n".join(line for line in text.splitlines() if not re.match(r"\| (Date|Host)\s*:", line)).rstrip()

for flow in ("main", "head"):
    for top in ("engine", "ucpu"):
        root = packet / "scratch" / ("viv_" + flow)
        util = (root / (top + "_util.rpt")).read_text()
        timing = (root / (top + "_timing.rpt")).read_text()
        log = (root / (top + "_ooc.log")).read_text()
        metrics = {}
        for key in ("Slice LUTs*", "Slice Registers", "Block RAM Tile", "DSPs"):
            metrics[key] = re.search(r"^\| " + re.escape(key) + r"\s*\|\s*([\d.]+)", util, re.M).group(1)
        wns = re.search(r"^\s*WNS\(ns\).*\n.*\n\s*([\d.]+)\s+([\d.]+)\s+(\d+)\s+(\d+)", timing, re.M).groups()
        metrics.update(WNS=wns[0], TNS=wns[1], failing_endpoints=wns[2], total_endpoints=wns[3])
        expected = ("4853" if flow == "main" else "4852", "3652", "1.5", "4", "1.773", "0.000", "0", "12254") if top == "engine" else ("1643", "733", "1.5", "4", "1.941", "0.000", "0", "3165")
        assert tuple(metrics.values()) == expected, metrics
        print(flow, top, metrics)
        assert "CRITICAL WARNING:" not in log
        assert "0 Critical Warnings and 0 Errors encountered." in log
        for i, line in enumerate(log.splitlines(), 1):
            if any(t in line for t in ("# read_xdc", "Command: synth_design", "Parsing XDC File [", "Start Technology Mapping", "synth_design completed successfully", "# create_clock", "Critical Warnings")):
                print(f"  {top}_ooc.log:{i}: {line}")
        assert all((root / (top + "_" + suffix + ".rpt")).is_file() for suffix in ("util", "util_hier", "timing"))
for top in ("engine", "ucpu"):
    old = (packet / "scratch" / "viv_main" / (top + "_timing.rpt")).read_text()
    new = (packet / "scratch" / "viv_head" / (top + "_timing.rpt")).read_text()
    same = timing_body(old) == timing_body(new)
    print(f"{top}: timing summary bodies equal after stripping Date/Host and the appended report_clocks: {same}")
    assert same
print("PASS: both flows reproduce every published metric; both runs retain six reports")
