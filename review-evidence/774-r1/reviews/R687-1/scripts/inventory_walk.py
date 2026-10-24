#!/usr/bin/env python3
"""Walk scripts/ci_tool_inventory.py --check past each "changed declared
script" refusal on a DISPOSABLE copy of a tree, recording every refusal in
order, so the refusals a change adds can be told from those its base
already had.

usage: CI_IMAGE_SHFMT=<pinned shfmt> python3 inventory_walk.py <disposable-root>
Each step re-pins only the refused script's sha256 in the copy's
ci/image/command-table.json and re-runs the check; then, when the refusal is
the inventory drift, it runs --write in the copy and prints the inventory
diff. Never point it at a checkout you care about.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
table_path = root / "ci/image/command-table.json"
inv_path = root / "ci/image/tool-inventory.json"


def check() -> tuple[int, str]:
    out = subprocess.run([sys.executable, "scripts/ci_tool_inventory.py", "--check"],
                         cwd=root, capture_output=True, text=True, check=False)
    return out.returncode, (out.stdout + out.stderr).strip()


for step in range(20):
    rc, text = check()
    print(f"step {step}: rc={rc} {text}")
    m = re.search(r"changed declared script '([^']+)'", text)
    if not m:
        break
    rel = m.group(1)
    table = json.loads(table_path.read_text())
    new = hashlib.sha256((root / rel).read_bytes()).hexdigest()
    print(f"  re-pin {rel}: {table['scripts'][rel]['sha256']} -> {new}")
    table["scripts"][rel]["sha256"] = new
    table_path.write_text(json.dumps(table, indent=2) + "\n")

if "tool inventory differs" in text:
    before = json.loads(inv_path.read_text())
    out = subprocess.run([sys.executable, "scripts/ci_tool_inventory.py", "--write"],
                         cwd=root, capture_output=True, text=True, check=False)
    print(f"write: rc={out.returncode} {(out.stdout + out.stderr).strip()}")
    after = json.loads(inv_path.read_text())
    for key in ("inputs",):
        for k in sorted(set(before[key]) | set(after[key])):
            if before[key].get(k) != after[key].get(k):
                print(f"  {key} {k}: {before[key].get(k)} -> {after[key].get(k)}")
    for k in sorted(set(before["residue"]) ^ set(after["residue"])):
        print(f"  residue {'+' if k in after['residue'] else '-'} {k}")
    bt = {json.dumps(t, sort_keys=True) for t in before["tools"]}
    at = {json.dumps(t, sort_keys=True) for t in after["tools"]}
    for t in sorted(bt ^ at):
        print(f"  tool {'+' if t in at else '-'} {t}")
    rc, text = check()
    print(f"final check: rc={rc} {text}")
