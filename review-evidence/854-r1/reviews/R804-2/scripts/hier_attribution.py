#!/usr/bin/env python3
"""Area attribution check over the published route hierarchy reports.
Usage: hier_attribution.py <author-r2/receipts/area/runs directory>
Prints (1) every instance down to depth 4 whose FF count differs between the
ExtraPostPlacementOpt (eppo) and AltSpreadLogic_high (aslh) routes at the head,
and (2) for the wrapper KL_pp_shadow, its total, its own-cell row and the sum
of its children, for each route and standalone run, showing whether the
hierarchical LUT totals are additive."""
import pathlib, sys

def rows(path):
    out, stack = {}, []
    for line in open(path):
        if not line.startswith("|") or "Instance" in line:
            continue
        cells = line.rstrip("\n").split("|")[1:-1]
        if len(cells) < 8:
            continue
        name = cells[0]
        indent = len(name) - len(name.lstrip())
        try:
            lut, ff = int(cells[2]), int(cells[6])
        except ValueError:
            continue
        while stack and stack[-1][0] >= indent:
            stack.pop()
        stack.append((indent, name.strip()))
        out["/".join(s[1] for s in stack)] = (lut, ff)
    return out

runs = pathlib.Path(sys.argv[1])
a, b = rows(runs / "eppo/baseline_hierarchy.rpt"), rows(runs / "aslh/baseline_hierarchy.rpt")
print("# FF differences, head ExtraPostPlacementOpt minus head AltSpreadLogic_high (depth <= 4)")
for key in a:
    if key in b and a[key][1] != b[key][1] and key.count("/") <= 4:
        print(f"  {key}: FF {a[key][1] - b[key][1]:+d}  eppo {a[key]}  aslh {b[key]}")
print("# wrapper: total, own-cell row, children sum (LUT, FF)")
for run in ("eppo", "aslh", "eto", "ooc-1x1", "ooc-8x8"):
    h = rows(runs / run / "baseline_hierarchy.rpt")
    tops = [k for k in h if k.split("/")[-1] in ("pp_shadow", "KL_pp_shadow")]
    if not tops:
        print(f"  {run}: no wrapper row"); continue
    top = min(tops, key=len)
    depth = top.count("/") + 1
    kids = {k: v for k, v in h.items() if k.startswith(top + "/") and k.count("/") == depth}
    own = [v for k, v in kids.items() if k.split("/")[-1].startswith("(")]
    children = {k.split("/")[-1]: v for k, v in kids.items() if not k.split("/")[-1].startswith("(")}
    csum = (sum(v[0] for v in children.values()), sum(v[1] for v in children.values()))
    print(f"  {run}: total {h[top]}  own-cell row {own[0] if own else None}  children {sorted(children)} sum {csum}"
          f"  total-minus-children ({h[top][0] - csum[0]}, {h[top][1] - csum[1]})")
