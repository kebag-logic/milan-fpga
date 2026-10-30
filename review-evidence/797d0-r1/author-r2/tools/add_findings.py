#!/usr/bin/env python3
"""Append findings to scripts/docs_inventory.json in its own serialization.

Usage: python3 -I add_findings.py <tree> <findings.json>

<findings.json> is a list of {id, page, quote, source, correction}. Each quote
must occur on its page exactly once and each id must be new; the data file is
rewritten as json.dumps(indent=1, ensure_ascii=False) plus a newline, the form
the committed file already has.
"""
import json
import sys
from pathlib import Path

tree, batch = Path(sys.argv[1]), Path(sys.argv[2])
data_path = tree / "scripts/docs_inventory.json"
data = json.loads(data_path.read_text(encoding="utf-8"))
known = {f["id"] for f in data["findings"]}
problems = []
for entry in json.loads(batch.read_text(encoding="utf-8")):
    text = (tree / entry["page"]).read_text(encoding="utf-8")
    hits = sum(entry["quote"] in line for line in text.split("\n"))
    if hits != 1:
        problems.append(f"{entry['id']}: quote found on {hits} lines of {entry['page']}")
    if entry["id"] in known:
        problems.append(f"{entry['id']}: duplicate id")
    if "—" in json.dumps(entry, ensure_ascii=False):
        problems.append(f"{entry['id']}: carries an em dash")
    known.add(entry["id"])
    data["findings"].append({k: entry[k] for k in ("id", "page", "quote", "source", "correction")})
if problems:
    print("\n".join(problems))
    raise SystemExit(1)
data_path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"{len(data['findings'])} findings")
