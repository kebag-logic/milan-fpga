#!/usr/bin/env python3
"""Attribute flattened Yosys LUT cells to source scopes through the names of
the nets they drive (only nets with a public, non-$ name, or an hdlname).
usage: flat_scope.py <KL_pp_shadow.ooc.json>
Prints per scope (depth u_pp/<child>) LUT counts, and the unattributed rest."""
import collections, json, re, sys
m = json.load(open(sys.argv[1]))["modules"]["KL_pp_shadow"]
names = collections.defaultdict(list)
for name, net in m["netnames"].items():
    hd = net.get("attributes", {}).get("hdlname")
    for bit in net["bits"]:
        names[bit].append(hd.split() if hd else None if name.startswith("$") else re.split(r"[./]", name))
def scope(path):
    if path[0] == "u_pp":
        return "u_pp/" + (path[1] if len(path) > 2 else "@own")
    return path[0] if len(path) > 1 else "@own"
rows = collections.Counter()
for cell in m["cells"].values():
    if not re.fullmatch(r"LUT[1-6]", cell["type"]):
        continue
    cand = [p for p in names.get(cell["connections"]["O"][0], []) if p]
    if not cand:
        rows["@unattributed"] += 1
        continue
    # deepest name wins: it is closest to the originating module
    rows[scope(max(cand, key=len))] += 1
for k, v in rows.most_common():
    print(f"{k}\t{v}")
