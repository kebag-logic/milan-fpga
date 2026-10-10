#!/usr/bin/env python3
"""Compare two record_configs.py outputs: the set of (side argv, unit, flags) judged, and what each read.

Usage: python3 -I compare_configs.py <old.json> <new.json>
Exit 0 when the judged configuration sets and every configuration's label, reads, deciding macros and
error state are identical; 1 otherwise (the differences printed).
"""
import json
import sys
from collections import Counter


def load(path):
    data = json.loads(open(path, encoding="utf-8").read())
    rows = {}
    dup = Counter()
    for r in data["records"]:
        key = (tuple(r["argv"]), r["unit"], tuple(r["flags"]))
        dup[key] += 1
        rows[key] = (r["label"], tuple(r["deps"]), tuple(r["tested"]), r["error"], r["stopped"])
    return data["rc"], rows, [k for k, n in dup.items() if n > 1]


rc_old, old, dup_old = load(sys.argv[1])
rc_new, new, dup_new = load(sys.argv[2])
print(f"old: rc {rc_old}, {len(old)} distinct configurations, {len(dup_old)} repeated keys")
print(f"new: rc {rc_new}, {len(new)} distinct configurations, {len(dup_new)} repeated keys")
only_old = sorted(set(old) - set(new))
only_new = sorted(set(new) - set(old))
diff = sorted(k for k in set(old) & set(new) if old[k] != new[k])
sides = Counter(k[0][0] + " " + k[0][-1] for k in new)
print("per side (compiler, language) in new:", dict(sides))
units = len({(k[0], k[1]) for k in new})
print(f"units x sides judged: old {len({(k[0], k[1]) for k in old})}, new {units}")
for title, keys in (("only in old", only_old), ("only in new", only_new), ("differ", diff)):
    print(f"{title}: {len(keys)}")
    for k in keys[:20]:
        print("  ", k[1], k[2], old.get(k), new.get(k))
sys.exit(1 if only_old or only_new or diff or rc_old or rc_new else 0)
