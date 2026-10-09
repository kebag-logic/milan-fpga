#!/usr/bin/env python3
"""Recompute the Mark II plan's recorded-baseline figures and ledger arithmetic.

Usage: recompute_ledger.py <repo>
Reads docs/design/MARK_II_AREA_PLAN.md, docs/design/AREA_BUDGET.md and
syn/ooc/pp_resource_baseline.json from <repo> (read-only) and prints one
CHECK line per figure: OK or FAIL with both values. Exit 0 only when every
check passes. Informational NOTE lines carry reviewer-derived scenarios.
"""
import json
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1])
plan = (repo / "docs/design/MARK_II_AREA_PLAN.md").read_text()
budget = (repo / "docs/design/AREA_BUDGET.md").read_text()
rec = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]
fails = 0


def check(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"CHECK {'OK  ' if ok else 'FAIL'} {name}: document {got} / recomputed {want}")


def num(s):
    s = s.strip().strip("*").replace(",", "")
    return float(s) if "." in s else int(s)


def table_after(text, header_start):
    """Rows (cell lists) of the first Markdown table whose header line starts with header_start."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(header_start):
            rows = []
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                rows.append([c.strip() for c in row.strip().strip("|").split("|")])
            return rows
    raise SystemExit(f"table not found: {header_start}")


F = {e: rec[e]["record"]["figures"] for e in rec}
S = {e: rec[e]["record"]["scopes"] for e in rec}
L = lambda e, s: S[e][s]["LUT"]

# 1. Recorded endpoint table.
for row in table_after(plan, "| Endpoint | LUT | FF | Slice | RAMB36"):
    ep = row[0].strip("`")
    f = F[ep]
    check(f"{ep} LUT", num(row[1]), f["LUT"])
    check(f"{ep} FF", num(row[2]), f["FF"])
    if row[3] != "--":
        check(f"{ep} slice", num(row[3]), f["SLICE"])
    check(f"{ep} RAMB36", num(row[4]), f["RAMB36"])
    check(f"{ep} RAMB18", num(row[5]), f["RAMB18"])
    check(f"{ep} BRAM tiles", num(row[6]), f["BRAM_TILE"])
    check(f"{ep} DSP", num(row[7]), f["DSP"])
    wns, whs = [float(x) for x in row[8].replace("+", "").split("/")]
    check(f"{ep} WNS", wns, f["WNS_ns"])
    check(f"{ep} WHS", whs, f["WHS_ns"])

# 2. Input digests.
for row in table_after(plan, "| Endpoint | Input SHA-256 |"):
    ep = row[0].strip("`")
    check(f"{ep} inputs_sha256", row[1].strip("`"), rec[ep]["record"]["inputs_sha256"])

# 3. Current processor inventory (route / ooc-1x1 / ooc-8x8 per scope).
for row in table_after(plan, "| Scope relative to wrapper |"):
    sc = row[0].strip("`")
    for col, ep in ((1, "route-1x1"), (2, "ooc-1x1"), (3, "ooc-8x8")):
        check(f"{sc} {ep}", num(row[col]), L(ep, sc))

# 4. Derived device figures (xc7a100t: 63,400 LUT, 15,850 slices, 135 BRAM tiles).
r = F["route-1x1"]
check("limit 60 percent of 63,400", round(0.60 * 63400), 38040)
check("excess over limit", 50267 - 38040, r["LUT"] - 38040)
check("1 percent margin bar (floor)", 37659, int(38040 * 0.99))
check("WNS needed for 0.25 ns fall", 0.049, round(r["WNS_ns"] - rec["route-1x1"]["tolerance"]["WNS_ns"], 3))
check("free slices", 71, 15850 - r["SLICE"])
check("free BRAM tiles", 47.5, 135 - r["BRAM_TILE"])
check("ceiling allowance tiles", 34.0, rec["route-1x1"]["ceiling"]["BRAM_TILE"] - r["BRAM_TILE"])

# 5. Default split basis.
o = lambda s: L("ooc-1x1", s)
basis = {
    "ADP": o("u_pp/u_adp"),
    "ACMP listener and listener admission": o("u_pp/u_listener") + o("u_pp/u_lsn_admit"),
    "ACMP talker": o("u_pp/u_talker"),
    "Originator": o("u_pp/u_originator"),
    "ACMP binding store": o("u_pp/u_nvm_shadow"),
    "SRP": o("u_pp/u_srp"),
    "AECP, including microcode, descriptor and D3 stores": o("u_pp/u_aecp"),
    "Notification": o("u_pp/u_notify"),
    "NVM port and arbiter": o("u_pp/u_nvm_port") + o("u_pp/u_nvm_arb"),
    "Wrapper NVM backend": o("u_nvm"),
}
rows = table_after(plan, "| Removed function | OOC 1x1 LUT basis |")
for row in rows:
    name = row[0].strip("*")
    if name in basis:
        check(f"basis {name}", num(row[1]), basis[name])
sub = sum(basis.values())
check("disjoint wrapper subtotal", num([r_ for r_ in rows if "subtotal" in r_[0]][0][1]), sub)
check("gross reference (+ parent MAAP 429)", num([r_ for r_ in rows if "Gross" in r_[0]][0][1]), sub + 429)
check("uncredited standalone residual", 5501, o("wrapper") - sub)
tiles = sum(S["ooc-1x1"][k]["RAMB36"] + S["ooc-1x1"][k]["RAMB18"] / 2 for k in (
    "u_pp/u_adp", "u_pp/u_listener", "u_pp/u_lsn_admit", "u_pp/u_talker", "u_pp/u_originator",
    "u_pp/u_nvm_shadow", "u_pp/u_srp", "u_pp/u_aecp", "u_pp/u_notify", "u_pp/u_nvm_port",
    "u_pp/u_nvm_arb", "u_nvm"))
check("credited BRAM tiles", 6.5, tiles)
check("mailbox tiles (1 RAMB36 + 10 RAMB18)", 6.0, 1 + 10 / 2)
gross = sub + 429
check("central split", 14005, gross - 3102 - 1000)
check("conservative split", 11505, gross - 3102 - 2000 - 1500)
check("optimistic split", 16005, gross - 3102 - 500 + 1500)

# 6. Cumulative default-image table.
lanes = [("F0-F5", 14000, 11500, 16000), ("M2", 200, 100, 400), ("M5", 600, 400, 1000),
         ("M6", 600, 400, 900), ("M7", 500, 300, 700), ("M8a", 1000, 400, 1500),
         ("M8b", 1700, 1300, 2200), ("M3 and M10", 0, 0, 0)]
c = k = p = r["LUT"]
cum = table_after(plan, "| Order | Lane | Saving | Central image |")
for (name, mid, lo, hi), row in zip(lanes, cum[1:]):
    c, k, p = c - mid, k - lo, p - hi
    check(f"cumulative {name} central", num(row[3]), c)
    check(f"cumulative {name} conservative", num(row[4]), k)
    check(f"cumulative {name} optimistic", num(row[5]), p)
check("central headroom", 6373, 38040 - c)
check("central headroom percent", 16.75, round(100 * (38040 - c) / 38040, 2))
check("conservative headroom", 2173, 38040 - k)
check("conservative headroom percent", 5.71, round(100 * (38040 - k) / 38040, 2))
check("conservative without M8b", 37167, k + 1300)
check("M8 lane row central/low/high", (2700, 1700, 3700), (1000 + 1700, 400 + 1300, 1500 + 2200))

# 7. M3 basis.
aecp_own = o("u_pp/u_aecp") - sum(o(f"u_pp/u_aecp/{x}") for x in ("u_d3", "u_dyn", "u_store", "u_ucpu", "u_resp"))
check("AECP own logic (ooc-1x1)", 1302, aecp_own)
check("AECP dispatch queue (ooc-1x1)", 421, o("u_pp/u_dispatch/u_aecp_q"))
m3 = 0.6 * o("u_pp/u_notify") + 0.7 * (o("u_pp/u_aecp/u_d3") + o("u_pp/u_aecp/u_dyn")) + 0.5 * aecp_own + 0.4 * o("u_pp/u_dispatch/u_aecp_q")
check("M3 displaced (about 3,380)", 3380, round(m3, -1))
check("M10 routed AECP engine bound", 1727, L("route-1x1", "u_pp/u_aecp/u_ucpu"))

# 8. AREA_BUDGET agreement with the plan.
for row in table_after(budget, "| Lane | Estimated saving, central | Image after, central |"):
    if row[2][0].isdigit():
        found = [x for x in cum if x[1].split(",")[0].split(" ")[0] in row[0]]
    want = {"F0-F5 split": 36267, "M2 retained SoC tables": 36067, "M5 CSR read path": 35467,
            "M6 media contexts": 34867, "M7 gPTP tables": 34367, "M8a on-chip main memory": 33367,
            "M8b smaller cacheless RV32I": 31667, "M3 residual fabric AECP": 31667,
            "M10 shared gPTP/AECP engine": 31667}
    if row[0] in want:
        check(f"AREA_BUDGET {row[0]}", num(row[2]), want[row[0]])
for row in table_after(budget, "| Recorded endpoint | LUT | FF |"):
    ep = row[0].strip("`")
    check(f"AREA_BUDGET {ep} LUT", num(row[1]), F[ep]["LUT"])
    check(f"AREA_BUDGET {ep} FF", num(row[2]), F[ep]["FF"])
    r36, r18 = [int(x) for x in row[3].split("/")]
    check(f"AREA_BUDGET {ep} RAMB36/18", (r36, r18), (F[ep]["RAMB36"], F[ep]["RAMB18"]))
    check(f"AREA_BUDGET {ep} DSP", num(row[4]), F[ep]["DSP"])

# 9. Reviewer scenarios (informational).
no_split_table = r["LUT"] - (200 + 600 + 600 + 500 + 1000 + 1700)
print(f"NOTE no-split central, M2..M8b only (the plan's 45,667): {no_split_table}")
print(f"NOTE no-split central, adding the plan's own retained-fabric M3 2,600 and M10 1,200: {no_split_table - 3800}")
f5_rows = basis["AECP, including microcode, descriptor and D3 stores"] + basis["Notification"] + basis["Originator"] \
    + basis["NVM port and arbiter"] + basis["Wrapper NVM backend"]
f5_gross = gross - f5_rows
for label, alloc, lanes_sum, m3m10 in (("central", 1000, 4600, 3800), ("conservative", 3500, 2900, 2400)):
    credit = f5_gross - 3102 - alloc
    print(f"NOTE illustrative F5-unqualified flip ({label}; AECP, notification, originator and fabric NVM path kept;"
          f" M3+M10 active): split credit {credit}, image {r['LUT'] - credit - lanes_sum - m3m10}")
print(f"RESULT {'PASS' if fails == 0 else 'FAIL'}: {fails} failing check(s)")
sys.exit(1 if fails else 0)
