#!/usr/bin/env python3
"""Count processor module ports with no `//!` contract using the parent's own
parser (scripts/sv_ports.py declarations()), for two processor trees.
Usage: r391_port_doc_count.py <dir containing sv_ports.py> <tree_a> <tree_b>"""
import sys, pathlib
sys.path.insert(0, sys.argv[1])
from sv_ports import declarations
def undoc(tree):
    out = []
    for p in sorted(pathlib.Path(tree, "hdl").rglob("*.sv")):
        for mod, name, doc, _b, kind in declarations(p.read_text()):
            if kind != "param" and not doc.strip():
                out.append(f"{p.relative_to(tree)}:{mod}.{name}")
    return out
a, b = undoc(sys.argv[2]), undoc(sys.argv[3])
print("base undocumented", len(a), "head undocumented", len(b))
for x in sorted(set(b) - set(a)): print("NEW", x)
for x in sorted(set(a) - set(b)): print("GONE", x)
