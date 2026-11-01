#!/usr/bin/env python3
"""Independent offset cross-check: every RTL A_* localparam against the page's 'RTL name' lines.
Usage: offset_check.py <rtl> <page>"""
import re, sys
rtl = re.sub(r"//.*", "", open(sys.argv[1], encoding="utf-8").read())
addr = {m.group(1): int(m.group(2), 16) for m in re.finditer(r"\b(A_\w+)\s*=\s*'h([0-9A-Fa-f]+)", rtl)}
page = open(sys.argv[2], encoding="utf-8").read()
secs = {m.group(2): (m.group(1), int(m.group(3), 16)) for m in re.finditer(
    r"^### (\S+) registers? \(offset (?:(0x[0-9A-F]+)).*?\n", page, re.M) for _ in [0] if False}
rows = re.findall(r"^### (\S+) registers? \(offset (0x[0-9A-F]+)[^\n]*\n.*?RTL name: `([^`]+)`", page, re.M | re.S)
print("A_ labels", len(addr), "page sections", len(rows))
seen = set(); bad = 0
for acr, off, name in rows:
    off = int(off, 16)
    key = name.split()[0].split("..")[0]
    if key in addr:
        seen.add(key)
        if addr[key] != off:
            print("MISMATCH", acr, hex(off), name, hex(addr[key])); bad += 1
missing = sorted(set(addr) - seen)
print("mismatches", bad)
print("labels with no section of their own:", [(m, hex(addr[m])) for m in missing])
