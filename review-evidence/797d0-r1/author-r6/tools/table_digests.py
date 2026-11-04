#!/usr/bin/env python3
"""Compare every declared script digest in ci/image/command-table.json with the file's bytes, at one tree.

usage: python3 -I table_digests.py <tree>
Prints each mismatch or missing file, then the counts. Read-only.
"""
import hashlib, json, sys
from pathlib import Path
tree = Path(sys.argv[1])
scripts = json.loads((tree / "ci/image/command-table.json").read_text())["scripts"]
bad = 0
for name, entry in sorted(scripts.items()):
    path = tree / name
    if not path.is_file():
        print(f"MISSING {name}"); bad += 1; continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != entry["sha256"]:
        print(f"MISMATCH {name}: declared {entry['sha256'][:12]}, bytes {actual[:12]}"); bad += 1
for name in ("scripts/docs_inventory.py", "scripts/ci_litex_legs.py", "scripts/ci_gate_workflows_selftest.py",
             "scripts/ci_scope_history.py", "scripts/run_litex_sims.sh"):
    print(f"{name}: declared {'and matches' if name in scripts and hashlib.sha256((tree / name).read_bytes()).hexdigest() == scripts[name]['sha256'] else 'NO MATCH'}")
print(f"{len(scripts)} declared scripts, {bad} mismatched or missing")
