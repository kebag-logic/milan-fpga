"""Recompute the memory ledger from resource records and the prior SoC census.

Usage: python3 verify_round1d.py REPOSITORY
This checks documentation arithmetic, not physical implementation capacity.
Preflight source: issue #665, comment 6081556432.
Allocation source: issue #640, comment 6081706413.
"""
import json
import math
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
plan = (root / "docs/design/MARK_II_AREA_PLAN.md").read_text()
budget = (root / "docs/design/AREA_BUDGET.md").read_text()
census = (root / "docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md").read_text()
record_path = "syn/ooc/pp_resource_baseline.json"
raw = (root / record_path).read_bytes()
original = subprocess.check_output(
    ["rtk", "proxy", "git", "show", "39258a1486897127288f82fbb1b86333febf6f00:" + record_path], cwd=root)
assert raw == original, "Resource record changed"
ep = json.loads(raw)["endpoints"]["route-1x1"]
scopes = ep["record"]["scopes"]
figures = ep["record"]["figures"]

def table(text, header):
    assert text.count(header) == 1, header
    rows = []
    for line in text.split(header, 1)[1].splitlines()[2:]:
        if not line.startswith("|"):
            break
        rows.append([x.strip() for x in line.strip("|").split("|")])
    assert rows, header
    return rows

def num(text):
    return float(text.replace(",", ""))

def pair(scope):
    return (scopes[scope]["RAMB36"], scopes[scope]["RAMB18"])

def add(items):
    values = list(items)
    return tuple(sum(v[i] for v in values) for i in (0, 1))

def tiles(p):
    return p[0] + p[1] / 2

base = (figures["RAMB36"], figures["RAMB18"])
assert tiles(base) == figures["BRAM_TILE"] == 87.5
credited = add(pair(s) for s in ("u_pp/u_aecp", "u_pp/u_srp"))
assert credited == (6, 1)
remaining = [*(f"u_pp/g_rx_pool[{i}].u_rx_slots" for i in (0, 1, 2, 4, 5)),
             "u_pp/u_mrp_strip", "u_pp/u_tx_slots", "u_pp/u_timer", "u_pp/u_trace",
             "u_pp/u_rx_validator", "ctl_fifo"]
released = add(pair(s) for s in remaining)
assert released == (10, 2)
assert add((credited, released)) == pair("wrapper"), "Release credits must partition wrapper storage"
reuse_row = next(row for row in table(census, "| Name class | FF | IOB FF | LUT cells | LUT-RAM cells | RAMB36 | RAMB18 | DSP |")
                 if row[0] == "BIOS ROM and SRAM")
reuse = tuple(int(v) for v in reuse_row[5:7])
assert reuse == (18, 1)
mailbox = (1, 10)
mailbox_text = (root / "docs/design/MAILBOX_SPLIT.md").read_text()
ring_row = next(row for row in table(mailbox_text, "| Block | LUT | FF | RAMB36 | RAMB18 |")
                if row[0] == "the eleven rings (flattened into `KL_mbx`)")
assert tuple(int(v) for v in ring_row[3:5]) == mailbox
# The debit is the published measured mailbox allocation, not a new synthesis.
deltas = [base, tuple(-v for v in credited), mailbox,
          tuple(-v for v in reuse), (50, 0), (2, 0), tuple(-v for v in released)]
header = "| Item | RAMB36 delta | RAMB18 delta | Tile delta | Image tiles after |"
checked = 0
for name, text in (("plan", plan), ("budget", budget)):
    rows = table(text, header)
    assert len(rows) == len(deltas)
    cumulative = 0
    for row, delta in zip(rows, deltas):
        cumulative += tiles(delta)
        expected = [*delta, tiles(delta), cumulative]
        assert [num(x) for x in row[1:]] == expected, (name, row, expected)
        print(name, row[0], expected)
        checked += 4
assert table(plan, header) == table(budget, header)
release_rows = table(plan, "| Released fabric scope, relative to wrapper | RAMB36 | RAMB18 | Tiles |")
release_groups = [add(pair(s) for s in remaining[:5]), *(pair(s) for s in remaining[5:]), released]
assert len(release_rows) == len(release_groups)
for row, p in zip(release_rows, release_groups):
    assert [num(x) for x in row[1:]] == [*p, tiles(p)], row
    checked += 3
preflight_rows = table(plan, "| Preflight shape | Linked span, bytes | Status |")
assert [num(r[1]) for r in preflight_rows] == [94688, 147360]
sections = 56948 + 3458 + 0 + 78744 + 8192
assert sections == 147342
assert sections + 18 == 147360
assert math.ceil(224 * 1024 / 4608) == 50
assert math.ceil(224 * 1024 / 4096) == 56
pre_release = sum(tiles(d) for d in deltas[:-1])
full_release = pre_release - tiles(released)
ceiling = ep["ceiling"]["BRAM_TILE"]
assert (pre_release, full_release, ceiling) == (120.5, 109.5, 121.5)
assert 135 - ceiling == 13.5
assert ceiling - pre_release == 1
assert ceiling - full_release == 12
assert pre_release + tiles(reuse) == 139
assert full_release + tiles(reuse) == 128
assert full_release + 56 - 50 == 115.5
assert ceiling - (full_release + 56 - 50) == 6
partial = pre_release + tiles(pair("u_pp/u_aecp"))
assert partial == 126.5 and partial - ceiling == 5
for text in (plan, budget):
    for token in ("224 KB", "50 RAMB36", "94,688", "147,360", "126.5", "115.5"):
        assert token in text, token
    for comment in ("6081706413", "6081556432", "6081705916"):
        assert f"issuecomment-{comment}" in text
    for phrase in ("M0s", "default flip", "five largest BSS"):
        assert phrase in text
print(f"PASS: {checked} memory table cells; wrapper partition; historical reuse; F5 spans; packing arithmetic; partial placement; reserve; unchanged record")
