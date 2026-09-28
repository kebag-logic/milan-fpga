#!/usr/bin/env python3
"""Heuristic used-before-declaration probe for one SystemVerilog module.

Collects module-scope net/variable declarations (logic, wire, typed struct/
enum variables) with their line numbers, strips comments, and reports every
identifier whose first textual reference precedes its declaration. It is a
reviewer probe mirroring the class of finding the parent's xvlog gate reports
(VRFC 10-3380); it is not a parser and may over-report, never silently skip a
declared name.

usage: decl_order_probe.py FILE.sv
"""
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
# strip comments, keep line structure
src = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group().count("\n"), src, flags=re.S)
lines = [re.sub(r"//.*", "", l) for l in src.split("\n")]

decl_re = re.compile(
    r"^\s*(?:logic|wire|reg|tk_rec_t|state_e|evc_e|dk_e|pp_txn_t)\b"
    r"(?:\s*\[[^\]]*\])*\s+(.*?);")
decls = {}
for n, l in enumerate(lines, 1):
    m = decl_re.match(l)
    if not m:
        continue
    for part in m.group(1).split(","):
        name = re.match(r"\s*([A-Za-z_]\w*)", part)
        if name and name.group(1) not in decls:
            decls[name.group(1)] = n

bad = []
for name, dline in sorted(decls.items(), key=lambda kv: kv[1]):
    pat = re.compile(r"\b" + re.escape(name) + r"\b")
    for n, l in enumerate(lines[: dline - 1], 1):
        if pat.search(l):
            bad.append((name, n, dline))
            break

print(f"{sys.argv[1]}: {len(decls)} module-scope declarations checked")
for name, used, declared in bad:
    print(f"USED-BEFORE-DECL {name}: first use line {used}, declared line {declared}")
print(f"RESULT: {len(bad)} finding(s)")
sys.exit(1 if bad else 0)
