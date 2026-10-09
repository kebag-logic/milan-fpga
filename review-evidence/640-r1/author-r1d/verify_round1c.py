"""Recompute Round 1c scenario rows from stored scopes and lane assumptions."""
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
record_path = "syn/ooc/pp_resource_baseline.json"
raw = (root / record_path).read_bytes()
original = subprocess.check_output(["rtk", "proxy", "git", "show", "c4b8b7d3:" + record_path], cwd=root)
assert raw == original, "Resource record changed"
record = json.loads(raw)["endpoints"]
scopes = record["ooc-1x1"]["record"]["scopes"]
base = record["route-1x1"]["record"]["figures"]["LUT"]
plan = (root / "docs/design/MARK_II_AREA_PLAN.md").read_text()
budget = (root / "docs/design/AREA_BUDGET.md").read_text()

def table(text, header):
    tail = text.split(header, 1)[1].splitlines()[2:]
    rows = []
    for line in tail:
        if not line.startswith("|"):
            break
        rows.append([c.strip() for c in line.strip("|").split("|")])
    assert rows, header
    return rows

def number(s):
    return int(s.replace(",", "").replace("+", ""))

lanes = {}
for row in table(plan, "| Lane | Default saving, central (range) | Basis and overlap exclusion |"):
    if row[0].split()[0] in ("M3", "M10"):
        continue
    central, low, high = map(number, re.findall(r"[0-9][0-9,]*", row[1]))
    lanes[row[0].split()[0]] = [low, central, high]
# Named cells have no anonymous-cell credit.
for i, (share, debit) in enumerate(((0.50, 400), (0.75, 250), (1.00, 100))):
    assert int((1696 * share - debit) // 100) * 100 == lanes["M8a"][i]
sums = [sum(values[i] for values in lanes.values()) for i in range(3)]
partial_gross = sum(scopes[key]["LUT"] for key in (
    "u_pp/u_adp", "u_pp/u_listener", "u_pp/u_lsn_admit", "u_pp/u_talker",
    "u_pp/u_nvm_shadow", "u_pp/u_srp")) + 429
assert partial_gross == 8012
partial_credit = [partial_gross - 3102 - allowance for allowance in (3500, 1000, -1000)]
partial_rows = table(plan, "| Partial split case | Calculation | Estimated split saving |")
assert [number(row[2]) for row in partial_rows] == partial_credit
m3m10 = [1500 + 900, 2600 + 1200, 3600 + 1500]
full_credit = [11500, 14000, 16000]
expected = {}
for i, case in enumerate(("Conservative", "Central", "Optimistic")):
    expected[("Full split", case)] = base - full_credit[i] - sums[i]
    expected[("No split, including M3/M10", case)] = base - sums[i] - m3m10[i]
    expected[("Partial, F5 unqualified", case)] = base - partial_credit[i] - sums[i] - m3m10[i]
header = "| Placement | Case | Estimated image LUT | Headroom to 38,040 | Headroom to 37,659 |"
count = 0
for label, text in (("plan", plan), ("budget", budget)):
    rows = table(text, header)
    assert len(rows) == len(expected)
    seen = set()
    for row in rows:
        key = tuple(row[:2]); assert key not in seen; seen.add(key)
        value = expected[key]
        assert list(map(number, row[2:])) == [value, 38040 - value, 37659 - value], (label, row, value)
        count += 3
    assert seen == set(expected)
assert expected[("Partial, F5 unqualified", "Central")] + lanes["M8b"][1] == 39657
assert expected[("Full split", "Conservative")] + lanes["M8b"][0] == 37167
for name in ("MilanMAC.tx_sf", "MilanMAC.mac_tx_cdc", "MilanMAC.mac_rx_cdc", "milan_axil_cdc"):
    assert name in plan
for name in ("MARK_II_AREA_PLAN.md", "AREA_BUDGET.md"):
    text = (root / "docs/design" / name).read_text()
    visible = re.sub(r"\[[^\n]*?\]\([^\n]*?\)", "", text)
    assert not re.search(r"#[0-9]+", visible), name
print(f"PASS: {count} scenario cells; M8a packing arithmetic; partial removal; conditional-core cases; named FIFOs; issue links; unchanged resource record")
for key, value in expected.items():
    print(f"{key[0]} / {key[1]}: {value}; headroom {38040-value} / {37659-value}")
