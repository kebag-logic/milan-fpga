#!/usr/bin/env python3
"""List every recorded quote that holds punctuation before its last word, with the `also` spellings it carries.

usage: tail_census.py <tree>
Reads the data file only. A quote cut from a line can run past its own clause; this is the
population that was read to decide which entries need their own sentence under `also`.
"""
import json, re, sys
from pathlib import Path
data = json.loads((Path(sys.argv[1]) / "scripts/docs_inventory.json").read_text(encoding="utf-8"))
held = 0
for f in data["findings"]:
    q = f["quote"].strip()
    if q.startswith("|") or not re.search(r"[.,;:]\**\s+\S", q):
        continue
    held += 1
    print(f"{f['id']}: {q}")
    for a in f.get("also", []):
        print(f"    also: {a}")
print(f"{held} of {len(data['findings'])} quotes hold inner punctuation (table rows not counted)")
