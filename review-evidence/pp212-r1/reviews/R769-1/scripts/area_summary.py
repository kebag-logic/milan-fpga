#!/usr/bin/env python3
"""area_summary.py <dir>...: LUT1-6, FF, CARRY4, MUXF7/8, RAM from yosys stat files."""
import re, sys, pathlib
def read(p):
    c = {}
    for m in re.finditer(r"^\s+(\d+)\s+.*?\b(\w+)$|^\s+(\w+)\s+(\d+)$", p.read_text(), re.M):
        if m.group(1): c[m.group(2)] = c.get(m.group(2), 0) + int(m.group(1))
        else: c[m.group(3)] = c.get(m.group(3), 0) + int(m.group(4))
    lut = sum(v for k, v in c.items() if re.fullmatch(r"LUT[1-6]", k))
    ff = sum(v for k, v in c.items() if re.fullmatch(r"FD[CPRSE]+", k))
    mux = c.get("MUXF7", 0) + c.get("MUXF8", 0)
    ram = sum(v for k, v in c.items() if k.startswith("RAM"))
    return lut, ff, c.get("CARRY4", 0), mux, ram, c.get("INV", 0)
print("| dir | shape | LUT1-6 | FF | CARRY4 | MUXF7/8 | RAM | INV |")
print("|---|---|---:|---:|---:|---:|---:|---:|")
for d in sys.argv[1:]:
    for s in sorted(pathlib.Path(d).glob("*.stat")):
        print(f"| {pathlib.Path(d).name} | {s.stem} |", " | ".join(str(x) for x in read(s)), "|")
