#!/usr/bin/env python3
"""Compare D0-063..065 and D0-024 between the round-3 and round-4 heads, after undoing the citation respelling only."""
import json, subprocess, sys
OLD, NEW = sys.argv[1:3]
def load(rev):
    return {f["id"]: f for f in json.loads(subprocess.check_output(["git", "show", f"{rev}:scripts/docs_inventory.json"]))["findings"]}
old, new = load(OLD), load(NEW)
print("ids equal:", sorted(old) == sorted(new), "count", len(new))
LIT = "`protocol-processor/hdl/top/protocol_processor_top.sv`"
REP = "`protocol_processor_top.sv` in the `protocol-processor` submodule"
for ident in sorted(new):
    o, n = old[ident], new[ident]
    changed = [k for k in sorted(set(o) | set(n)) if o.get(k) != n.get(k)]
    if not changed: continue
    print(ident, "changed:", changed)
    for k in changed:
        if k == "also":
            print("  also:", n["also"]); continue
        back = n[k].replace(REP, LIT)
        print(f"  {k}: identical after undoing respelling:", back == o[k])
        if back != o[k]:
            import difflib
            for tag, a, b, c, d in difflib.SequenceMatcher(None, o[k], back).get_opcodes():
                if tag != "equal": print("    ", tag, repr(o[k][a:b]), "->", repr(back[c:d]))
