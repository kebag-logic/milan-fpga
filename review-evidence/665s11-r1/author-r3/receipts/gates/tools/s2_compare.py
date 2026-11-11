#!/usr/bin/env python3
"""s2_compare.py <base results.json> <head results.json>: each path's worst instance (path.if<n>) at the base and
the head, the paths over T_svc at either, and the range of the change over the paths both measured."""
import json, sys
def probes(f):
    out = {}
    for p in json.load(open(f))['paths']:
        w = p['worst']
        out[f"{p['path']}.if{p['interface']}"] = (w['ms'], w['within_t_svc'], w['start_sys'])
    return out
b, h = probes(sys.argv[1]), probes(sys.argv[2])
print(f"paths: base {len(b)}, head {len(h)}, both {len(set(b) & set(h))}")
print(f"over T_svc: base {sum(not v[1] for v in b.values())}, head {sum(not v[1] for v in h.values())}")
for k in sorted(set(b) & set(h)):
    if b[k][1] != h[k][1]:
        print(f"  {k}: base {b[k][0]:.3f} ms (start {b[k][2]}), head {h[k][0]:.3f} ms (start {h[k][2]}): "
              f"{'newly over' if b[k][1] else 'no longer over'} T_svc")
d = sorted(h[k][0] - b[k][0] for k in set(b) & set(h))
print(f"change head - base over every path both measured: {d[0]:+.3f} to {d[-1]:+.3f} ms")
