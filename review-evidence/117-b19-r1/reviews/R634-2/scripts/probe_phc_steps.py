#!/usr/bin/env python3
"""DUT PHC against the tap clock per box 3 cycle, consecutive Pdelay responses in
tap order: rate (ppm) between neighbours under 3.5 s apart, and every
offset step over 1 ms with its size and tap time.  Usage: probe_phc_steps.py RAW_ROOT"""
import sys
from pathlib import Path
src = open(Path(__file__).with_name("probe_box3.py")).read()
ns = {}
exec(src.split("root = Path(sys.argv[1])")[0], ns)
root = Path(sys.argv[1])
for i in range(1, 7):
    R = list(ns["recs"](root / f"cycle{i:02d}" / "tap.pcap"))
    resp = {r["seq"]: r["tap"] for r in R if r["port"] == 3 and r["mt"] == 0x3}
    pr = sorted((resp[r["seq"]], r["ts"] + r["corr"]) for r in R if r["port"] == 3 and r["mt"] == 0xA and r["seq"] in resp and 0 <= r["tap"] - resp[r["seq"]] < 1e8)
    rates, steps = [], []
    t0 = pr[0][0]
    for (ta, pa), (tb, pb) in zip(pr, pr[1:]):
        dt = tb - ta
        jump = (pb - pa) - dt
        if dt < 3.5e9 and abs(jump) < 1e6:
            rates.append(jump / dt * 1e6)
        else:
            steps.append((round((ta - t0) / 1e9, 2), round(dt / 1e9, 2), round(jump / 1e9, 4)))
    print(f"cycle{i}: pairs {len(pr)}, rate ppm {min(rates):.3f}..{max(rates):.3f} over {len(rates)} neighbours; "
          f"gaps/steps (tap s from first pair, dt s, PHC minus tap s): {steps}")
