"""Attribute Yosys-mapped memory and DSP primitives to hierarchy prefixes.

usage: yosys_attrib.py <KL_pp_shadow.ooc.json>
Flattened cell names keep the source hierarchy as dotted/escaped prefixes;
the hdlname attribute is used when present.
"""
import collections
import json
import sys

net = json.load(open(sys.argv[1]))
cells = net["modules"]["KL_pp_shadow"]["cells"]
count = collections.Counter()
for name, cell in cells.items():
    kind = cell["type"]
    if not (kind.startswith("RAM") or kind.startswith("DSP")):
        continue
    hdl = cell.get("attributes", {}).get("hdlname", "")
    path = hdl.split(" ") if hdl else name.lstrip("\\$").split(".")
    scope = "/".join(p for p in path[:3] if not p.startswith("$"))
    if "u_notify" in path:
        scope = "/".join(path[:path.index("u_notify") + 2])
    count[(scope, kind)] += 1
for (scope, kind), n in sorted(count.items()):
    print(f"{n:6d} {kind:10s} {scope}")
