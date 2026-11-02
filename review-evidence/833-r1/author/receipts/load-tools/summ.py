#!/usr/bin/env python3
"""usage: summ.py <focus jsonl> [trace jsonl]  Scratch only: outcome counts, cleanup-time distribution, failing traces."""
import json, sys, collections
rows = [json.loads(l) for l in open(sys.argv[1])]
print(collections.Counter((r["case"], r["outcome"]) for r in rows))
for r in rows:
    if r["outcome"] != "pass":
        print("  FAIL", r["case"], r["outcome"], r["seconds"], "load", r["load"], r["text"][:900].replace("\n", " | "))
if len(sys.argv) > 2:
    tr = [json.loads(l) for l in open(sys.argv[2])]
    el = sorted(t["elapsed"] for t in tr)
    q = lambda f: el[min(len(el) - 1, int(f * len(el)))]
    print(f"cleanups {len(tr)} failed {sum(t['outcome'] != 'clean' for t in tr)} elapsed p50 {q(.5)} p90 {q(.9)} p99 {q(.99)} max {el[-1]}")
    slow = sorted((p[1] for t in tr for p in t["passes"]))
    print(f"pass time p50 {slow[len(slow)//2]} p99 {slow[int(.99*len(slow))]} max {slow[-1]} passes/cleanup median {sorted(len(t['passes']) for t in tr)[len(tr)//2]}")
