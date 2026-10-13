#!/usr/bin/env python3
"""Extract the pinned public evidence, excluding handoff prose and other reviews."""
import argparse
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument("source", type=Path)
p.add_argument("packet", type=Path)
a = p.parse_args()
rev = "a7ca711b8256ea6d655203364a2b83c1af340f48"
prefix = "review-evidence/734-r1/"
git = ["git", "-C", str(a.source.resolve())]
probe = subprocess.run([*git, "cat-file", "-e", rev], capture_output=True)
if probe.returncode:
    subprocess.run([*git, "fetch", "--no-tags", "https://github.com/kebag-logic/milan-fpga.git", rev], check=True)
paths = subprocess.check_output([*git, "ls-tree", "-r", "--name-only", rev, "--", prefix], text=True).splitlines()
for path in paths:
    if path.endswith(("HANDOFF.md", "PR-BODY.md")):
        continue
    dest = a.packet.resolve()/"scratch/public-evidence"/path.removeprefix(prefix)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(subprocess.check_output([*git, "show", rev+":"+path]))
print("Pinned public receipts extracted to scratch/public-evidence")
