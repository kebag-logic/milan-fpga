#!/usr/bin/env python3
"""Re-derive the #234 findings-page tables from the published gate records.

Usage: check_tables.py <repo checkout> <evidence dir holding the *-record-*.json files>
Prints one line per checked cell group and a final tally; exit 1 on any mismatch.
"""
import json
import re
import sys
from pathlib import Path

repo, ev = Path(sys.argv[1]), Path(sys.argv[2])
doc = (repo / "docs/findings/234_PP_SHADOW_AREA_BASELINE.md").read_text()
base = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())
rec = {f"{c}-{e}": json.loads((ev / f"{c}-record-{e}.json").read_text())
       for c in "AB" for e in ("route-1x1", "ooc-1x1", "ooc-8x8")}
bad = 0
checked = 0


def num(text):
    return float(text.replace(",", "").replace("+", "")) if "." in text else int(text.replace(",", "").replace("+", ""))


def expect(label, got, want):
    global bad, checked
    checked += 1
    ok = got == want
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {label}: doc {got} record {want}")


# Baseline JSON equals the published A records.
for e in ("route-1x1", "ooc-1x1", "ooc-8x8"):
    expect(f"baseline.json {e} record == A-record-{e}.json", True, base["endpoints"][e]["record"] == rec[f"A-{e}"])

# Shipping route table.
for comb in "AB":
    m = re.search(rf"^\| {comb} \| ([^\n]+)\|$", doc.split("## Shipping route")[1], re.M)
    cells = [c.strip() for c in m.group(1).split("|")]
    f = rec[f"{comb}-route-1x1"]["figures"]
    keys = ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "BRAM_TILE", "DSP", "CARRY4", "WNS_ns", "WHS_ns")
    expect(f"route {comb} figures", [num(c) for c in cells], [f[k] for k in keys])

# Routed hierarchy: wrapper row.
m = re.search(r"^\| `milan_datapath/pp_shadow` \| ([\d,]+) / ([\d,]+) \| ([\d,]+) / ([\d,]+) \| (\d+) / (\d+) \| (\d+) \|$", doc, re.M)
wa, wb = rec["A-route-1x1"]["scopes"]["wrapper"], rec["B-route-1x1"]["scopes"]["wrapper"]
expect("routed pp_shadow row", [num(x) for x in m.groups()],
       [wa["LUT"], wb["LUT"], wa["FF"], wb["FF"], wa["RAMB36"], wa["RAMB18"], wa["DSP"]])

# Standalone table.
sect = doc.split("## Standalone synthesis")[1].split("## Processor sub-blocks")[0]
for shape, ep in (("1x1", "ooc-1x1"), ("8x8", "ooc-8x8")):
    for comb in "AB":
        m = re.search(rf"^\| {shape}, {comb} \| ([^\n]+)\|$", sect, re.M)
        cells = [c.strip() for c in m.group(1).split("|")]
        f = rec[f"{comb}-{ep}"]["figures"]
        keys = ("LUT", "FF", "RAMB36", "RAMB18", "BRAM_TILE", "DSP", "CARRY4", "WNS_ns")
        expect(f"standalone {shape} {comb}", [num(c) for c in cells], [f[k] for k in keys])

# Sub-block tables.
sub = doc.split("## Processor sub-blocks")[1].split("## Storage mapping")[0]
parts = sub.split("**8x8 shape, A / B**")
for shape, ep, text in (("1x1", "ooc-1x1", parts[0]), ("8x8", "ooc-8x8", parts[1].split("From 1x1 to 8x8")[0])):
    for line in text.splitlines():
        if not line.startswith("| ") or line.startswith("| Sub-block") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        insts = re.findall(r"`([^`]+)`", cells[1])
        vals = [tuple(num(x) for x in c.split(" / ")) for c in cells[2:]]
        want = []
        for comb in "AB":
            scopes = rec[f"{comb}-{ep}"]["scopes"]
            names = []
            for inst in insts:
                if "[*]" in inst:
                    pat = re.escape(inst).replace(r"\[\*\]", r"\[\d+\]")
                    names += [k for k in scopes if re.fullmatch(pat, k)]
                else:
                    names.append(inst)
            want.append([sum(scopes[n][k] for n in names) for k in ("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4")])
        expect(f"sub-block {shape} {cells[0]}", vals, list(zip(*want)))

# Per-context table (1x1 -> 8x8, A).
ctx = sub.split("From 1x1 to 8x8")[1]
for line in ctx.splitlines():
    m = re.match(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|$", line)
    if not m:
        continue
    s1, s8 = rec["A-ooc-1x1"]["scopes"][m.group(1)], rec["A-ooc-8x8"]["scopes"][m.group(1)]
    want = [s1["LUT"], s8["LUT"], round((s8["LUT"] - s1["LUT"]) / 7), s1["FF"], s8["FF"], round((s8["FF"] - s1["FF"]) / 7)]
    expect(f"per-context {m.group(1)}", [num(x) for x in m.groups()[1:]], want)

print(f"checked {checked} groups, {bad} mismatches")
sys.exit(1 if bad else 0)
