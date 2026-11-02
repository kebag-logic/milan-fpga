#!/usr/bin/env python3
"""Round 4 data checks, read from Git. Usage: check_data.py <repo> <old> <new>."""
import json, re, subprocess, sys
repo, old, new = sys.argv[1:4]
def load(rev):
    return json.loads(subprocess.check_output(["git", "-C", repo, "show", f"{rev}:scripts/docs_inventory.json"], text=True))
a, b = load(old), load(new)
fa = {f["id"]: f for f in a["findings"]}; fb = {f["id"]: f for f in b["findings"]}
print("finding ids identical:", list(fa) == list(fb), len(fb))
LIT = "`protocol-processor/hdl/top/protocol_processor_top.sv`"
NEW = "`protocol_processor_top.sv` in the `protocol-processor` submodule,"
for i in fb:
    for k in ("page", "quote", "source", "correction"):
        if fa[i][k] != fb[i][k]:
            # undo the path rewrite and name the remaining byte difference
            restored = fb[i][k].replace(NEW + " ", LIT + " ").replace(NEW, LIT)
            same = restored == fa[i][k]
            print(i, k, "differs; only the path spelling" if same else "differs in more than the path spelling")
            if not same:
                x, y = fa[i][k], restored
                p = next((n for n in range(min(len(x), len(y))) if x[n] != y[n]), 0)
                print("   old:", x[max(0, p-40):p+60]); print("   new:", y[max(0, p-40):p+60])
print("also entries:")
for i, f in fb.items():
    for s in f.get("also", []):
        page = subprocess.check_output(["git", "-C", repo, "show", f"{new}:{f['page']}"], text=True)
        print(f"  {i} on_page={s in page} in_quote={s.rstrip('.') in f['quote']} {s!r}  <- quote {f['quote']!r}")
tail = re.compile(r"[.,;:]\s+\S+(?:\s+\S+){0,3}$")
print("quotes with words after inner punctuation and no also:")
for i, f in fb.items():
    if tail.search(f["quote"]) and not f.get("also"):
        print(f"  {i} {f['quote']!r}")
