#!/usr/bin/env python3
"""Re-derive route figures from raw Vivado report receipts (no trust in route-figures.json).

Usage: python3 -I rederive_routes.py <receipts_dir>
Prints one line per (side, directive) and compares against route-figures.json.
"""
import json, re, sys, pathlib

R = pathlib.Path(sys.argv[1])
TAG = {"aslh": "AltSpreadLogic_high", "eppo": "ExtraPostPlacementOpt", "eto": "ExtraTimingOpt"}
ref = json.loads((R / "route-figures.json").read_text())
bad = 0
for side in ("dev", "head"):
    for t, name in TAG.items():
        d = R / f"route-{side}"
        tt = (d / f"{t}-timing-design-tables.txt").read_text().split("== ")
        corners = {}
        for blk in tt:
            m = re.match(r"alinx_ax7101_signoff_(Slow_0C|Slow_85C|Fast_0C|Fast_85C)_timing\.rpt", blk)
            if not m:
                continue
            nums = re.search(r"-{5,}.*\n\s+(\S+)\s+\S+\s+\S+\s+\S+\s+(\S+)", blk)
            corners[m.group(1)] = [float(nums.group(1)), float(nums.group(2))]
        u = (d / f"{t}-baseline_utilization.rpt").read_text()
        def g(pat):
            return float(re.search(pat, u, re.M).group(1))
        fig = dict(LUT=int(g(r"^\| Slice LUTs\s+\|\s+(\d+)")), FF=int(g(r"^\| Slice Registers\s+\|\s+(\d+)")),
                   SLICE=int(g(r"^\| Slice\s+\|\s+(\d+)")), RAMB36=int(g(r"^\|\s+RAMB36/FIFO\*\s+\|\s+(\d+)")),
                   RAMB18=int(g(r"^\|\s+RAMB18\s+\|\s+(\d+)")), DSP=int(g(r"^\| DSPs\s+\|\s+(\d+)")))
        rs = (d / f"{t}-route_status.rpt").read_text()
        rerr = int(re.search(r"routing errors\.+\s*:\s*(\d+)", rs).group(1))
        rc = (d / f"{t}-baseline.log.rc").read_text().split()[0]
        wns = min(v[0] for v in corners.values()); whs = min(v[1] for v in corners.values())
        r = ref[side][name]
        ok = all(fig[k] == r[k] for k in fig) and corners == r["corners"] and rerr == r["routing_errors"]
        floor = wns >= 0.030 and whs >= 0.0
        bad += (not ok) + (not floor)
        print(f"{side:4} {name:22} LUT={fig['LUT']} FF={fig['FF']} SLICE={fig['SLICE']} free={15850-fig['SLICE']} "
              f"RAMB={fig['RAMB36']}/{fig['RAMB18']} DSP={fig['DSP']} WNS={wns:+.3f} WHS={whs:+.3f} "
              f"slow={corners['Slow_0C']} fast={corners['Fast_0C']} rerr={rerr} rc={rc} "
              f"match_json={ok} floors_met={floor}")
print("RESULT", "PASS" if bad == 0 else f"FAIL({bad})")
sys.exit(1 if bad else 0)
