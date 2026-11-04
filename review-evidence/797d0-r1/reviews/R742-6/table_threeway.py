#!/usr/bin/env python3
"""Three-way check of ci/image/command-table.json across a merge: every change each side made
relative to the base is present in the merge, and the merge adds nothing neither side made.
Usage: python3 -I table_threeway.py BASE LANE DEV MERGE   (run inside the repository)"""
import json, subprocess, sys
def load(r): return json.loads(subprocess.check_output(['git','show',r+':ci/image/command-table.json']))
def flat(o, p=()):
    """Leaves keyed by path; list items keyed by their canonical JSON so row order is not identity."""
    out = {}
    if isinstance(o, dict):
        for k, v in o.items(): out.update(flat(v, p + (k,)))
    elif isinstance(o, list) and o and all(isinstance(x,(list,str,int,float)) or x is None for x in o) and not all(isinstance(x,dict) for x in o):
        for x in o: out[p + ('[]', json.dumps(x, sort_keys=True))] = True
    elif isinstance(o, list):
        for x in o: out[p + ('[]', json.dumps(x, sort_keys=True))] = True
    else:
        out[p] = o
    return out
b, l, d, m = (flat(load(r)) for r in sys.argv[1:5])
bad = 0
for name, side in (('lane', l), ('dev', d)):
    added = {k for k in side if k not in b or side[k] != b[k]}
    removed = {k for k in b if k not in side}
    miss = [k for k in added if m.get(k, object()) != side[k]]
    kept = [k for k in removed if k in m]
    print(f"{name}: {len(added)} leaves added/changed, {len(removed)} removed; missing in merge {len(miss)}, removed-but-kept {len(kept)}")
    for k in miss + kept: print("  ", k); bad += 1
extra = [k for k in m if k not in b and k not in l and k not in d]
changed = [k for k in m if k in b and m[k] != b[k] and m[k] != l.get(k) and m[k] != d.get(k)]
print(f"merge-only leaves: {len(extra)}, merge-only values: {len(changed)}")
bad += len(extra) + len(changed)
print("RESULT", "OK" if bad == 0 else "FAIL"); sys.exit(1 if bad else 0)
