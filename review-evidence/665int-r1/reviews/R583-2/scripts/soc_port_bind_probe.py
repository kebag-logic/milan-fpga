#!/usr/bin/env python3
"""Reviewer probe: every port of KL_mbx is bound by the --ctrl-mailbox SoC's
Instance("KL_mbx", ...) in sw/litex/milan_soc.py, with the right direction,
and no keyword names a port KL_mbx lacks. Usage: python3 -I soc_port_bind_probe.py <repo>"""
import re, sys
from pathlib import Path
repo = Path(sys.argv[1])
sv = (repo / "hdl/milan/mailbox/KL_mbx.sv").read_text()
hdr = sv[sv.index("module KL_mbx"):sv.index(");", sv.index("module KL_mbx"))]
ports = {m.group(2): m.group(1) for m in re.finditer(r"\b(input|output)\s+(?:logic\s+|wire\s+)?(?:\[[^\]]*\]\s*)?(\w+)", hdr)}
soc = (repo / "sw/litex/milan_soc.py").read_text()
start = soc.index('Instance("KL_mbx",')
body = soc[start:soc.index("self.comb", start)]
kw = {m.group(2): {"i": "input", "o": "output"}[m.group(1)] for m in re.finditer(r"\b([io])_(\w+)=", body)}
missing = sorted(set(ports) - set(kw)); extra = sorted(set(kw) - set(ports))
wrongdir = sorted(p for p in set(ports) & set(kw) if ports[p] != kw[p])
print(f"KL_mbx ports {len(ports)}; SoC binds {len(kw)}; missing {missing}; extra {extra}; wrong direction {wrongdir}")
sys.exit(1 if (missing or extra or wrongdir) else 0)
