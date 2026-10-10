#!/usr/bin/env python3
"""Diff the three recorded endpoints of pp_resource_baseline.json between two revisions.

Usage: record_delta.py <repo> <old-rev> <new-rev>
"""
import json
import subprocess
import sys


def load(repo, rev):
    out = subprocess.run(["git", "-C", repo, "show", f"{rev}:syn/ooc/pp_resource_baseline.json"],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)


repo, old_rev, new_rev = sys.argv[1:4]
old, new = load(repo, old_rev), load(repo, new_rev)
for ep in ("route-1x1", "ooc-1x1", "ooc-8x8"):
    o, n = old["endpoints"][ep], new["endpoints"][ep]
    for part in ("tolerance", "floor", "ceiling"):
        print(f"{ep} {part} {'same' if o.get(part) == n.get(part) else 'CHANGED'}")
    orec, nrec = o["record"], n["record"]
    print(f"{ep} identity {'same' if orec['identity'] == nrec['identity'] else 'CHANGED'}")
    print(f"{ep} inputs_sha256 {orec['inputs_sha256'][:8]} -> {nrec['inputs_sha256'][:8]}")
    fchg = {k: (orec['figures'].get(k), v) for k, v in nrec['figures'].items() if orec['figures'].get(k) != v}
    print(f"{ep} figures changed: {fchg if fchg else 'none'}")
    schg = sorted(s for s in set(orec['scopes']) | set(nrec['scopes']) if orec['scopes'].get(s) != nrec['scopes'].get(s))
    print(f"{ep} scopes changed: {len(schg)} of {len(nrec['scopes'])}")
