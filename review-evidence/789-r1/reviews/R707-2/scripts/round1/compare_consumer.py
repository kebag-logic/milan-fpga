#!/usr/bin/env python3
"""Compare dev's and the head's generated jobs in rtl-fast.yml: steps kept, removed, added; timeouts; other jobs.

Usage: compare_consumer.py <dev-rtl-fast.yml> <head-rtl-fast.yml>
"""
import sys
import yaml

dev, head = (yaml.safe_load(open(p)) for p in sys.argv[1:3])
strip = lambda s: {k: v for k, v in s.items() if k != "id"}
for job in ("yosys-elaboration",):
    d, h = dev["jobs"][job]["steps"], head["jobs"][job]["steps"]
    dn = [s.get("name", s.get("uses")) for s in d]
    hn = [s.get("name", s.get("uses")) for s in h]
    print(job, "dev steps:", len(d), "head steps:", len(h))
    print("  removed:", [n for n in dn if n not in hn])
    print("  added:", [n for n in hn if n not in dn])
    kept = [n for n in dn if n in hn]
    print("  kept in order:", kept == [n for n in hn if n in dn])
    changed = [n for n in kept if strip(d[dn.index(n)]) != strip(h[hn.index(n)])]
    print("  kept steps whose body differs (ids ignored):", changed)
for job in sorted(set(dev["jobs"]) | set(head["jobs"])):
    a, b = dev["jobs"].get(job), head["jobs"].get(job)
    if a is None or b is None:
        print("job only in", "head" if a is None else "dev", ":", job, "timeout", (b or a).get("timeout-minutes"))
    elif a != b:
        print("job differs:", job, "timeout dev", a.get("timeout-minutes"), "head", b.get("timeout-minutes"))
    if b is not None and b.get("timeout-minutes", 0) > 30 and job != "publication-census":
        print("  timeout above 30:", job, b.get("timeout-minutes"))
print("head timeouts:", {j: v.get("timeout-minutes") for j, v in head["jobs"].items()})
print("dev timeouts: ", {j: v.get("timeout-minutes") for j, v in dev["jobs"].items()})
