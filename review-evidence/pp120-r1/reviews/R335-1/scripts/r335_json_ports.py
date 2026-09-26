#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Compare the elaborated top-level ports (name, direction, width) of a
module between two Verilator --json-only trees.
Usage: r335_json_ports.py <base.tree.json> <head.tree.json> <module>"""
import json, sys

def ports(path, module):
    tree = json.load(open(path))
    types = {}
    def walk(n, fn):
        if isinstance(n, dict):
            fn(n)
            for v in n.values(): walk(v, fn)
        elif isinstance(n, list):
            for v in n: walk(v, fn)
    def collect_types(n):
        if n.get("type", "").endswith("DTYPE") and "addr" in n:
            types[n["addr"]] = n
    walk(tree, collect_types)
    mods = []
    walk(tree, lambda n: mods.append(n) if n.get("type") == "MODULE"
         and n.get("origName", n.get("name")) == module else None)
    out = []
    for item in mods[0].get("stmtsp", []):
        if item.get("type") == "VAR" and item.get("direction", "NONE") != "NONE":
            dt = types.get(item.get("dtypep"), {})
            rng = dt.get("range", "") or dt.get("width", "")
            out.append((item["name"], item["direction"], str(dt.get("name", "")),
                        str(rng)))
    return out

b = ports(sys.argv[1], sys.argv[3]); h = ports(sys.argv[2], sys.argv[3])
bs, hs = set(b), set(h)
print(f"{sys.argv[3]}: base {len(b)} ports, head {len(h)} ports")
for p in b:
    if p not in hs: print("  REMOVED/CHANGED", p)
for p in h:
    if p not in bs: print("  ADDED", p)
print("  common ports in identical order:",
      [p for p in b if p in hs] == [p for p in h if p in bs])
