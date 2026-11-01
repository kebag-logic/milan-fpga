#!/usr/bin/env python3
"""List scripts whose content hash differs from their pin in ci/image/command-table.json.
usage: table_pin_drift.py <tree>"""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
table = json.loads((root / "ci/image/command-table.json").read_text())
def walk(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, dict) and "sha256" in value:
                yield key, value["sha256"]
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)
n = bad = 0
for name, pin in walk(table):
    path = root / name
    if not path.is_file():
        continue
    n += 1
    if hashlib.sha256(path.read_bytes()).hexdigest() != pin:
        bad += 1
        print("DRIFT", name)
print(f"pins checked {n}, drifted {bad}")
