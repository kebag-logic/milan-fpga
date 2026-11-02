"""Recompute the composed rows and the per-pass share from the author's raw results.

Usage: python3 -I recompute_rows.py <results-root> <label>...
Each <label> names <results-root>/<label>/results.json. Prints, per label, the
clock record, every row's worst ms over the backlog groups with its bound
min(budget_ms, ceiling_ms), and the share verdict over the work passes.
"""
import json
import sys

root, labels = sys.argv[1], sys.argv[2:]
for label in labels:
    d = json.load(open(f"{root}/{label}/results.json"))
    print(f"== {label} point={d['point']} clock={json.dumps(d.get('clock'))}")
    rows, mism = {}, 0
    groups = [r["group"] for r in d["results"]]
    for r in d["results"]:
        for p in r["probes"]:
            if p.get("status") != "measured":
                continue
            if p["sys_cycles"] != p["cpu_cycles"]:
                mism += 1
            bound = min(p["budget_ms"], p["ceiling_ms"])
            key = p["row"]
            cur = rows.get(key)
            if cur is None or p["ms"] > cur[0]:
                rows[key] = (p["ms"], bound, r["group"], p["probe"])
    print(f"   groups={groups} cpu!=sys probes={mism}")
    for k, (ms, bound, g, probe) in sorted(rows.items()):
        flag = "OVER" if ms > bound else "ok"
        print(f"   {k:70s} {ms:8.3f} / {bound:5.1f} {flag} ({g}:{probe})")
    tot = over = 0
    longest = (0, None)
    for r in d["results"]:
        s = r["passes"]["share"]
        tot += s["passes"]
        over += s["over"]
        w = r["passes"]["worst"]
        if w["ms"] > longest[0]:
            longest = (w["ms"], r["group"])
        print(f"   share {r['group']:24s} work={s['passes']:5d} over={s['over']} longest={w['ms']:.4f} ms share={s['ms']} cycles={s['cycles']}")
    backlog_tot = sum(r["passes"]["share"]["passes"] for r in d["results"] if r["group"].startswith("backlog"))
    print(f"   SHARE total work={tot} (backlog groups {backlog_tot}) over={over} longest={longest}")
    print(f"   composed_maximum={json.dumps(d.get('composed_maximum'))[:300]}")
    print(f"   refusals={json.dumps(d.get('refusals'))[:300]} misses={len(d.get('misses') or [])} share_misses={json.dumps(d.get('share_misses'))[:200]}")
