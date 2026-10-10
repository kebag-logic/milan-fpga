#!/usr/bin/env python3
"""Census of the processor class-D wires the parent datapath reads.

Usage: consumer_census.py <milan_datapath.sv>
For each pp_cd_* wire, prints the line numbers where it is READ (any use other
than its declaration and the processor port binding), so the publication block
can be compared with what the datapath consumes.
"""
import re, sys
text = open(sys.argv[1], encoding="utf-8").read().splitlines()
wires = sorted({m for ln in text for m in re.findall(r"\b(pp_cd_[a-z0-9_]+_w)\b", ln)})
for w in wires:
    uses = []
    for n, ln in enumerate(text, 1):
        code = ln.split("//")[0]
        if not re.search(rf"\b{w}\b", code):
            continue
        if re.match(rf"\s*(wire|logic)\b.*\b{w}\b", code) or re.search(rf"\.\w+\s*\(\s*{w}\s*\)", code):
            continue
        uses.append(n)
    print(f"{w}: {len(uses)} read(s) {uses[:12]}")
