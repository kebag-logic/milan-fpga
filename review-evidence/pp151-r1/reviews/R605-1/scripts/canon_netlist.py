#!/usr/bin/env python3
"""Canonical form of a Yosys `write_verilog -noattr` netlist, connectivity kept.

Source positions (all.v:N[.c-N.c]) are masked; Yosys's numbered auto-names
(`_123_` from write_verilog, `$123` counters inside escaped names) are renumbered
in order of first appearance, so an object created or not created upstream
shifts no later name. Line order is kept (not sorted), so the result still
encodes which net drives which cell.
usage: canon_netlist.py <net.v>   (canonical text on stdout)
"""
import re
import sys

text = open(sys.argv[1]).read()
text = re.sub(r"all\.v:\d+(\.\d+-\d+\.\d+)?", "all.v:L", text)
for pat, fmt in ((r"\b_(\d+)_\b", "_{}_"), (r"\$(\d+)\b", "${}")):
    seen = {}
    def ren(m, seen=seen, fmt=fmt):
        return fmt.format(seen.setdefault(m.group(0), len(seen)))
    text = re.sub(pat, ren, text)
sys.stdout.write(text)
