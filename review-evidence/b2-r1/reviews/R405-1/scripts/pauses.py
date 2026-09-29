#!/usr/bin/env python3
"""Host-clock pauses between the last probe-bearing connect and each cycle's disconnect.
usage: pauses.py <packet author dir>"""
import json, sys
from pathlib import Path
A = Path(sys.argv[1])
def tx(p, mt):
    for l in p.read_text().splitlines():
        x = json.loads(l)
        if x.get("kind") == "transaction" and x["mt"] == mt:
            return x
prev = tx(A / "bind/bind-5/bind.jsonl", 6)["end"]
long = []
for n in range(1, 101):
    f = A / "cycles" / f"cycle-{n:03d}" / "cycle.jsonl"
    d, c = tx(f, 8), tx(f, 6)
    gap = d["start"] - prev
    if gap > 15:
        long.append((n, round(gap, 1)))
    prev = c["end"]
print("cycles whose disconnect came > 15 s after the previous connect (host clock):", long)
b1 = tx(A / "bind/bind-1/bind.jsonl", 6)
import datetime
print("bind-1 CONNECT_RX host time:", datetime.datetime.fromtimestamp(b1["start"], datetime.UTC).isoformat())
for n in range(1, 6):
    r = json.loads((A / f"bind/bind-{n}/result.json").read_text()); a = json.loads((A / f"bind/bind-{n}/analysis.json").read_text())
    print(f"bind {n}: live latency {r['latency_s']} replay {a['latency_s']} equal {r['latency_s'] == a['latency_s']}")
