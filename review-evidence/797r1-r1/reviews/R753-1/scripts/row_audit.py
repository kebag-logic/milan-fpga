#!/usr/bin/env python3
"""List field rows with empty descriptions and side-effect rows on the page. Usage: row_audit.py <page>"""
import re, sys, collections
text = open(sys.argv[1], encoding="utf-8").read()
empty = collections.Counter(); total = collections.Counter(); blank_rows = []; nopurpose = []; noname = []
secs = list(re.finditer(r"^### (\S+) registers? \(offset (0x[0-9A-F]+).*?\n(.*?)(?=^#{2,3} )", text, re.M | re.S))
for s in secs:
    name, off, body = s.groups()
    paras = [p for p in body.split("\n\n") if p.strip()]
    if not paras or paras[0].startswith(("RTL name", "This build")):
        nopurpose.append(name)
    for r in re.finditer(r"^\| (\d+(?::\d+)?) \| `([^`]+)` \| ([^`|\s]+) \| ([^|]*?) \| (.*) \|$", body, re.M):
        bits, fname, acc, rst, d = r.groups()
        total[acc] += 1
        if not d.strip():
            empty[acc] += 1
            blank_rows.append((off, name, bits, fname, acc))
print("registers", len(secs), "without a purpose paragraph:", nopurpose)
print("rows per access", dict(total))
print("rows with an empty description per access", dict(empty), "total", sum(empty.values()), "of", sum(total.values()))
print("--- side-effect access codes with an empty description cell")
for b in blank_rows:
    if b[4] not in ("R", "R/W", "W"):
        print("  ", *b)
print("--- W and R/W rows with an empty description cell")
for b in blank_rows:
    if b[4] in ("R/W", "W"):
        print("  ", *b)
