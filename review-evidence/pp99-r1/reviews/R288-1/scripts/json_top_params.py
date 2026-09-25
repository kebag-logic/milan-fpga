#!/usr/bin/env python3
"""List GPARAM (overridable) and LPARAM vars declared directly in
protocol_processor_top from a Verilator --json-only tree, in source order.
Usage: json_top_params.py <tree.json>"""
import json
import sys

tree = json.load(open(sys.argv[1]))


def walk(n):
    if isinstance(n, dict):
        yield n
        for v in n.values():
            yield from walk(v)
    elif isinstance(n, list):
        for v in n:
            yield from walk(v)


mods = [n for n in walk(tree) if n.get("type") == "MODULE"
        and n.get("origName", n.get("name")) == "protocol_processor_top"]
print("top modules found:", len(mods))
m = mods[0]
g, l = [], []
for item in m.get("stmtsp", []):
    if item.get("type") == "VAR" and item.get("varType") in ("GPARAM", "LPARAM"):
        (g if item["varType"] == "GPARAM" else l).append(item.get("origName", item["name"]))
print("GPARAM", len(g), " ".join(g))
print("LPARAM(header+body)", len(l))
