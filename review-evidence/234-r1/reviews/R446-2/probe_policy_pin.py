#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: check-baseline's pin between the baseline JSON and the AREA_BUDGET.md table.

1. The round-1 table (2a765a6c, prose cells) and the round-2 table (one value
   per cell) carry the same values, and both equal the JSON policy.
2. Every non-dash table cell bumped, every dash given a value and every value
   replaced by a dash, one at a time in a copy of the real page: check-baseline
   must exit 2.
3. Every JSON policy value bumped, removed, and one extra policy figure added,
   one at a time in a copy of the real baseline: check-baseline must exit 2.

Usage: probe_policy_pin.py <checkout> <scratch-dir>; exit 0 when every case holds.
"""

import copy
import json
from pathlib import Path
import re
import subprocess
import sys

REPO, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(REPO / "syn/ooc"))
import pp_resource_gate as gate  # noqa: E402

PAGE = (REPO / "docs/design/AREA_BUDGET.md").read_text()
BASE = json.loads((REPO / "syn/ooc/pp_resource_baseline.json").read_text())
OLD = subprocess.run(["git", "-C", str(REPO), "show", "2a765a6c3:docs/design/AREA_BUDGET.md"],
                     capture_output=True, text=True, check=True).stdout
JSON_DIFF = subprocess.run(["git", "-C", str(REPO), "diff", "--stat", "2a765a6c3", "HEAD", "--",
                            "syn/ooc/pp_resource_baseline.json"], capture_output=True, text=True, check=True).stdout
bad = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global bad
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {label}{' -- ' + detail if detail else ''}")


def audit(page: str | None = None, base: dict | None = None) -> tuple[int, str]:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    (SCRATCH / "budget.md").write_text(PAGE if page is None else page)
    (SCRATCH / "baseline.json").write_text(json.dumps(BASE if base is None else base))
    result = subprocess.run([sys.executable, "-B", str(REPO / "syn/ooc/pp_resource_gate.py"), "check-baseline",
                             "--baseline", str(SCRATCH / "baseline.json"), "--budget", str(SCRATCH / "budget.md")],
                            capture_output=True, text=True)
    return result.returncode, (result.stdout + result.stderr).strip().replace("\n", " | ")


# 1. Values: round-1 prose table, round-2 table and JSON.
new = gate.policy_table(PAGE)
policy = {name: {field: {k: float(v) for k, v in entry.get(field, {}).items()} for field in gate.POLICY}
          for name, entry in BASE["endpoints"].items()}
check("JSON baseline unchanged since round 1", JSON_DIFF.strip() == "", JSON_DIFF.strip())
check("round-2 table parses to the JSON policy", new == policy)
old_rows = {m[1]: m[2] for m in re.finditer(r"^\| `([\w-]+)` \| (.+) \|$", OLD, re.M)}
expected_old = {
    "route-1x1": "+500 | +600 | +80 | +0 each | WNS at least +0.030 ns and WHS at least 0 ns; neither falls by "
                 "more than 0.25 ns | 121.5 BRAM tiles",
    "ooc-1x1": "+250 | +250 | - | +0 each | not gated: no I/O constraints | -",
    "ooc-8x8": "+316 | +339 | - | +0 each | not gated | -"}
check("round-1 table rows are the three read here", {k: old_rows.get(k) for k in expected_old} == expected_old,
      str({k: old_rows.get(k) for k in expected_old}))
old_policy = {
    "route-1x1": {"tolerance": {"LUT": 500.0, "FF": 600.0, "SLICE": 80.0, "RAMB36": 0.0, "RAMB18": 0.0, "DSP": 0.0,
                                "WNS_ns": 0.25, "WHS_ns": 0.25},
                  "floor": {"WNS_ns": 0.03, "WHS_ns": 0.0}, "ceiling": {"BRAM_TILE": 121.5}},
    "ooc-1x1": {"tolerance": {"LUT": 250.0, "FF": 250.0, "RAMB36": 0.0, "RAMB18": 0.0, "DSP": 0.0},
                "floor": {}, "ceiling": {}},
    "ooc-8x8": {"tolerance": {"LUT": 316.0, "FF": 339.0, "RAMB36": 0.0, "RAMB18": 0.0, "DSP": 0.0},
                "floor": {}, "ceiling": {}}}
check("round-1 table values (read by hand above) equal the round-2 table", old_policy == new)
status, out = audit()
check("real page and real baseline pass", status == 0, out)

# 2. Table cells.
head = "| Endpoint | " + " | ".join(gate.COLUMNS) + " |"
lines = PAGE.splitlines(keepends=True)
start = next(i for i, line in enumerate(lines) if line.strip() == head)
row_index = start + 2
while lines[row_index].startswith("|"):
    cells = lines[row_index].strip().strip("|").split("|")
    for col in range(1, len(cells)):
        cell = cells[col].strip()
        if cell == "-":
            variants = [("dash given a value", "+5")]
        else:
            number = re.match(r"([+-]?)(\d+(?:\.\d+)?)", cell)
            bumped = f"{number[1]}{float(number[2]) + 1:g}" + (" ns" if cell.endswith(" ns") else "")
            variants = [("value bumped", bumped), ("value replaced by a dash", "-")]
        for what, replacement in variants:
            changed = list(cells)
            changed[col] = f" {replacement} "
            page = "".join(lines[:row_index] + ["|" + "|".join(changed) + "|\n"] + lines[row_index + 1:])
            status, out = audit(page=page)
            column = list(gate.COLUMNS)[col - 1]
            check(f"table {cells[0].strip()} {column}: {what} ({cell!r} -> {replacement!r}) refused",
                  status == 2, out[:160])
    row_index += 1

# 3. JSON values.
for name, entry in BASE["endpoints"].items():
    for field in gate.POLICY:
        for figure, value in entry.get(field, {}).items():
            for what, edit in (("bumped", lambda d: d.__setitem__(figure, value + 1)),
                               ("removed", lambda d: d.pop(figure))):
                base = copy.deepcopy(BASE)
                edit(base["endpoints"][name][field])
                status, out = audit(base=base)
                check(f"JSON {name} {field} {figure}: {what} refused", status == 2, out[:160])
    for field, figure in (("ceiling", "LUT"), ("floor", "WNS_ns"), ("tolerance", "CARRY4")):
        if figure in entry.get(field, {}):
            continue
        base = copy.deepcopy(BASE)
        base["endpoints"][name].setdefault(field, {})[figure] = 10 ** 6
        status, out = audit(base=base)
        check(f"JSON {name} {field} {figure}: extra figure added refused", status == 2, out[:160])

print(f"policy pin probe: {bad} case(s) not as expected")
sys.exit(1 if bad else 0)
