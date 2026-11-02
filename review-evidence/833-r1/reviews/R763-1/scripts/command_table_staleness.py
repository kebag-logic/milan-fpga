#!/usr/bin/env python3
"""Count command-table script pins whose sha256 differs from a given git tree.

Usage: command_table_staleness.py REPO COMMIT  (reads ci/image/command-table.json at COMMIT)
"""
import hashlib, json, subprocess, sys
repo, commit = sys.argv[1], sys.argv[2]
def blob(path):
    r = subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None
table = json.loads(blob("ci/image/command-table.json"))
pins = {p: v["sha256"] for p, v in table["scripts"].items() if isinstance(v, dict) and "sha256" in v}
stale, missing = [], []
for path, digest in sorted(pins.items()):
    data = blob(path)
    if data is None:
        missing.append(path)
    elif hashlib.sha256(data).hexdigest() != digest:
        stale.append(path)
print(f"commit {commit}: pinned {len(pins)} stale {len(stale)} missing {len(missing)}")
for p in stale: print("  stale", p)
for p in missing: print("  missing", p)
