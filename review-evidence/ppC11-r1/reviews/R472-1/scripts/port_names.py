#!/usr/bin/env python3
"""Every *_i / *_o name on the given Markdown pages must be a port declared in hdl/.

usage: port_names.py <repo> <page>...   (prints each name not declared; rc 1 if any)
Ports: ANSI declarations `input|output|inout ... name[, name]` in every hdl/**/*.sv.
Names are taken from anywhere on the page (code spans, prose, waveform JSON), and
a name carrying a [msb:lsb] suffix is reduced to its base name.
"""
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1])
decl = re.compile(r"^\s*(?:input|output|inout)\b([^;/]*)", re.M)
ports, top = set(), set()
for sv in sorted((repo / "hdl").rglob("*.sv")):
    text = re.sub(r"/\*.*?\*/", "", sv.read_text(encoding="utf-8"), flags=re.S)
    for m in decl.finditer(text):
        names = re.findall(r"\b([A-Za-z_]\w*)\s*(?:\[[^\]]*\]\s*)*(?=,|\)|$)", m.group(1))
        for n in names:
            ports.add(n)
            if sv.name == "protocol_processor_top.sv":
                top.add(n)
name = re.compile(r"(?<![\w.])([a-z][a-z0-9_]*_[io])(?![\w])")
missing, seen = [], {}
for page in sys.argv[2:]:
    for no, line in enumerate((repo / page).read_text(encoding="utf-8").splitlines(), 1):
        for n in name.findall(line):
            seen.setdefault(n, f"{page}:{no}")
            if n not in ports:
                missing.append(f"{page}:{no}: {n}")
print(f"ports declared under hdl/: {len(ports)} ({len(top)} on protocol_processor_top)")
print(f"distinct *_i/*_o names on {len(sys.argv) - 2} pages: {len(seen)}")
not_top = sorted(n for n in seen if n in ports and n not in top)
print(f"names that are ports of a submodule, not of the top ({len(not_top)}): "
      + ", ".join(f"{n} ({seen[n]})" for n in not_top))
for m in missing:
    print(f"NOT A PORT: {m}")
print("OK" if not missing else f"{len(missing)} FAILURES")
sys.exit(1 if missing else 0)
