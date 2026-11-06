#!/usr/bin/env python3
"""Compare every path-keyed sha256 in ci/image/command-table.json with the blob at each commit.

usage: table_digests.py <repo clone> <commit> [<commit> ...]
"""
import hashlib
import json
import subprocess
import sys


def walk(node, trail=()):
    if isinstance(node, dict):
        if "sha256" in node and trail and isinstance(trail[-1], str):
            yield trail[-1], node["sha256"]
        for key, value in node.items():
            yield from walk(value, trail + (key,))
    elif isinstance(node, list):
        for value in node:
            yield from walk(value, trail)


def blob(repo, commit, path):
    shown = subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"], capture_output=True, check=False)
    return shown.stdout if shown.returncode == 0 else None


repo, sets = sys.argv[1], {}
for commit in sys.argv[2:]:
    table = json.loads(blob(repo, commit, "ci/image/command-table.json"))
    rows = [(p, d) for p, d in walk(table) if blob(repo, commit, p) is not None]
    sets[commit] = {p for p, d in rows if hashlib.sha256(blob(repo, commit, p)).hexdigest() != d}
    print(commit[:8], "entries", len(rows), "mismatched", len(sets[commit]))
first, *rest = sys.argv[2:]
for other in rest:
    print("only at", first[:8], sorted(sets[first] - sets[other]))
    print("only at", other[:8], sorted(sets[other] - sets[first]))
print("docs_inventory mismatched at", [c[:8] for c in sets if "scripts/docs_inventory.py" in sets[c]])
