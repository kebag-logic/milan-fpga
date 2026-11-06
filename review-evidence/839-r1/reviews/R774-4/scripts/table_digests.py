#!/usr/bin/env python3
"""Compare ci/image/command-table.json 'scripts' digests with the file bytes of a git commit.
usage: table_digests.py REPO COMMIT  -> prints MISMATCH/MISSING lines and a count."""
import hashlib, json, subprocess, sys
repo, commit = sys.argv[1], sys.argv[2]
t = json.loads(subprocess.run(["git", "-C", repo, "show", f"{commit}:ci/image/command-table.json"],
                              check=True, capture_output=True).stdout)
bad = []
for path, e in sorted(t["scripts"].items()):
    r = subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"], capture_output=True)
    if r.returncode:
        bad.append(f"MISSING {path}")
    elif "sha256" in e and hashlib.sha256(r.stdout).hexdigest() != e["sha256"]:
        bad.append(f"MISMATCH {path}")
print("\n".join(bad)); print(f"{commit}: {len(bad)} of {len(t['scripts'])} declared scripts mismatch or missing")
