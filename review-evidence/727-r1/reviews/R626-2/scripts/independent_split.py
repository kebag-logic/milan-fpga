#!/usr/bin/env python3
"""Independently recompute the five-worker split from the committed tables
(parsed as literals, the module is not imported) and compare it with the
published --list outputs.  Usage: independent_split.py SELECTOR LISTDIR"""
import ast, re, sys
src = open(sys.argv[1]).read()
table = ast.literal_eval(re.search(r"SUITE_SECONDS = (\{.*?\n\})", src, re.S).group(1))
over = list(ast.literal_eval(re.search(r"WORKER_OVERHEAD_SECONDS = (\(.*?\))", src).group(1)))
lists = [open(f"{sys.argv[2]}/shard-{i}-of-5.txt").read().split() for i in range(5)]
load = over[:]
own = {"milan_dp": 4, "tsn_fuzz": 1, "chmap_capture": 3}
for s, w in own.items():
    load[w] += table[s]
for s in sorted((s for s in table if s not in own), key=lambda s: (-table[s], s)):
    w = min(range(4), key=lambda w: (load[w], w))
    own[s] = w; load[w] += table[s]
mine = [sorted(s for s, w in own.items() if w == i) for i in range(5)]
print("independent split equals --list:", mine == [sorted(l) for l in lists])
pred = [over[i] + sum(table[s] for s in lists[i]) for i in range(5)]
print("predicted from lists:", pred, "max", max(pred), "bound 120*60*0.6 =", 120 * 36)
print("independent loads:", load)
print("with maap at the issue's 1380 s:", [p + (5 if "maap" in lists[i] else 0) for i, p in enumerate(pred)])
print("table total (s):", sum(table.values()), "+ overhead", sum(over))
