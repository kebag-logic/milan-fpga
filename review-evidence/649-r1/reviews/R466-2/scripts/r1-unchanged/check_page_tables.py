#!/usr/bin/env python3
"""R466 probe: compare every delimited table block on the findings page with the
published generated tables.md, and the map tables with the published map outputs;
re-tie the published map.json against the route-1x1 record (totals and every
processor scope). Usage: check_page_tables.py <repo> <evidence author dir>"""
import json, re, sys
from pathlib import Path
repo, ev = Path(sys.argv[1]), Path(sys.argv[2])
page = (repo / "docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md").read_text()
BLOCK = re.compile(r"<!-- table: ([a-z0-9-]+) -->\n(.*?)<!-- end table: \1 -->", re.S)
pblocks = dict(BLOCK.findall(page))
gblocks = dict(BLOCK.findall((ev / "receipts/tables.md").read_text()))
bad = 0
print(f"page blocks {len(pblocks)}, generated blocks {len(gblocks)}")
for name, body in pblocks.items():
    if name not in gblocks:
        print("MISSING in generated:", name); bad += 1
    elif gblocks[name] != body:
        print("DIFFERS:", name); bad += 1
print("generated but not on page:", sorted(set(gblocks) - set(pblocks)))
# map tables against map outputs
ranking = (ev / "receipts/blocks_ranked.md").read_text()
if pblocks.get("map-ranking") != ranking:
    print("map-ranking differs from blocks_ranked.md"); bad += 1
part = (ev / "receipts/partition.md").read_text()
for n in ("map-image", "map-datapath", "map-soc-names"):
    if pblocks[n] not in part:
        print(n, "not found verbatim in partition.md"); bad += 1
# record tie from map.json
m = json.loads((ev / "receipts/map.json").read_text())
rec = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]["route-1x1"]["record"]
figs, scopes = rec["figures"], rec.get("scopes", {})
table, root = m["table"], m["root"]
top = table[root]
for c in ("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4", "SLICE"):
    ok = abs(top[c] - figs[c]) < 1e-6
    bad += not ok
    print(f"record {c}: map {top[c]} record {figs[c]} {'OK' if ok else 'MISMATCH'}")
wrapper = next(k for k in table if k.endswith("/milan_datapath/pp_shadow"))
n_ok = 0
for scope, vals in scopes.items():
    key = wrapper if scope == "wrapper" else f"{wrapper}/{scope}"
    row = table.get(key)
    if row is None or any(row.get(c) != v for c, v in vals.items()):
        print("SCOPE MISMATCH", scope, vals, row and {c: row.get(c) for c in vals}); bad += 1
    else:
        n_ok += 1
print(f"processor scopes in record: {len(scopes)}, matching: {n_ok}; columns compared: {sorted({c for v in scopes.values() for c in v})}")
leaves = m["leaves"]
print("leaves", len(leaves), "depth", m["depth"])
for c in ("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4", "SLICE", "IOB_FF"):
    s = sum(table[l][c] for l in leaves)
    print(f"leaf sum {c}: {round(s, 2)} (top {top[c]})")
adj = sum(a.get("LUT", 0) for a in m["adjustments"].values())
print("total LUT sharing adjustment", adj, "nonzero parents", {k.split('/')[-1] if '/' in k else k: v['LUT'] for k, v in m['adjustments'].items() if v.get('LUT')})
print("RESULT", "PASS" if not bad else f"FAIL {bad}")
sys.exit(1 if bad else 0)
