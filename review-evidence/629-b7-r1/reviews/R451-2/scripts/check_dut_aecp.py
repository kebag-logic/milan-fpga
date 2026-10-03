#!/usr/bin/env python3
"""Count the DUT's AECP command results in every run's ctl.jsonl, list each non-SUCCESS,
and show the commands that follow it.  usage: check_dut_aecp.py <packet author dir>"""
import json, sys, pathlib, collections, datetime as dt
tz = dt.timezone(dt.timedelta(hours=2))
root = pathlib.Path(sys.argv[1]) / "runs"
tot = collections.Counter(); per = {}
for d in sorted(p for p in root.iterdir() if p.is_dir()):
    f = d / "ctl.jsonl"
    if not f.exists():
        print(d.name, "no ctl.jsonl"); continue
    rows = [json.loads(x)["line"] for x in f.read_text().splitlines() if x.strip() and "line" in json.loads(x)]
    res = [r for r in rows if "cmd" in r and "status" in r]
    dut = [r for r in res if r.get("role") == "dut"]
    c = collections.Counter(r["status"] for r in dut)
    per[d.name] = (len(dut), dict(c)); tot.update(c)
    for i, r in enumerate(res):
        if r.get("role") == "dut" and r["status"] != "SUCCESS":
            print(f"{d.name}: {r['cmd']} {r['what']} {r['status']} tx {dt.datetime.fromtimestamp(r['t_tx'], tz):%H:%M:%S.%f} rx-tx {r['t_rx']-r['t_tx']:.3f} s")
            for n in res[i + 1:i + 3]:
                print(f"   next: {n['role']} {n['cmd']} {n['what']} {n['status']}")
for k, v in per.items(): print(k, v)
print("runs", len(per), "DUT total", sum(tot.values()), dict(tot))
