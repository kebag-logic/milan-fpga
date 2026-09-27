#!/usr/bin/env python3
"""R362-1: compare base and head plan JSON; report every step whose content differs.

Usage: plan_diff.py BASE.json HEAD.json
Exit 0 when only soak or power steps differ, 1 otherwise.
"""
import json
import sys


def steps(doc):
    if isinstance(doc, dict):
        for key in ("steps", "plan"):
            if key in doc:
                return steps(doc[key])
        return doc
    return {str(s.get("sid", i)): s for i, s in enumerate(doc)}


base = steps(json.load(open(sys.argv[1])))
head = steps(json.load(open(sys.argv[2])))
changed = sorted(k for k in set(base) | set(head) if base.get(k) != head.get(k))
print(f"steps base={len(base)} head={len(head)} changed={len(changed)}")
for key in changed:
    b, h = base.get(key, {}), head.get(key, {})
    print(f"CHANGED {key}")
    if isinstance(b, dict) and isinstance(h, dict):
        for field in sorted(set(b) | set(h)):
            if b.get(field) != h.get(field):
                if field == "args" and isinstance(b.get(field), dict):
                    for arg in sorted(set(b[field]) | set(h[field])):
                        if b[field].get(arg) != h[field].get(arg):
                            print(f"  args.{arg}: {b[field].get(arg)!r} -> {h[field].get(arg)!r}")
                else:
                    print(f"  {field} differs")
sys.exit(0 if all(k.startswith(("soak.", "power.")) for k in changed) else 1)
