#!/usr/bin/env python3
"""Compare D3 section 15.1 'Selected option' cells with the manager ruling table.

Usage: compare_rulings.py <issue70_comments.json> <SAVED_STATE_MATERIALIZATION.md>
Exit 0 only if all ten IDs are present, marked RULED, and byte-identical.
"""
import json, re, sys

comments = json.load(open(sys.argv[1]))
ruling = [c for c in comments if c["id"] == 5862405632][0]["body"]
page = open(sys.argv[2], encoding="utf-8").read()

def rows(text):
    out = {}
    for line in text.splitlines():
        if not line.startswith("| DR"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        out[cells[0]] = cells
    return out

r = rows(ruling)
sec = page.split("### 15.1 Manager decision register", 1)[1].split("### 15.2", 1)[0]
p = rows(sec)
ids = ["DR1a", "DR1b", "DR2a", "DR2b", "DR2c", "DR3a", "DR3b", "DR4", "DR5", "DR6"]
bad = 0
print("ruling ids:", list(r))
for i in ids:
    key = [k for k in p if k.startswith(i + ":")]
    if i not in r or len(key) != 1:
        print(i, "MISSING", i in r, key); bad += 1; continue
    pc = p[key[0]]
    ruled = "**RULED**" in pc[0]
    same = pc[2] == r[i][1]
    print(f"{i}: status_ruled={ruled} selected_identical={same}")
    if not same:
        print("  ruling:", r[i][1]); print("  page  :", pc[2])
    bad += (not ruled) + (not same)
extra = [k for k in p if k.split(":")[0] not in ids]
print("extra page rows:", extra)
print("RESULT", "PASS" if bad == 0 and not extra else "FAIL")
sys.exit(1 if bad or extra else 0)
