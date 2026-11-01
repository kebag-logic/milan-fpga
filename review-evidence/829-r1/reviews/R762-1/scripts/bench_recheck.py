#!/usr/bin/env python3
"""Recompute the bench table's derived figures from the author's public receipts.
usage: bench_recheck.py <author dir>"""
import json, re, statistics, sys
from pathlib import Path
A = Path(sys.argv[1]); RC = A / "receipts"; table = (RC / "table.md").read_text()
bad = 0
for row in sorted(RC.glob("*/row.json")):
    d = json.loads(row.read_text()); name = row.parent.name
    if name.startswith("m-"): continue
    diff = round(d["arty"] - d["zero"], 1); total = round(diff + d["ingress"] + d["egress"], 1)
    gl = f'{d["ingress"]:04x}{d["egress"]:04x}'
    ok_lat = gl == d["gptp_lat"]
    in_table = re.search(rf'`{name}`\) \| in \| {d["n_arty"]} \| {d["arty"]}, {d["arty_sd"]} \| {d["zero"]}, {d["zero_sd"]} \| {d["residual"]} \| {d["sum"]} \|', table) is not None
    poll = (row.parent / "poll.txt").read_text() if (row.parent / "poll.txt").exists() else ""
    flag = "" if abs(diff-d["residual"]) <= .11 and abs(total-d["sum"]) <= .11 and ok_lat else "  <-- MISMATCH"
    bad += bool(flag)
    print(f"{name:32} n={d['n_arty']:4} arty {d['arty']:7} zero {d['zero']:7} diff {diff:7} sum {total:7} lat {d['gptp_lat']} pd {d['pdelay_mean']} ({d['pdelay_min']}..{d['pdelay_max']}) asc {d['ascapable']} sync {d['sync']} in_table={in_table}{flag}")
print("mismatches", bad)
for name in ("f-10-tap-comp-sync-a", "f-11-tap-comp-sync-b"):
    d = json.loads((RC/name/"row.json").read_text()); o = (RC/name/"offset.txt").read_text().splitlines()[0]
    print(name, "zero-pdelay", round(d["pdelay_mean"]-d["zero"],1), "|", o)
    p = (RC/name/"poll.txt").read_text()
    print("   polls with status lines", len(re.findall(r"ASCAPABLE=", p)), "ascapable=1", len(re.findall(r"ASCAPABLE=1", p)), "sync=1", len(re.findall(r"\bSYNC=1", p)))
for name in ("stream-1", "stream-2"):
    print(name, (RC/name/"summary.txt").read_text()[:900])
print("bench-left-final", (RC/"bench-left-final"/"row.json").read_text()[:300])
