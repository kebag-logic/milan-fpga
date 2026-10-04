#!/usr/bin/env python3
"""Recompute the available_index readings of the published B6/B7/B8 ADP enumerations.

Usage: aidx_rates.py <label>=<adp-discover.jsonl> ...  (in chronological order)
Prints, per enumeration, each answering entity by role (the entity whose
entity_capabilities equal the processor's F04.6 value 0x0000C588 is "processor",
any other is "peer"), its available_index and receive time; then, for each role,
the index step and time between consecutive enumerations and the seconds per
increment. No entity id, model id, address or name is printed.
"""
import json
import sys

PROC_CAPS = 0x0000C588
runs = []
for arg in sys.argv[1:]:
    label, path = arg.split("=", 1)
    ents, types = {}, set()
    for line in open(path):
        r = json.loads(line)
        types.add(r.get("type"))
        if r.get("type") != "adp":
            continue
        role = "processor" if int(r["entity_caps"], 16) == PROC_CAPS else "peer"
        ents.setdefault(role, []).append((r["available_index"], r["t"], r["entity_id"]))
    runs.append((label, ents, types))
    print(f"{label}: record types {sorted(types)}; " + "; ".join(
        f"{role} index {v[0][0]} at t={v[0][1]:.3f}" + (f" (+{len(v)-1} more)" if len(v) > 1 else "")
        for role, v in sorted(ents.items())))
print()
for role in ("peer", "processor"):
    for (la, ea, _), (lb, eb, _) in zip(runs, runs[1:]):
        a, b = ea[role][0], eb[role][0]
        same = "same entity_id" if a[2] == b[2] else "entity_id differs"
        di, dt = b[0] - a[0], b[1] - a[1]
        rate = f"{dt/di:.3f} s per increment" if di > 0 else "index fell: restart"
        print(f"{role} {la} -> {lb}: index {a[0]} -> {b[0]} ({di:+d}) in {dt:.0f} s: {rate}; {same}")
