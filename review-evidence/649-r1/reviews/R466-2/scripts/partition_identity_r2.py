#!/usr/bin/env python3
"""R466-2 probe, round 1's partition fuzz adapted to this head.
(a) Identity: on random hierarchies, the leaves plus the ancestry step's sharing adjustments equal the
    top row in every column whenever ancestry passes, so "Partition" can only be an identity.
(b) Real image: for every leaf and every parent row of the published route, move its LUT (and
    logic_LUT) figure by one in the report rows and record which tie catches it: ancestry alone, the
    census LUT tie, both, or neither. A change ancestry misses but the census catches is the leaf-LUT
    reading round 1 found missing.
Usage: partition_identity_r2.py <repo> <route_map dir with map_cells.tsv>"""
import copy, random, sys
from pathlib import Path
repo, mapdir = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "syn/resmap"))
import resmap_map as M
rng = random.Random(649)
broken = 0
for trial in range(20000):
    keys = ["top"]
    for _ in range(rng.randint(1, 12)):
        parent = rng.choice([k for k in keys if not k.endswith("/@own")])
        keys.append(f"{parent}/n{len(keys)}")
    for k in list(keys):
        if any(o.startswith(k + "/") for o in keys) and rng.random() < 0.7:
            keys.append(f"{k}/@own")
    rows = {k: {c: rng.randint(0, 9) for c in M.COLUMNS} for k in keys}
    root, children = M.tree_of(rows)
    leaves = M.leaves_of(rows, children)
    anc, adj = M.ancestry_ties(rows, children)
    if anc:
        continue
    for c in M.SHARED:
        if sum(rows[l][c] for l in leaves) + sum(a[c] for a in adj.values()) != rows[root][c]:
            broken += 1
print(f"(a) 20000 random hierarchies: identity broken with ancestry clean in {broken} cases")

rows = M.hierarchy(mapdir / "map_hierarchy.rpt")
root, children = M.tree_of(rows)
leaves = M.leaves_of(rows, children)
census = M.read_census(mapdir / "map_cells.tsv")
by_leaf = M.census_by_leaf(census, root, rows, children)
sites = M.lut_sites(census, root, rows, children)
anc0, adj0 = M.ancestry_ties(rows, children)
cen0 = M.census_ties(rows, leaves, by_leaf, sites, root)
print(f"(b) clean image: {len(rows)} rows, {len(leaves)} leaves, {len(children)} parents; ancestry failures "
      f"{len(anc0)}, census failures {len(cen0)}")
tally = {}
for key in rows:
    kind = "leaf" if key in leaves else "parent"
    for step in (-1, +1):
        if rows[key]["LUT"] + step < 0:
            continue
        planted = copy.deepcopy(rows)
        planted[key]["LUT"] += step
        planted[key]["logic_LUT"] += step
        anc, _ = M.ancestry_ties(planted, children)
        cen = M.census_ties(planted, leaves, by_leaf, sites, root)
        caught = ("ancestry " if anc else "") + ("census" if any("LUT sites" in f for f in cen) else "")
        caught = caught.strip() or "NOT CAUGHT"
        tally[(kind, step, caught)] = tally.get((kind, step, caught), 0) + 1
for (kind, step, caught), n in sorted(tally.items()):
    print(f"    {kind:6s} LUT {step:+d}: {n:4d} plants caught by {caught}")
missed = sum(n for (k, s, c), n in tally.items() if c == "NOT CAUGHT")
census_only = sum(n for (k, s, c), n in tally.items() if c == "census")
print(f"plants not caught: {missed}; caught by the census LUT tie alone (ancestry clean): {census_only}")
sys.exit(1 if broken or missed or anc0 or cen0 else 0)
