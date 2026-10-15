#!/usr/bin/env python3
"""Compare the existing policy scanner on changed files at base and head."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

p = argparse.ArgumentParser()
p.add_argument("repository", type=Path)
p.add_argument("--scratch", type=Path, required=True)
a = p.parse_args()
root = a.repository.resolve()
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("policy_scanner", root / "scripts/check_baremetal_only.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
base = "84f9e3001b7d9b77835c4a9a599dbe6230a8031b"
files = subprocess.check_output(["git", "-C", str(root), "diff", "--name-only", base, "HEAD"], text=True).splitlines()
with tempfile.TemporaryDirectory(prefix="policy-base-", dir=a.scratch) as tmp:
    old = Path(tmp)
    for name in files:
        target = old / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(subprocess.check_output(["git", "-C", str(root), "show", base + ":" + name]))
    old_findings = [f for name in files for f in gate.scan_file(old, name)]
    new_findings = [f for name in files for f in gate.scan_file(root, name)]
print("Focused content scan; no elaboration, no full bank.")
print(f"Base changed-file findings: {len(old_findings)}")
print(f"Head changed-file findings: {len(new_findings)}")
for f in new_findings:
    print(f)
assert len(old_findings) == 0 and len(new_findings) == 21
print("REPRODUCED: 21 new policy findings, matching hosted job 116583405450.")
