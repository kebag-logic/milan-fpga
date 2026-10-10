#!/usr/bin/env python3
"""Compare the composed pages' current-record figures with the recorded baseline.

Usage: python3 -I check_figures.py <candidate-checkout>
Reads syn/ooc/pp_resource_baseline.json, the "Current record" inventory of
docs/design/MARK_II_AREA_PLAN.md and the gate-record table of
docs/design/AREA_BUDGET.md; prints every compared figure and exits 1 on any
difference.
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
base = json.loads((root / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]
route = base["route-1x1"]["record"]
ooc1 = base["ooc-1x1"]["record"]
ooc8 = base["ooc-8x8"]["record"]
bad = 0
n = 0


def num(text):
    return float(text.replace(",", "").replace("+", ""))


def compare(label, page, recorded):
    global bad, n
    n += 1
    ok = abs(page - recorded) < 1e-9
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'} {label}: page {page:g} record {recorded:g}")


plan = (root / "docs/design/MARK_II_AREA_PLAN.md").read_text().splitlines()
start = next(i for i, l in enumerate(plan) if "source-scope references of the gate's current record" in l)
rows = 0
for line in plan[start:start + 60]:
    m = re.match(r"\| `([^`]+)` \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|", line)
    if not m:
        if rows and not line.startswith("|"):
            break
        continue
    rows += 1
    scope = m.group(1)

    def scope_lut(rec, name):
        scopes = rec["scopes"]
        return scopes[name]["LUT"] if name in scopes else None

    for col, rec in ((2, route), (3, ooc1), (4, ooc8)):
        rec_lut = scope_lut(rec, scope)
        if rec_lut is None and scope == "wrapper" and col > 2:
            rec_lut = rec["figures"]["LUT"]
        if rec_lut is None:
            print(f"BAD {scope} col{col}: scope not in record")
            bad += 1
            continue
        compare(f"MARK_II {scope} col{col - 1}", num(m.group(col)), rec_lut)
print(f"MARK_II current inventory rows: {rows}")

budget = (root / "docs/design/AREA_BUDGET.md").read_text()
f = route["figures"]
for label, pattern, key in (
        ("AREA_BUDGET Slice LUT", r"\| Slice LUT \| 63,400 \| ([\d,]+) \|", "LUT"),
        ("AREA_BUDGET Slice register", r"\| Slice register \| 126,800 \| ([\d,]+) \|", "FF"),
        ("AREA_BUDGET Slice", r"\| Slice \| 15,850 \| ([\d,]+) \|", "SLICE"),
        ("AREA_BUDGET BRAM tile", r"\| Block RAM tile \| 135 \| ([\d.]+) \|", "BRAM_TILE"),
        ("AREA_BUDGET DSP", r"\| DSP \| 240 \| ([\d,]+) \|", "DSP"),
        ("AREA_BUDGET WNS", r"\| WNS / WHS \| - \| ([+\-\d.]+) / ", "WNS_ns"),
        ("AREA_BUDGET WHS", r"\| WNS / WHS \| - \| [+\-\d.]+ / ([+\-\d.]+) ns", "WHS_ns")):
    m = re.search(pattern, budget)
    if not m:
        print(f"BAD {label}: row not found")
        bad += 1
        continue
    compare(label, num(m.group(1)), f[key])
m = re.search(r"At the current \+([\d.]+) ns WNS record", budget)
compare("AREA_BUDGET gate-comparison WNS", num(m.group(1)), f["WNS_ns"])
m = re.search(r"At the current \+([\d.]+) ns WNS record", "\n".join(plan))
compare("MARK_II gate-comparison row WNS", num(m.group(1)), f["WNS_ns"])
m = re.search(r"that stack names ([\d,]+) LUTs", budget)
print(f"info AREA_BUDGET datapath stack {m.group(1)} (milan_datapath scope not in record scopes: "
      f"{'milan_datapath' in route['scopes']})")
compare("AREA_BUDGET wrapper", num(re.search(r"The wrapper names ([\d,]+) of them", budget).group(1)),
        route["scopes"]["wrapper"]["LUT"])
print(f"figures compared: {n}, differences: {bad}")
sys.exit(1 if bad else 0)
