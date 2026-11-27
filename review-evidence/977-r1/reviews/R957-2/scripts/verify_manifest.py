#!/usr/bin/env python3
"""Verify review-evidence/977-r1/MANIFEST.json entries against the blobs at an evidence commit.
Usage: verify_manifest.py <repo> <commit> [prefix-filter]"""
import hashlib, json, subprocess, sys
repo, commit = sys.argv[1], sys.argv[2]
flt = sys.argv[3] if len(sys.argv) > 3 else ""
base = "review-evidence/977-r1/"
def show(p):
    return subprocess.run(["git", "-C", repo, "show", f"{commit}:{base}{p}"], capture_output=True, check=True).stdout
man = json.loads(show("MANIFEST.json"))
tree = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", commit, base], capture_output=True, text=True, check=True).stdout.split()
listed = {e["file"] for e in man}
ok = bad = 0
for e in man:
    if not e["file"].startswith(flt):
        continue
    h = hashlib.sha256(show(e["file"])).hexdigest()
    if h == e["published_sha256"]:
        ok += 1
    else:
        bad += 1; print("MISMATCH", e["file"])
unlisted = [p[len(base):] for p in tree if p[len(base):].startswith(flt) and p[len(base):] not in listed and p[len(base):] != "MANIFEST.json"]
for u in unlisted: print("UNLISTED", u)
print(f"commit={commit} filter='{flt}' ok={ok} mismatch={bad} unlisted={len(unlisted)}")
sys.exit(1 if bad or unlisted else 0)
