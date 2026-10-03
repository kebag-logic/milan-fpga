#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer reconciliation: baseline JSON <-> published records <-> doc tables.

Usage: reconcile.py <checkout> <evidence-dir>
  <evidence-dir> = review-evidence/234-r1/author/evidence of the public
  evidence commit 43ad8362.
Prints one line per check; exit 0 when every check holds.
"""

import json
from pathlib import Path
import re
import sys

REPO, EV = Path(sys.argv[1]), Path(sys.argv[2])
BASE = json.loads((REPO / "syn/ooc/pp_resource_baseline.json").read_text())
FIND = (REPO / "docs/findings/234_PP_SHADOW_AREA_BASELINE.md").read_text()
BUDGET = (REPO / "docs/design/AREA_BUDGET.md").read_text()
REC = {(c, e): json.loads((EV / f"{c}-record-{e}.json").read_text())
       for c in "AB" for e in ("route-1x1", "ooc-1x1", "ooc-8x8")}
REC[("A", "ooc-1x1-10ns")] = json.loads((EV / "A-record-ooc-1x1-10ns.json").read_text())
bad = 0


def check(label, ok, detail=""):
    global bad
    bad += 0 if ok else 1
    print(f"{'OK ' if ok else 'BAD'} {label}{(' -- ' + detail) if detail else ''}")


def num(text):
    return float(text.replace(",", "").replace("+", ""))


# 1. The recorded baseline is exactly A's published records (not B, not hand-typed).
for endpoint in ("route-1x1", "ooc-1x1", "ooc-8x8"):
    check(f"baseline {endpoint} record == published A-record-{endpoint}.json",
          BASE["endpoints"][endpoint]["record"] == REC[("A", endpoint)])
    check(f"baseline {endpoint} record != B record", BASE["endpoints"][endpoint]["record"] != REC[("B", endpoint)])
check("10 ns control differs from 20 ns record only in clock identity and figures/scopes",
      REC[("A", "ooc-1x1-10ns")]["identity"]["standalone_clock_ns"] == ["10.000"]
      and REC[("A", "ooc-1x1")]["identity"]["standalone_clock_ns"] == ["20.000"])
print("INFO 10 ns control inputs digest differs from the 20 ns run, as expected (clock.xdc is a read input): "
      f"{REC[('A','ooc-1x1-10ns')]['inputs_sha256'][:12]} vs {REC[('A','ooc-1x1')]['inputs_sha256'][:12]}")

# 2. Headline tables in the findings page and AREA_BUDGET equal the records.
F = {k: v["figures"] for k, v in REC.items()}


def row_of(text, prefix):
    hits = [line for line in text.splitlines() if line.startswith(prefix)]
    return [c.strip() for c in hits[0].strip("|").split("|")] if len(hits) == 1 else None


for comb in "AB":
    cells = row_of(FIND.split("\n## Shipping route\n")[1].split("\n## Standalone")[0], f"| {comb} | ")
    want = F[(comb, "route-1x1")]
    got = dict(zip(["LUT", "FF", "SLICE", "RAMB36", "RAMB18", "BRAM_TILE", "DSP", "CARRY4", "WNS_ns", "WHS_ns"],
                   map(num, cells[1:])))
    check(f"findings shipping-route row {comb} == record", all(abs(got[k] - want[k]) < 1e-9 for k in got),
          str({k: (got[k], want[k]) for k in got if abs(got[k] - want[k]) > 1e-9}))
for comb, shape in (("A", "1x1"), ("B", "1x1"), ("A", "8x8"), ("B", "8x8")):
    cells = row_of(FIND.split("\n## Standalone synthesis\n")[1].split("\n## Processor")[0], f"| {shape}, {comb} | ")
    want = F[(comb, f"ooc-{shape}")]
    got = dict(zip(["LUT", "FF", "RAMB36", "RAMB18", "BRAM_TILE", "DSP", "CARRY4", "WNS_ns"], map(num, cells[1:])))
    check(f"findings standalone row {shape},{comb} == record", all(abs(got[k] - want[k]) < 1e-9 for k in got),
          str({k: (got[k], want[k]) for k in got if abs(got[k] - want[k]) > 1e-9}))
c10 = F[("A", "ooc-1x1-10ns")]
check("10 ns control sentence figures == record",
      "It measures {:,} LUTs, {:,} FFs, {} RAMB36, {} RAMB18, {} DSPs and {:,} CARRY4.".format(
          c10["LUT"], c10["FF"], c10["RAMB36"], c10["RAMB18"], c10["DSP"], c10["CARRY4"]) in FIND)

# 3. Per-sub-block tables equal the record scopes (instances grouped as the table states).
for shape in ("1x1", "8x8"):
    section = FIND.split(f"**{shape} shipping shape, A / B**" if shape == "1x1" else "**8x8 shape, A / B**")[1]
    section = section.split("\n\n")[1]
    for line in section.splitlines()[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        names = re.findall(r"`([^`]+)`", cells[1])
        for col, field in zip(range(2, 8), ("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4")):
            a, b = (num(x) for x in cells[col].split(" / "))
            for comb, value in (("A", a), ("B", b)):
                scopes = REC[(comb, f"ooc-{shape}")]["scopes"]
                total = 0
                for name in names:
                    if "[*]" in name:
                        pat = re.escape(name).replace(r"\[\*\]", r"\[\d+\]")
                        keys = [k for k in scopes if re.fullmatch(pat, k)]
                    else:
                        keys = [name] if name in scopes else []
                    total += sum(scopes[k][field] for k in keys)
                if total != value:
                    check(f"sub-block {shape} {cells[0]} {field} {comb}", False, f"doc {value} record {total}")
    check(f"sub-block table {shape}: every cell re-derived from record scopes (mismatches listed above)", True)

# 4. Derived sentences.
s = {c: REC[(c, "ooc-1x1")]["scopes"] for c in "AB"}
leaf = [k for k in s["A"] if k.count("/") == 1 or (k.count("/") == 0 and k != "wrapper")]
untouched = [k for k in s["A"] if k.startswith("u_pp/") and k.count("/") == 1 and k != "u_pp/u_nvm_port"]
untouched += [k for k in ("u_nvm", "ctl_fifo") if k in s["A"]]
net_lut = sum(s["B"].get(k, {}).get("LUT", 0) - s["A"][k]["LUT"] for k in untouched)
net_ff = sum(s["B"].get(k, {}).get("FF", 0) - s["A"][k]["FF"] for k in untouched)
abs_lut = sum(abs(s["B"].get(k, {}).get("LUT", 0) - s["A"][k]["LUT"]) for k in untouched)
print(f"INFO 1x1 B-A over depth-1 u_pp children except u_nvm_port, plus u_nvm and ctl_fifo: "
      f"net LUT {net_lut:+d}, net FF {net_ff:+d}, abs LUT {abs_lut}")
print(f"INFO wrapper B-A {s['B']['wrapper']['LUT'] - s['A']['wrapper']['LUT']:+d} LUT, "
      f"u_pp B-A {s['B']['u_pp']['LUT'] - s['A']['u_pp']['LUT']:+d} LUT, "
      f"u_pp own (u_pp minus children) B-A "
      f"{(s['B']['u_pp']['LUT'] - sum(s['B'][k]['LUT'] for k in s['B'] if k.startswith('u_pp/') and k.count('/') == 1)) - (s['A']['u_pp']['LUT'] - sum(s['A'][k]['LUT'] for k in s['A'] if k.startswith('u_pp/') and k.count('/') == 1)):+d}")
# The partition that reproduces the findings page: u_pp's direct children except
# u_nvm_port (the changed block) AND u_nvm_arb (excluded without being stated).
part = [k for k in s["A"] if k.startswith("u_pp/") and k.count("/") == 1
        and k not in ("u_pp/u_nvm_port", "u_pp/u_nvm_arb")]
p_lut = sum(s["B"][k]["LUT"] - s["A"][k]["LUT"] for k in part)
p_ff = sum(s["B"][k]["FF"] - s["A"][k]["FF"] for k in part)
p_abs = sum(abs(s["B"][k]["LUT"] - s["A"][k]["LUT"]) for k in part)
print(f"INFO partition u_pp direct children minus u_nvm_port and u_nvm_arb: net LUT {p_lut:+d}, "
      f"net FF {p_ff:+d}, abs LUT {p_abs}")
print(f"INFO whole wrapper minus u_nvm_port: LUT {s['B']['wrapper']['LUT'] - s['A']['wrapper']['LUT'] - 83:+d}, "
      f"FF {s['B']['wrapper']['FF'] - s['A']['wrapper']['FF'] - 33:+d}")
check("findings :135-136 'net 101 LUTs', 'sum to 309' reproduce on that partition",
      "net 101 LUTs" in FIND and "sum to 309 LUTs" in FIND and p_lut == 101 and p_abs == 309,
      f"recomputed {p_lut:+d} / {p_abs}")
check("AREA_BUDGET 'net 101 LUTs and 95 FFs': FF on the same partition",
      "net 101 LUTs and 95 FFs" in BUDGET and p_ff == 95,
      f"same partition gives FF {p_ff:+d}; +95 is only reached by adding the processor top's own +107 FF")
r = {c: REC[(c, "route-1x1")]["scopes"] for c in "AB"}
check("route wrapper +259 LUT (B-A pp_shadow scope)", r["B"]["wrapper"]["LUT"] - r["A"]["wrapper"]["LUT"] == 259)
check("route pp_shadow A LUT 23,937 / FF 24,263", r["A"]["wrapper"]["LUT"] == 23937 and r["A"]["wrapper"]["FF"] == 24263)
check("route pp_shadow B LUT 24,196 / FF 24,274", r["B"]["wrapper"]["LUT"] == 24196 and r["B"]["wrapper"]["FF"] == 24274)
check("625 - 259 = 366 outside the wrapper", F[("B", "route-1x1")]["LUT"] - F[("A", "route-1x1")]["LUT"] - 259 == 366)
dev = {"LUT": 63400, "FF": 126800, "SLICE": 15850, "RAMB36": 135, "RAMB18": 270, "BRAM_TILE": 135, "DSP": 240}
for k, pct in (("LUT", "79.07"), ("FF", "46.53"), ("SLICE", "99.78"), ("RAMB36", "58.52"), ("RAMB18", "10.00"),
               ("BRAM_TILE", "68.52"), ("DSP", "5.83")):
    check(f"percent {k} {pct}", f"{100 * F[('A', 'route-1x1')][k] / dev[k]:.2f}" == pct)
check("NFR-RES-01 gap 12,088", F[("A", "route-1x1")]["LUT"] - int(0.6 * 63400) == 12088)
check("wrapper target 11,849 = routed pp_shadow 23,937 - 12,088", 23937 - 12088 == 11849)
check("ceiling 121.5 = 135 - 13.5 reserve", BASE["endpoints"]["route-1x1"]["ceiling"]["BRAM_TILE"] == 135 - 13.5)
for e, k in (("ooc-1x1", "LUT"), ("ooc-1x1", "FF"), ("ooc-8x8", "LUT"), ("ooc-8x8", "FF")):
    tol = BASE["endpoints"][e]["tolerance"][k]
    print(f"INFO {e} {k} tolerance {tol} = {100 * tol / F[('A', e)][k]:.2f} % of the record")
print(f"reconcile: {bad} mismatches")
sys.exit(1 if bad else 0)
