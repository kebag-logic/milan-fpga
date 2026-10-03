#!/usr/bin/env python3
"""Every `*_i`/`*_o` name in 02 sections 4.3 to 6 (lines 344-528 at e2c7d97) must be a
protocol_processor_top port. Usage: port_names_02.py <clone>"""
import re, sys
root = sys.argv[1]
top = open(f"{root}/hdl/top/protocol_processor_top.sv").read()
hdr = re.search(r"module\s+protocol_processor_top(.*?)\n\);", top, re.S).group(1)
ports = {m.group(3): (m.group(1), m.group(2)) for m in
         re.finditer(r"^\s*(input|output)\s+(?:wire|logic)?\s*(\[[^\]]+\])?\s*(\w+)", hdr, re.M)}
doc = open(f"{root}/docs/architecture/02_interfaces.md").read().splitlines()[343:528]
names = sorted({n for l in doc for t in re.findall(r"`([^`]+)`", l)
                for n in re.findall(r"\b([a-z][a-z0-9_]*_(?:i|o))\b", t)})
miss = [n for n in names if n not in ports]
for n in names:
    print(("OK      " if n in ports else "MISSING ") + n, ports.get(n, ""))
print(f"{len(ports)} top ports; {len(names)} names in 02 4.3-6; {len(miss)} missing")
sys.exit(1 if miss else 0)
