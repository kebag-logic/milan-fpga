#!/usr/bin/env python3
"""Every `scripts` declaration of ci/image/command-table.json whose sha256 differs from the file at a commit.

usage: command_table_pins.py <repo> <commit>
Reads both the table and the files from the commit's tree (git show), not the work tree.
"""
import hashlib, json, subprocess, sys
repo, commit = sys.argv[1:3]
def show(path):
    r = subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None
table = json.loads(show("ci/image/command-table.json"))
mism = []
for path, decl in sorted(table["scripts"].items()):
    data = show(path)
    actual = hashlib.sha256(data).hexdigest() if data is not None else "ABSENT"
    if actual != decl.get("sha256"):
        mism.append(path)
        print(f"MISMATCH {path} pin={decl.get('sha256','')[:12]} actual={actual[:12]}")
print(f"{commit}: {len(table['scripts'])} declared scripts, {len(mism)} mismatched")
