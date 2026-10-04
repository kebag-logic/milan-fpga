#!/usr/bin/env python3
"""R466-2 probe: tie the published CPU, cache and L2 variant receipts together.
For every priced variant: the published synth_hierarchy.rpt hashes to the receipt's report_sha256,
its top row and its CPU row parse (with the repository's own report parser) to the receipt's total
and cpu figures, meta.json equals the receipt's meta, the export used the pricing copy and the
receipt's argv differs from the shipping argv only in the variant's flags; then an independent
least-squares fit of the three numeric axes, and the stated differences.
Usage: check_soc_variants.py <repo> <round-2 author inputs dir>"""
import hashlib, json, sys
from pathlib import Path
import numpy as np
repo, inputs = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "syn/ooc"))
from pp_baseline_rank import hierarchy
prices = json.loads((inputs / "soc_prices.json").read_text())
bad = 0
ship_argv = prices["ship"]["export"]["argv"]


def argv_delta(argv):
    def pairs(a):
        out, i = {}, 0
        while i < len(a):
            if a[i].startswith("--") and i + 1 < len(a) and not a[i + 1].startswith("--"):
                out[a[i]] = a[i + 1]; i += 2
            else:
                out[a[i]] = True; i += 1
        return out
    s, v = pairs(ship_argv), pairs(argv)
    return {k: v.get(k) for k in set(s) | set(v) if s.get(k) != v.get(k) and k != "--output-dir"}


for name, entry in sorted(prices.items()):
    exp = entry["export"]
    if "synth" not in entry:
        print(f"{name:14s} not priced: export rc {exp.get('rc')}, recipe {exp.get('recipe')}, flags {argv_delta(exp['argv'])}")
        continue
    d = inputs / "soc-variants" / name
    rpt = d / "synth_hierarchy.rpt"
    digest = hashlib.sha256(rpt.read_bytes()).hexdigest()
    rows = hierarchy(rpt)
    top = rows["alinx_ax7101"]
    cpu = rows[entry["synth"]["cpu_row"]]
    ok_digest = digest == entry["synth"]["report_sha256"]
    ok_total = all(top[c] == v for c, v in entry["synth"]["total"].items())
    ok_cpu = all(cpu[c] == v for c, v in entry["synth"]["cpu"].items())
    meta = json.loads((d / "meta.json").read_text())
    ok_meta = meta == entry.get("meta")
    ok_recipe = exp.get("recipe") == "milan_soc_pricing.py"
    ok_rom = meta["read_rom_sha256"] == prices["ship"]["meta"]["read_rom_sha256"]
    ok = ok_digest and ok_total and ok_cpu and ok_meta and ok_recipe and ok_rom and entry["vivado"]["rc"] == 0
    bad += not ok
    print(f"{name:14s} report {'=' if ok_digest else '!='} receipt, total {'=' if ok_total else '!='}, cpu "
          f"{'=' if ok_cpu else '!='}, meta {'=' if ok_meta else '!='}, recipe {exp.get('recipe')}, shipping ROM read "
          f"{ok_rom}, vivado rc {entry['vivado']['rc']}; flags vs ship {argv_delta(exp['argv'])}")
st = prices["ship-tracked"]["export"]
print(f"ship-tracked: recipe {st.get('recipe')}, rc {st.get('rc')}, cpu netlist {st.get('cpu_netlist')} vs ship "
      f"{prices['ship']['export'].get('cpu_netlist')}; flags vs ship {argv_delta(st['argv'])}")


def tiles(c):
    return c["RAMB36"] + c["RAMB18"] / 2


def fit(xs, ys):
    A = np.column_stack([np.ones(len(xs)), xs]); c, *_ = np.linalg.lstsq(A, np.array(ys, float), rcond=None)
    r = np.array(ys, float) - A @ c
    return c[1], float(np.sqrt(np.mean(r ** 2))), float(np.max(np.abs(r)))


for label, names, xs in (("CPU count", ("ship", "cpu2", "cpu4"), (1, 2, 4)),
                         ("L1 ways", ("l1-caches", "l1-w2", "l1-w4"), (1, 2, 4)),
                         ("L2 KiB on L1 core", ("l1l2-8k", "l1l2-16k", "l1l2-32k"), (8, 16, 32))):
    t = [prices[n]["synth"]["total"] for n in names]
    lut = fit(xs, [x["LUT"] for x in t]); ff = fit(xs, [x["FF"] for x in t]); br = fit(xs, [tiles(x) for x in t])
    print(f"fit {label}: LUT/unit {lut[0]:.1f} rms {lut[1]:.1f} max {lut[2]:.1f}; FF/unit {ff[0]:.1f}; BRAM tiles/unit {br[0]:.2f}")
T = {n: e["synth"]["total"] for n, e in prices.items() if "synth" in e}
for a, b in (("isa-m", "ship"), ("isa-mf", "isa-m"), ("isa-mfd", "isa-mf"), ("rv64", "ship"), ("naxriscv", "ship"),
             ("naxriscv-rv64", "naxriscv"), ("l1-fetch", "ship"), ("l1-caches", "ship"), ("l1l2-8k", "l1-caches"),
             ("l1l2-16k", "l1-caches"), ("l1l2-32k", "l1-caches"), ("rv64-fpu", "rv64"), ("l2-8k", "ship"),
             ("l2-16k", "ship"), ("l2-32k", "ship")):
    print(f"{a} - {b}: LUT {T[a]['LUT'] - T[b]['LUT']:+d} FF {T[a]['FF'] - T[b]['FF']:+d} "
          f"BRAM {tiles(T[a]) - tiles(T[b]):+.1f} DSP {T[a]['DSP'] - T[b]['DSP']:+d}")
s = T["ship"]["LUT"]; c = prices["ship"]["synth"]["cpu"]["LUT"]
print(f"ship synth over route: SoC {s}/{4847 + 3524} = {s / (4847 + 3524):.3f}; CPU {c}/3524 = {c / 3524:.3f}")
print("RESULT", "PASS" if not bad else f"FAIL {bad}")
sys.exit(1 if bad else 0)
