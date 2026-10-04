#!/usr/bin/env python3
"""Independent check of the CPU, cache and L2 variant prices (round 2).

Usage: check_soc_variants.py <inputs dir of review-evidence/649-r2/author> <head milan_soc.py> <page.md>

Without the lane's scripts: reads each variant's published synth_hierarchy.rpt, takes the
top row and the CPU core's row (meta.json's cpu_module), compares them with soc_prices.json,
recomputes every change from `ship`, the three per-unit least-squares slopes with their LUT,
FF and BRAM residuals, checks the page's soc-variant-prices rows, checks every non-ship row
carries the profile label, and checks that pricing-copy.diff removes exactly the head
recipe's two profile refusals.
"""
import json, re, sys
from pathlib import Path

inp = Path(sys.argv[1]); soc = Path(sys.argv[2]).read_text(); page = Path(sys.argv[3]).read_text()
page = re.search(r"<!-- table: soc-variant-prices -->\n(.*?)<!-- end table", page, re.S).group(1)
prices = json.loads((inp / "soc_prices.json").read_text())
COLS = ("LUT", "logic_LUT", "LUTRAM", "SRL", "FF", "RAMB36", "RAMB18", "DSP")
fails = []


def rows_of(rpt):
    out = {}
    for line in rpt.read_text().splitlines():
        c = line.split("|")
        if len(c) == 12 and c[3].strip().isdigit():
            out.setdefault(c[1].strip(), dict(zip(COLS, (int(x) for x in c[3:11]))))
            out.setdefault("module:" + c[2].strip(), dict(zip(COLS, (int(x) for x in c[3:11]))))
    return out


measures = lambda r: {"LUT": r["LUT"], "FF": r["FF"], "BRAM": r["RAMB36"] + r["RAMB18"] / 2, "DSP": r["DSP"]}
got = {}
for name, entry in prices.items():
    d = inp / "soc-variants" / name
    if "synth" not in entry:
        print(f"{name}: not priced ({entry.get('parameter')} {entry.get('value')}): export rc {entry['export'].get('rc')}")
        continue
    rows = rows_of(d / "synth_hierarchy.rpt")
    meta = json.loads((d / "meta.json").read_text())
    top = next(iter(rows.values()))
    cpu = rows.get("module:" + meta["cpu_module"]) or rows.get(meta["cpu_module"])
    sub = {k: v for k, v in entry["synth"]["total"].items() if k in COLS}
    if sub != {k: top[k] for k in sub}:
        fails.append(f"{name}: report top {top} != receipt {sub}")
    if cpu is None or {k: cpu[k] for k in COLS} != {k: entry["synth"]["cpu"][k] for k in COLS}:
        fails.append(f"{name}: cpu row {cpu} != receipt {entry['synth']['cpu']}")
    got[name] = (measures(top), measures(cpu))
ship = got["ship"][0]
print(f"{'variant':15s} {'SoC LUT':>8s} {'dLUT':>7s} {'dFF':>7s} {'dBRAM':>6s} {'dDSP':>4s}  page row ok")
for name, (tot, cpu) in got.items():
    d = {m: tot[m] - ship[m] for m in tot}
    row = re.search(rf"^\| {re.escape(name)} \| .*$", page, re.M)
    cells = [x.strip() for x in row.group(0).split("|")[1:-1]] if row else []
    n = lambda s: float(s.replace(",", "").replace("+", ""))
    ok = bool(cells) and n(cells[4]) == tot["LUT"] and n(cells[5]) == tot["FF"] and n(cells[6]) == tot["BRAM"] \
        and n(cells[8]) == d["LUT"] and n(cells[9]) == d["FF"] and n(cells[10]) == d["BRAM"] and n(cells[11]) == d["DSP"] \
        and n(cells[12]) == cpu["LUT"] and n(cells[13]) == cpu["FF"]
    label_ok = bool(cells) and (cells[3] == "ships" if name == "ship" else cells[3] == "not buildable under the shipping software profile")
    if not ok or not label_ok:
        fails.append(f"page row {name}: {cells}")
    print(f"{name:15s} {tot['LUT']:8.0f} {d['LUT']:+7.0f} {d['FF']:+7.0f} {d['BRAM']:+6.1f} {d['DSP']:+4.0f}  {ok and label_ok}")


def lsq(xs, ys):
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    res = [y - (a + b * x) for x, y in zip(xs, ys)]
    return b, res


for label, names, xs in (("CPU count", ("ship", "cpu2", "cpu4"), (1, 2, 4)),
                         ("L1 ways", ("l1-caches", "l1-w2", "l1-w4"), (1, 2, 4)),
                         ("L2 KiB on L1 core", ("l1l2-8k", "l1l2-16k", "l1l2-32k"), (8, 16, 32))):
    for m in ("LUT", "FF", "BRAM"):
        b, res = lsq(xs, [got[n][0][m] for n in names])
        print(f"fit {label:18s} {m:4s} slope {b:9.3f} residuals {[round(r, 2) for r in res]}")
    steps = [got[names[i + 1]][0]["BRAM"] - got[names[i]][0]["BRAM"] for i in range(2)]
    print(f"    {label} BRAM steps between the three points: {steps}")
# pricing copy: exactly the two refusals
diff = (inp / "soc-variants" / "pricing-copy.diff").read_text().splitlines()
minus = [l[1:] for l in diff if l.startswith("-") and not l.startswith("---")]
plus = [l[1:] for l in diff if l.startswith("+") and not l.startswith("+++")]
block = "\n".join(minus)
print(f"pricing-copy.diff: {len(minus)} removed lines, {len(plus)} added lines; removed block present verbatim in head milan_soc.py: {block in soc}")
if block not in soc or len([l for l in minus if "ap.error" in l]) != 2 or any(p.strip() != "pass  # pricing copy (#649 round 2): the profile refusal is removed" for p in plus):
    fails.append("pricing copy is not exactly the two refusals removed")
print("FAILURES" if fails else "ALL CHECKS PASS", fails[:10])
sys.exit(1 if fails else 0)
