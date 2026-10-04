import sys, re
from collections import defaultdict, Counter
from pathlib import Path
sys.path.insert(0, "$LANES/649-resmap/syn/resmap")
import resmap_map as M
d = Path("$VALIDATION_STORAGE/649-a527/route-map-2")
rows = M.hierarchy(d / "map_hierarchy.rpt")
root, children = M.tree_of(rows)
leaves = M.leaves_of(rows, children)
instances = {k for k in rows if not k.endswith("/@own")}
kinds = Counter()
pos = defaultdict(lambda: defaultdict(set))  # row -> column -> set
for line in (d / "map_cells.tsv").read_text().splitlines()[1:]:
    cell, prim, level, site, bel = line.split("\t")
    if level not in ("LEAF", "INTERNAL"):
        continue
    m = re.fullmatch(r"SLICE[LM]\.([A-D])[56]LUT", bel)
    if not m:
        continue
    if re.fullmatch(r"LUT[1-6]", prim):
        col = "logic_LUT"
    elif re.fullmatch(r"RAM[DS](32|64E)", prim):
        col = "LUTRAM"
    elif re.fullmatch(r"SRL(16E|C32E)", prim):
        col = "SRL"
    else:
        kinds[(prim, level, bel)] += 1
        continue
    p = (site, m.group(1))
    leaf = M.owner_of(cell, root, instances, children)
    node = leaf
    while True:
        pos[node][col].add(p)
        pos[node]["LUT"].add(p)
        if node.endswith("/@own"):
            node = node[:-5]
            continue
        if "/" not in node:
            break
        node = node.rsplit("/", 1)[0]
print("other LUT-bel kinds", kinds)
bad = 0
for k in rows:
    for col in ("LUT", "logic_LUT", "LUTRAM", "SRL"):
        got = len(pos[k][col])
        if got != rows[k][col]:
            bad += 1
            if bad < 40:
                print("MISMATCH", k, col, "census", got, "report", rows[k][col], "leaf" if k in leaves else "parent")
print("rows", len(rows), "mismatches", bad)
