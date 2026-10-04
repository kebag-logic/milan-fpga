#!/usr/bin/env python3
"""Independent re-reading of the census LUT tie and the LUT reconciliation (round 2).

Usage: check_census_lut.py <map dir with map_hierarchy.rpt and map_cells.tsv> <page.md>

Does not import the lane's scripts. Parses the hierarchical report by indentation,
assigns every LEAF/INTERNAL census cell on a [A-D][56]LUT BEL to its deepest
reported instance (or that instance's own row), counts distinct (slice, LUT letter)
sites per row and per ancestor, split by primitive, and compares every row's four
LUT columns. Then derives the leaf sum, each parent's sharing adjustment and the
census shared-site count, and checks the page's map-lut-sharing block against them.
"""
import re, sys
from collections import defaultdict
from pathlib import Path

d = Path(sys.argv[1]); page = Path(sys.argv[2]).read_text()
rows, stack = {}, []
for line in (d / "map_hierarchy.rpt").read_text().splitlines():
    if not line.startswith("| ") and not line.startswith("|  "):
        continue
    cells = line.split("|")
    if len(cells) != 12 or not cells[3].strip().isdigit():
        continue
    name_cell = cells[1]
    indent = (len(name_cell) - len(name_cell.lstrip(" ")) - 1) // 2
    name = name_cell.strip()
    vals = [int(c) for c in cells[3:11]]
    stack = stack[:indent]
    if name.startswith("(") and name.endswith(")") and indent > 0:
        key = "/".join(stack) + "/@own"
    else:
        stack.append(name)
        key = "/".join(stack)
    rows[key] = dict(zip(("LUT", "logic", "LUTRAM", "SRL", "FF", "RAMB36", "RAMB18", "DSP"), vals))
root = next(k for k in rows if "/" not in k)
parents = {k.rsplit("/", 1)[0] for k in rows if "/" in k}
leaves = [k for k in rows if k not in parents]
instances = {k for k in rows if not k.endswith("/@own")}
kind = lambda p: ("logic" if re.fullmatch(r"LUT[1-6]", p) else "LUTRAM" if re.fullmatch(r"RAM[DS](32|64E)", p)
                  else "SRL" if re.fullmatch(r"SRL(16E|C32E)", p) else None)
sites = defaultdict(lambda: defaultdict(set))
unknown = 0
with open(d / "map_cells.tsv") as fh:
    next(fh)
    for line in fh:
        cell, prim, level, site, bel = line.rstrip("\n").split("\t")
        m = re.fullmatch(r"SLICE[LM]\.([A-D])[56]LUT", bel)
        if level not in ("LEAF", "INTERNAL") or not m:
            continue
        k = kind(prim)
        if k is None:
            unknown += 1; continue
        parts = cell.split("/")[:-1]
        owner = None
        for cut in range(len(parts), -1, -1):
            key = "/".join([root, *parts[:cut]])
            if key in instances:
                owner = key + "/@own" if key in parents else key
                break
        node = owner
        while True:
            for col in ("LUT", k):
                sites[node][col].add((site, m.group(1)))
            if node == root:
                break
            node = node[:-5] if node.endswith("/@own") else node.rsplit("/", 1)[0]
mism = [(k, c, len(sites[k][c]), rows[k][c]) for k in rows for c in ("LUT", "logic", "LUTRAM", "SRL")
        if len(sites[k][c]) != rows[k][c]]
print(f"rows {len(rows)}, leaves {len(leaves)}, parents {len(parents)}, unknown LUT-BEL primitives {unknown}")
print(f"rows whose four LUT columns equal the census distinct LUT sites: {len(rows) - len({m[0] for m in mism})} of {len(rows)}")
for m in mism[:10]:
    print("MISMATCH", m)
leaf_sum = {c: sum(rows[l][c] for l in leaves) for c in ("LUT", "logic", "LUTRAM", "SRL")}
kids = defaultdict(list)
for k in rows:
    if "/" in k:
        kids[k.rsplit("/", 1)[0]].append(k)
adj = {p: rows[p]["LUT"] - sum(rows[k]["LUT"] for k in ks) for p, ks in kids.items()}
shared = {p: sum(len(sites[k]["LUT"]) for k in ks) - len(sites[p]["LUT"]) for p, ks in kids.items()}
nz = {p: a for p, a in adj.items() if a}
sub_nz = {c: sum(rows[p][c] - sum(rows[k][c] for k in ks) for p, ks in kids.items()) for c in ("logic", "LUTRAM", "SRL")}
print(f"leaf LUT sum {leaf_sum}; image LUT {rows[root]['LUT']}; difference {leaf_sum['LUT'] - rows[root]['LUT']}")
print(f"non-zero adjustments: {len(nz)}, sum {sum(nz.values())}; per sub-column adjustment sums {sub_nz}")
print(f"adjustment == -census shared sites for every parent: {all(adj[p] == -shared[p] for p in kids)}")
print(f"positive adjustments: {[p for p, a in adj.items() if a > 0]}")
# processor scopes
w = f"{root}/milan_datapath/pp_shadow"
inproc = [l for l in leaves if l == w or l.startswith(w + "/")]
print(f"leaves inside pp_shadow: {len(inproc)}; outside: {len(leaves) - len(inproc)}")
# page block
blk = re.search(r"<!-- table: map-lut-sharing -->\n(.*?)<!-- end table: map-lut-sharing -->", page, re.S).group(1)
lines = [l for l in blk.splitlines() if l.startswith("| ") and not l.startswith("| Scope")]
fails = []
num = lambda s: int(s.replace(",", "").replace("*", ""))
first = [c.strip() for c in lines[0].split("|")[1:-1]]
if first[0] != f"all {len(leaves)} blocks (leaves)" or num(first[1]) != leaf_sum["LUT"]:
    fails.append(f"leaf row {first}")
adj_rows = [l for l in lines if l.startswith("| sharing adjustment")]
if len(adj_rows) != len(nz):
    fails.append(f"page lists {len(adj_rows)} adjustments, census-derived {len(nz)}")
for l in adj_rows:
    c = [x.strip() for x in l.split("|")[1:-1]]
    label = re.search(r"`([^`]+)`", c[0]).group(1)
    key = root if label == root else f"{root}/{label}"
    if key not in nz or num(c[1]) != nz[key] or num(c[5]) != shared[key]:
        fails.append(f"row {label}: page {c[1]} / {c[5]}, derived {nz.get(key)} / {shared.get(key)}")
summ = [x.strip() for x in next(l for l in lines if l.startswith("| sum of")).split("|")[1:-1]]
if num(summ[1]) != sum(nz.values()) or num(summ[5]) != -sum(nz.values()):
    fails.append(f"sum row {summ}")
img = [x.strip() for x in lines[-1].split("|")[1:-1]]
if num(img[1]) != rows[root]["LUT"]:
    fails.append(f"image row {img}")
if leaf_sum["LUT"] + sum(nz.values()) != rows[root]["LUT"]:
    fails.append("leaves plus adjustments do not equal the image")
print(f"page map-lut-sharing rows: {len(lines)}; adjustment rows {len(adj_rows)}")
print("FAILURES" if fails or mism else "ALL CHECKS PASS", fails[:10])
sys.exit(1 if fails or mism else 0)
