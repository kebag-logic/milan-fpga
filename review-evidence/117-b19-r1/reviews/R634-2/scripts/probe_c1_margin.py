#!/usr/bin/env python3
"""Cycle 1 grandmaster-loss lower margin, unrounded, on the tap clock.
Usage: probe_c1_margin.py RAW_ROOT CYCLE   (prints ns-level inputs)"""
import json, re, sys
from pathlib import Path
root, cyc = Path(sys.argv[1]), sys.argv[2]
src = open(Path(__file__).with_name("probe_box3.py")).read()
ns = {}
exec(src.split("root = Path(sys.argv[1])")[0], ns)
R = list(ns["recs"](root / cyc / "tap.pcap"))
resp = {r["seq"]: r["tap"] for r in R if r["port"] == 3 and r["mt"] == 0x3}
pairs = sorted((r["ts"] + r["corr"], resp[r["seq"]]) for r in R if r["port"] == 3 and r["mt"] == 0xA and r["seq"] in resp and 0 <= r["tap"] - resp[r["seq"]] < 1e8)
S = []
for l in open(root / cyc / "console.jsonl"):
    if not l.strip(): continue
    r = json.loads(l)
    if r["cmd"] != "milan_status": continue
    kv = dict(re.findall(r"(\w+)=([0-9A-Za-z]+)", r["raw"]))
    if "TAI_NS" not in kv: continue
    phc = int(kv["TAI_NS"], 16)
    best = min(pairs, key=lambda p: abs(p[0] - phc))
    S.append(dict(gm=kv["GPTP_GM"], phc=phc, pair_dphc=(phc - best[0]) / 1e9, tap=best[1] + phc - best[0]))
k = next(k for k in range(1, len(S)) if S[k]["gm"] == "020000fffe000001" and S[k - 1]["gm"] == "3cc0c6fffefe0210")
a = S[k - 1]
ann = [r["tap"] for r in R if r["port"] == 2 and r["mt"] == 0xB and r["gm"] == "3cc0c6fffefe0210" and r["tap"] < a["tap"]]
c = max(ann) + 3e9
u_rate = abs(a["pair_dphc"]) * 8.361e-6 * 1e9  # this action's largest PHC-vs-tap rate over the pairing distance
m_full = c - a["tap"] + 10.938e6 - 0.075e6
m_rate = c - a["tap"] + 10.938e6 - u_rate
print(f"{cyc}: sample a pair distance {a['pair_dphc']:.3f} s; cause - a_phc_read = {(c - a['tap'])/1e6:.4f} ms (unrounded); "
      f"lower margin at d_lo 10.938 ms: {m_full/1e6:.4f} ms with the model's full u 0.075 ms (rounding allowance included), "
      f"{m_rate/1e6:.4f} ms with only the rate term {u_rate/1e6:.4f} ms (no rounding on unrounded inputs); "
      f"store growth that breaches it: {m_full/86.806e3:.2f} / {m_rate/86.806e3:.2f} byte times")
