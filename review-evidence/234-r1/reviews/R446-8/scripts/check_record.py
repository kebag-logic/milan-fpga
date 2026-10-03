#!/usr/bin/env python3
"""R446-8: compare the committed resource baseline at a head with the published
round-7 record-write receipts and with the pre-re-baseline policy.

usage: check_record.py <repo> <head> <old-rev> <receipts-dir>
Prints one line per check and exits 1 on any mismatch.
"""
import json
import subprocess
import sys

repo, head, old, rdir = sys.argv[1:5]
PATH = "syn/ooc/pp_resource_baseline.json"


def load(rev):
    out = subprocess.run(["git", "-C", repo, "show", f"{rev}:{PATH}"],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def receipt_record(endpoint):
    text = open(f"{rdir}/real/record-write-C-{endpoint}.log").read()
    body = text[text.index("\n{") + 1:]
    return json.loads(body)


new, prev = load(head), load(old)
bad = 0


def report(ok, msg):
    global bad
    bad += not ok
    print(("OK   " if ok else "FAIL ") + msg)


report(set(new) == set(prev), f"top-level keys equal: {sorted(new)}")
for k in new:
    if k != "endpoints":
        report(new[k] == prev[k], f"top-level {k!r} unchanged")
report(list(new["endpoints"]) == list(prev["endpoints"]),
       f"endpoint list unchanged: {list(new['endpoints'])}")
for ep, rec in new["endpoints"].items():
    old_ep = prev["endpoints"][ep]
    report(set(rec) == set(old_ep), f"{ep}: keys {sorted(rec)}")
    for field in sorted(set(rec) | set(old_ep)):
        if field in ("record", "measured"):
            continue
        a, b = old_ep.get(field), rec.get(field)
        report(a == b and type(a) is type(b),
               f"{ep}: policy {field} unchanged {json.dumps(b, sort_keys=True)}")
        for sub in sorted(set(a or {}) | set(b or {})):
            x, y = (a or {}).get(sub), (b or {}).get(sub)
            report(x == y and type(x) is type(y),
                   f"{ep}: {field}.{sub} {x!r} -> {y!r}")
    receipt = receipt_record(ep)
    report(rec["record"] == receipt,
           f"{ep}: committed record equals the published record-write output")
    for part in ("kind", "identity", "inputs_sha256", "figures", "scopes"):
        report(rec["record"][part] == receipt[part], f"{ep}: record.{part} equals receipt")
    report(rec["record"]["identity"] == old_ep["record"]["identity"],
           f"{ep}: identity (tool, device, design, state, flow, clock) unchanged from {old[:8]}")
    print(f"     {ep}: measured = {rec['measured']!r}")
    print(f"     {ep}: figures = {json.dumps(rec['record']['figures'], sort_keys=True)}")
    print(f"     {ep}: figures {old[:8]} = {json.dumps(old_ep['record']['figures'], sort_keys=True)}")

print(f"mismatches: {bad}")
sys.exit(1 if bad else 0)
