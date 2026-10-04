#!/usr/bin/env python3
"""Cross-check the page's run-receipts tables against the published run-receipts.json.

Usage: check_receipts.py <page.md> <run-receipts.json> <sweep_plan.json>
"""
import json, re, sys
page = open(sys.argv[1]).read(); rr = json.load(open(sys.argv[2])); plan = json.load(open(sys.argv[3]))
pts = rr["points"]
print("receipt points:", len(pts), "plan points:", len(plan["points"]))
k0 = next(iter(pts)); print("sample receipt keys:", sorted(pts[k0]) if isinstance(pts, dict) else pts[0])
rows = re.findall(r"^\| ([a-z0-9-]+) \| `(\w+)` \| (\d+) \| ([\d.]+) \| `([0-9a-f]{16})` \| (\w+) \|$", page, re.M)
print("page receipt rows:", len(rows))
fails = []
tot = 0.0
for name, top, rc, sec, dig, guard in rows:
    r = pts[name] if isinstance(pts, dict) else next(p for p in pts if p["name"] == name)
    flat = json.dumps(r)
    if dig not in flat: fails.append(f"{name} digest {dig} not in receipt")
    tot += float(sec)
    s = r["seconds"]["total"]
    if s is not None and abs(round(float(s), 1) - float(sec)) > 0.051: fails.append(f"{name} seconds {s} vs {sec}")
print("sum of page seconds (min):", round(tot / 60, 1))
names = {p["name"] for p in plan["points"]}
print("plan points missing from page:", sorted(names - {r[0] for r in rows}))
print("refused on page:", sorted(r[0] for r in rows if r[5] == "refused"))
print("FAILURES" if fails else "ALL RECEIPT ROWS MATCH", fails[:10])
sys.exit(1 if fails else 0)
