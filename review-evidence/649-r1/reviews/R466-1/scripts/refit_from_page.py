#!/usr/bin/env python3
"""R466 probe: refit the page's Vivado stream model, Yosys stream/channel model and
processor-parameter models from the page's own data tables with an independent
least-squares implementation, and recompute derived prose figures.
Usage: refit_from_page.py <repo>   (pp-ship LUT/FF totals are reviewer-reproduced)"""
import re, sys
import numpy as np
from pathlib import Path
page = (Path(sys.argv[1]) / "docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md").read_text()
def block(name):
    body = re.search(rf"<!-- table: {name} -->\n(.*?)<!-- end table", page, re.S).group(1)
    rows = [[c.strip() for c in l.strip("|").split("|")] for l in body.splitlines()[2:]]
    return rows
def n(x): return float(x.replace(",", "").replace("+", ""))
def fit(X, y):
    A = np.column_stack([np.ones(len(y))] + X)
    c, *_ = np.linalg.lstsq(A, y, rcond=None)
    r = y - A @ c
    return c, r, np.sqrt(np.mean(r**2)), np.max(np.abs(r))
v = block("vivado-opt-data")
N = np.array([n(r[1]) for r in v])
for i, m in ((2, "LUT"), (3, "FF"), (4, "BRAM")):
    c, r, rms, mx = fit([N], np.array([n(x[i]) for x in v]))
    print(f"vivado {m}: fixed {c[0]:.1f} per-stream {c[1]:.1f} rms {rms:.1f} max {mx:.1f} resid {np.round(r,0)}")
y = block("yosys-stream-data")
N = np.array([n(r[1]) for r in y]); C = np.array([n(r[2]) for r in y])
for i, m in ((3, "LUT"), (4, "FF")):
    c, r, rms, mx = fit([N, C, N*C], np.array([n(x[i]) for x in y]))
    print(f"yosys {m}: {np.round(c,1)} rms {rms:.1f} max {mx:.1f} resid {np.round(r,0)}")
# processor parameters from the marginals plus the reproduced pp-ship total
SHIP = 57386
pm = {r[0]: n(r[2]) for r in block("processor-marginals")}
groups = {"DESC_IDX_ENTRIES_P": ([16, 32, 64], [pm["pp-idx-16"], 0, pm["pp-idx-64"]]),
          "PP_N_CTRL_C": ([4, 8, 12, 16], [pm["pp-ctrl-4"], pm["pp-ctrl-8"], pm["pp-ctrl-12"], 0]),
          "RX_SLOTS_P": ([2, 4, 8], [pm["pp-rxslots-2"], 0, pm["pp-rxslots-8"]]),
          "streams": ([1, 2, 4, 8], [0, pm["pp-si3"], pm["pp-si5"], pm["pp-si9"]]),
          "TX_STD_SLOTS_P": ([2, 4, 8], [pm["pp-txslots-2"], 0, pm["pp-txslots-8"]])}
for k, (x, d) in groups.items():
    c, r, rms, mx = fit([np.array(x, float)], np.array(d) + SHIP)
    print(f"processor {k}: per unit {c[1]:.2f} rms {rms:.1f} max {mx:.1f} resid signs {''.join('+' if v > 0 else '-' for v in r)}")
cal = {(r[0], r[1]): r for r in block("calibration-totals")}
for a in ("ship", "streams-2", "streams-4", "ship-8x8"):
    hl = n(cal[(a, "LUT")][2]); ol = n(cal[(a, "LUT")][5]); sl = n(cal[(a, "LUT")][4])
    print(f"{a}: opt/hier {ol/hl:.3f} hier/opt {hl/ol:.2f} synth->opt LUT removed {100*(sl-ol)/sl:.2f}%")
print("route/OOC datapath", round(42200/43622, 4), "gap", 50767 - 38040, "gap share of prunes", round((512+674+35)/12727, 3))
print("one more stream slices", 4739/4, "fit-based", 3828/4)
