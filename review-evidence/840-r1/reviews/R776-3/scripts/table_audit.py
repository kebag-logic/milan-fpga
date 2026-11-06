#!/usr/bin/env python3
"""Compare command-table script pins and the tool-inventory input pins with blob bytes, per revision.

Usage: table_audit.py <repo> <rev> [<rev> ...]. Reads git objects only; writes nothing.
"""
import hashlib, json, subprocess, sys

repo, revs = sys.argv[1], sys.argv[2:]

def blob(rev, path):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None

def sha(data):
    return None if data is None else hashlib.sha256(data).hexdigest()

result = {}
for rev in revs:
    table = json.loads(blob(rev, "ci/image/command-table.json"))
    stale = sorted(p for p, row in table["scripts"].items() if row["sha256"] != sha(blob(rev, p)))
    inventory = json.loads(blob(rev, "ci/image/tool-inventory.json"))
    inputs = inventory["inputs"]
    stale_inputs = sorted(p for p, want in inputs.items() if want != sha(blob(rev, p)))
    result[rev] = (set(stale), set(stale_inputs))
    print(f"{rev}: table rows {len(table['scripts'])}, stale {len(stale)}; "
          f"inventory inputs {len(inputs)}, stale {len(stale_inputs)}")
    print(f"  table sha256 {sha(blob(rev, 'ci/image/command-table.json'))}")
    print(f"  inventory pin of table {inputs.get('ci/image/command-table.json')}")
    print(f"  stale inventory inputs: {stale_inputs}")
base = revs[0]
for rev in revs[1:]:
    print(f"{base} -> {rev}")
    print("  table added:", sorted(result[rev][0] - result[base][0]))
    print("  table removed:", sorted(result[base][0] - result[rev][0]))
    print("  inventory added:", sorted(result[rev][1] - result[base][1]))
    print("  inventory removed:", sorted(result[base][1] - result[rev][1]))
