#!/usr/bin/env python3
"""usage: latsum.py <jsonl> ...  Scratch only: SIGKILL-to-death distribution per kind, slowest samples and what they were doing."""
import json, sys, collections
for path in sys.argv[1:]:
    rows = [json.loads(l) for l in open(path)]
    for kind in ("idle", "forker"):
        a = sorted(r["latency"] for r in rows if r["kind"] == kind)
        if not a: continue
        q = lambda f: a[min(len(a) - 1, int(f * len(a)))]
        print(f"{path.rsplit('/',1)[1]} {kind}: n {len(a)} p50 {q(.5)} p99 {q(.99)} p99.9 {q(.999)} max {a[-1]}  over 1 s: {sum(x > 1 for x in a)}  over 2 s: {sum(x > 2 for x in a)}  over 4 s: {sum(x > 4 for x in a)}")
    for r in sorted(rows, key=lambda r: -r["latency"])[:5]:
        print("   slowest", r["latency"], r["kind"], "spawn", r["spawn"], "load", r["load"], r["seen"])
    c = collections.Counter()
    for r in rows:
        for k, v in r["seen"].items():
            if k.startswith("D"): c[k] += v
    print("   D samples by wait channel:", c.most_common(8))
    print("   spawn: p50", sorted(r["spawn"] for r in rows)[len(rows)//2], "max", max(r["spawn"] for r in rows), " load max", max(r["load"] for r in rows))
