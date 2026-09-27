#!/usr/bin/env python3
"""Cross-check the 50 MHz rerun figures on the baseline page against the committed manifest.

usage: check_page_figures.py REPO
Checks every numeric cell of the rerun section's tables, the stated deltas,
the capacity excess and the prose totals. Exit 1 on any disagreement.
"""
import json
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1])
page = (repo / "docs/findings/PP_SHADOW_BASELINE.md").read_text()
m = json.loads((repo / "docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json").read_text())["measurements"]
section = page.split("## 50 MHz 8x8 rerun", 1)[1].split("\n## ", 1)[0]
bad = 0


def num(cell):
    return float(cell.replace(",", "").replace("+", ""))


def row(label):
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == label:
            return cells[1:]
    raise KeyError(label)


def check(what, page_value, expected):
    global bad
    ok = abs(page_value - expected) < 1e-9
    bad += not ok
    print(f"{'OK  ' if ok else 'DIFF'} {what}: page={page_value} expected={expected}")


cols = ("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4")
tables = section.split("| Attribution-only 8x8 wrapper synthesis |")
default_rows = [l for l in tables[0].splitlines() if l.startswith("| ")]
attr_rows = [l for l in tables[1].splitlines() if l.startswith("| ")]


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


# Default whole-design table.
d = {r[0]: [num(x) for x in r[1:]] for r in map(cells, default_rows) if r[0].startswith(("Historical", "Declared", "50 MHz"))}
hist, new, delta = d["Historical 100 MHz, 2026-09-26"], d["Declared 50 MHz, 2026-09-27"], d["50 MHz minus historical 100 MHz"]
whole = m["default"]["metrics"]["alinx_ax7101"]
for i, c in enumerate(cols):
    check(f"default whole {c} vs manifest", new[i], whole[c])
check("default whole WNS vs manifest", new[6], whole["WNS_ns"])
for i in range(7):
    check(f"default delta column {i}", delta[i], round(new[i] - hist[i], 3))
# Attribution wrapper table.
a = {r[0]: [num(x) for x in r[1:]] for r in map(cells, attr_rows) if r[0].startswith(("Historical", "Declared", "50 MHz")) and "synthesis" not in r[0]}
hist_a, new_a, delta_a = a["Historical 100 MHz, 2026-09-26"], a["Declared 50 MHz, 2026-09-27"], a["50 MHz minus historical 100 MHz"]
wrap = m["attribution"]["metrics"]["milan_datapath/pp_shadow"]
for i, c in enumerate(cols):
    check(f"attribution wrapper {c} vs manifest", new_a[i], wrap[c])
check("attribution wrapper WNS vs manifest", new_a[6], wrap["internal_WNS_ns"])
for i in range(7):
    check(f"attribution delta column {i}", delta_a[i], round(new_a[i] - hist_a[i], 3))
# Historical rows must equal the #231 page rows retained elsewhere on the page.
check("historical default LUT equals #231 row", hist[0], 68136)
check("historical attribution LUT equals #231 row", hist_a[0], 29489)
# Prose.
check("capacity excess", num(re.search(r"remains ([\d,]+) above", section).group(1)), whole["LUT"] - 63400)
check("stated LUT reduction", num(re.search(r"That is ([\d,]+) fewer", section).group(1)), 68136 - whole["LUT"])
check("stated whole WNS", num(re.search(r"Whole-design WNS is (-?[\d.]+) ns", section).group(1)), whole["WNS_ns"])
aw = m["attribution"]["metrics"]["alinx_ax7101"]
check("attribution whole LUT prose", num(re.search(r"whole-design total is ([\d,]+) LUTs", section).group(1)), aw["LUT"])
check("attribution whole FF prose", num(re.search(r"It uses ([\d,]+) FFs", section).group(1)), aw["FF"])
check("attribution whole CARRY4 prose", num(re.search(r"and ([\d,]+) CARRY4s", section).group(1)), aw["CARRY4"])
check("attribution whole WNS prose", num(re.search(r"Its whole-design WNS is (-?[\d.]+) ns", section).group(1)), aw["WNS_ns"])
# Endpoint comparison row.
ep = cells(next(l for l in section.splitlines() if l.startswith("| Declared 50 MHz synthesis |")))
pairs = [tuple(num(x) for x in c.split(" / ")) for c in ep[1:]]
scopes = ["alinx_ax7101", "milan_datapath/pp_shadow", "milan_datapath/pp_shadow/u_pp/u_aecp",
          "milan_datapath/pp_shadow/u_pp/u_aecp/u_dyn"]
for (dv, av), s in zip(pairs, scopes):
    check(f"endpoint {s} default LUT", dv, m["default"]["metrics"][s]["LUT"])
    check(f"endpoint {s} attribution LUT", av, m["attribution"]["metrics"][s]["LUT"])
# Attribution scope subset table.
for line in section.splitlines():
    c = cells(line)
    if c and c[0].startswith("`u_") and len(c) == 8 and "/" not in c[1]:
        s = "milan_datapath/pp_shadow/" + c[0].strip("`")
        got = m["attribution"]["metrics"][s]
        for i, k in enumerate(cols):
            check(f"attribution subset {c[0]} {k}", num(c[i + 1]), got[k])
        check(f"attribution subset {c[0]} WNS", num(c[7]), got["internal_WNS_ns"])
# Boundary probe table.
names = {"`u_pp/u_aecp/u_dyn`": "milan_datapath/pp_shadow/u_pp/u_aecp/u_dyn",
         "`u_pp/u_aecp`": "milan_datapath/pp_shadow/u_pp/u_aecp",
         "`u_pp/u_srp`": "milan_datapath/pp_shadow/u_pp/u_srp",
         "`u_pp/u_notify`": "milan_datapath/pp_shadow/u_pp/u_notify",
         "`wrapper`": "milan_datapath/pp_shadow"}
for line in section.splitlines():
    c = cells(line)
    if c and c[0] in names and len(c) == 4:
        s = names[c[0]]
        probe = {v: {r["scope"]: r for r in m[v]["boundary_probe"]}[s] for v in ("default", "attribution")}
        for col, key in zip(c[1:], ("LUT", "LUT_all_loads_outside_wrapper",
                                    "LUT_outside_input_and_only_outside_loads")):
            dv, av = (num(x) for x in col.split(" / "))
            check(f"probe {c[0]} {key} default", dv, probe["default"][key])
            check(f"probe {c[0]} {key} attribution", av, probe["attribution"][key])
print(f"RESULT mismatches={bad}")
sys.exit(1 if bad else 0)
