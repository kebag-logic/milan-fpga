"""The PR's composed-row table, recomputed from raw results.

Usage: python3 -I table_rows.py <results-root> <label>...
Rows "X record, first/last" are the worst over the backlog groups other than
backlog-owed; "in the owed window" is backlog-owed's last AECP record. The
share line counts work passes over the four backlog groups.
"""
import json
import sys

root, labels = sys.argv[1], sys.argv[2:]
BACKLOG = ("backlog", "backlog-adp", "backlog-adp-refill", "backlog-owed")
for label in labels:
    d = json.load(open(f"{root}/{label}/results.json"))
    c = d.get("clock") or {}
    out = {}
    for r in d["results"]:
        if r["group"] not in BACKLOG:
            continue
        for p in r["probes"]:
            if p.get("status") != "measured":
                key = (p["row"] + (" [owed]" if r["group"] == "backlog-owed" else ""), "status")
                out.setdefault(key, set()).add(p.get("status"))
                continue
            row = p["row"]
            if r["group"] == "backlog-owed" and "composed load" in row:
                row += " [owed]"
            elif r["group"] == "backlog-owed":
                row += " [owed-group]"
            bound = min(p["budget_ms"], p["ceiling_ms"])
            cur = out.get(row)
            if cur is None or p["ms"] > cur[0]:
                out[row] = (p["ms"], bound, r["group"])
    print(f"== {label} {d['point']} cpu_cd={c.get('cpu_cd')} cpu_hz={c.get('cpu_hz')} sys_hz={c.get('sys_hz')}")
    for k in sorted(out, key=str):
        v = out[k]
        if isinstance(v, set):
            print(f"   {str(k):78s} status={sorted(map(str, v))}")
        else:
            print(f"   {k:78s} {v[0]:7.3f} bound {v[1]:5.1f} {'OVER' if v[0] > v[1] else 'ok'} {v[2]}")
    work = sum(r["passes"]["share"]["passes"] for r in d["results"] if r["group"] in BACKLOG)
    over = sum(r["passes"]["share"]["over"] for r in d["results"] if r["group"] in BACKLOG)
    lng = max(r["passes"]["worst"]["ms"] for r in d["results"] if r["group"] in BACKLOG)
    allw = sum(r["passes"]["share"]["passes"] for r in d["results"])
    allo = sum(r["passes"]["share"]["over"] for r in d["results"])
    alll = max(r["passes"]["worst"]["ms"] for r in d["results"])
    print(f"   SHARE backlog: {over} of {work}, longest {lng:.4f} ms | all {len(d['results'])} groups: {allo} of {allw}, longest {alll:.4f} ms")
    print(f"   refusals={d.get('refusals')} share_misses={d.get('share_misses')}")
