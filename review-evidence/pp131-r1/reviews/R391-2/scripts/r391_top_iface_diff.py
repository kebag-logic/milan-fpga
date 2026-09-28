#!/usr/bin/env python3
"""Mechanical diff of protocol_processor_top's ports and parameters between
two processor trees, with the parent's parser (scripts/sv_ports.py).
Usage: r391_top_iface_diff.py <dir containing sv_ports.py> <tree_a> <tree_b>"""
import sys, pathlib, re
sys.path.insert(0, sys.argv[1])
from sv_ports import declarations
def iface(tree):
    txt = pathlib.Path(tree, "hdl/top/protocol_processor_top.sv").read_text()
    head = txt[txt.index("module protocol_processor_top"):]
    head = head[:head.index("\n);") + 3]
    code = [re.sub(r"//.*", "", l).rstrip() for l in head.splitlines()]
    out = {}
    for mod, name, _doc, _b, kind in declarations(txt):
        if mod != "protocol_processor_top":
            continue
        # the declaration text: from the line naming it to the next ',' or ')' at depth 0
        i = next(k for k, l in enumerate(code) if re.search(r"\b%s\b" % re.escape(name), l))
        decl = code[i]
        while not re.search(r"[,;]\s*$|\)\s*;?\s*$", decl) and i + 1 < len(code):
            i += 1
            decl += " " + code[i]
        out[name] = (kind, re.sub(r"\s+", " ", decl).strip())
    return out
a, b = iface(sys.argv[2]), iface(sys.argv[3])
print(f"ports+params: {len(a)} -> {len(b)}")
for n in sorted(set(b) - set(a)): print("ADDED  ", b[n][0], n, "|", b[n][1][:160])
for n in sorted(set(a) - set(b)): print("REMOVED", a[n][0], n)
for n in sorted(set(a) & set(b)):
    if a[n] != b[n]: print("CHANGED", n, "|", a[n][1][:120], "=>", b[n][1][:160])
