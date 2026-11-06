#!/usr/bin/env python3
"""Compare a resource baseline at two revisions: which keys moved, per endpoint."""
import json, subprocess, sys
repo, old, new = sys.argv[1:4]
def load(rev):
    return json.loads(subprocess.check_output(["git","-C",repo,"show",f"{rev}:syn/ooc/pp_resource_baseline.json"]))
a, b = load(old), load(new)
print("top keys equal:", list(a)==list(b), "description equal:", a["description"]==b["description"], "schema", a["schema"], b["schema"])
for ep in b["endpoints"]:
    x, y = a["endpoints"][ep], b["endpoints"][ep]
    print("==", ep, "keys equal/ordered:", list(x)==list(y))
    for k in y:
        if x.get(k)==y[k]:
            print("  same   ", k); continue
        if isinstance(y[k], dict):
            ch=[q for q in set(x[k])|set(y[k]) if x[k].get(q)!=y[k].get(q)]
            print("  CHANGED", k, "subkeys", len(ch), "of", len(y[k]), sorted(ch)[:14])
        else:
            print("  CHANGED", k, repr(x[k])[:220], "->", repr(y[k])[:400])
