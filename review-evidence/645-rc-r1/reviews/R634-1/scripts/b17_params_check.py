#!/usr/bin/env python3
"""Independent re-derivation of follow_ring's kB17 table from B17's cNN.json.

Usage: python3 -I b17_params_check.py <645-b17-r1/author/summary dir> <sim_main.cpp>
Burst rule (B17 round 3): PDUs more than 20 us late, grouped while < 1 ms apart.
"""
import json, re, sys, glob, statistics
sdir, src = sys.argv[1], sys.argv[2]
txt = open(src).read()
rows = re.findall(r"\{(\d+), ([\d.]+), ([\d.]+), ([\d.]+), ([\d.]+)\}", txt.split("kB17 = {{")[1].split("}};")[0])
table = {int(r[0]): tuple(float(x) for x in r[1:]) for r in rows}
bad = 0
slopes = []
for f in sorted(glob.glob(sdir + "/c[0-9][0-9].json")):
    d = json.load(open(f))
    n = int(d["cycle"][1:])
    pr = d["tap"]["priming"]
    first_ms = pr["first_pdu_after_command_ms"]
    first_s = d["tap"]["streams"]["peer-aaf"]["first_s"]
    late = [p for p in d["tap"]["late_pdus"] if p["late_us"] > 20.0]
    bursts = []
    for p in late:
        if bursts and p["s"] - bursts[-1][-1]["s"] < 0.001:
            bursts[-1].append(p)
        else:
            bursts.append([p])
    b0 = bursts[0]
    peak0 = max(p["late_us"] for p in b0)
    t0 = b0[0]["s"] - first_s
    later = max(max(p["late_us"] for p in b) for b in bursts[1:])
    allpre = [p["late_us"] for p in d["tap"]["late_pdus"] if p["s"] < b0[0]["s"]]
    sl = d["poll"]["slips"][0]
    want = (first_ms, round(t0, 4), peak0, later)
    got = table[n]
    ok = all(abs(a - b) < 6e-4 for a, b in zip(want, got))
    bad += not ok
    print(f"c{n:02d} derived first_pdu_ms={first_ms} burst_s={t0:.4f} burst_us={peak0} later_us={later} "
          f"| table {got} {'MATCH' if ok else 'MISMATCH'} | max late before first burst "
          f"{max(allpre) if allpre else 'none-listed'} | slip {sl['s_lo']}..{sl['s_hi']} s, first burst at "
          f"{b0[0]['s']:.4f} s from bind, n={len(b0)}")
print("RESULT", "PASS" if bad == 0 and len(table) == 10 else f"FAIL {bad}")
