#!/usr/bin/env python3
"""inventory_walk.py's walk, carried past a base's own drift so the refusals a
change adds are reached even when the base already refuses earlier.

usage: CI_IMAGE_SHFMT=<pinned shfmt> python3 inventory_walk_far.py <disposable-root>
Runs scripts/ci_tool_inventory.py --check in a DISPOSABLE copy, recording every
refusal in order. Each "changed declared script" refusal re-pins that script's
sha256 in the copy's ci/image/command-table.json; each "undeclared executing or
network script" refusal declares that script "reviewed non-installing" in the
copy. Any other refusal ends the walk and is printed as the stop reason. Never
point it at a checkout you care about.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
table_path = root / "ci/image/command-table.json"
REASON = "Validation and source inspection: invokes existing tools or local fixtures; installs nothing."


def check():
    out = subprocess.run([sys.executable, "scripts/ci_tool_inventory.py", "--check"],
                         cwd=root, capture_output=True, text=True, check=False)
    return out.returncode, (out.stdout + out.stderr).strip()


for step in range(200):
    rc, text = check()
    print(f"step {step}: rc={rc} {text}", flush=True)
    changed = re.search(r"changed declared script '([^']+)'", text)
    undeclared = re.search(r"undeclared executing or network script '([^']+)'", text)
    if not (changed or undeclared):
        print(f"stop: {'clean' if rc == 0 else 'refusal outside the walk'}")
        break
    rel = (changed or undeclared).group(1)
    table = json.loads(table_path.read_text())
    new = hashlib.sha256((root / rel).read_bytes()).hexdigest()
    if changed:
        print(f"  re-pin {rel}: {table['scripts'][rel]['sha256']} -> {new}")
        table["scripts"][rel]["sha256"] = new
    else:
        print(f"  declare {rel}: reviewed non-installing {new}")
        table["scripts"][rel] = {"class": "reviewed non-installing", "reason": REASON, "sha256": new}
        table["scripts"] = dict(sorted(table["scripts"].items()))
    table_path.write_text(json.dumps(table, indent=2, ensure_ascii=False) + "\n")
