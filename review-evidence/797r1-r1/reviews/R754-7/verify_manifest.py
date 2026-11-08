#!/usr/bin/env python3
"""Verify every published_sha256 in an evidence MANIFEST.json against the blobs at one commit.
Usage (from a clone holding the commit): python3 -I verify_manifest.py <commit> <evidence-dir> [prefix]"""
import hashlib, json, subprocess, sys
commit, base = sys.argv[1], sys.argv[2].rstrip("/")
prefix = sys.argv[3] if len(sys.argv) > 3 else ""
show = lambda p: subprocess.run(["git", "show", f"{commit}:{p}"], capture_output=True).stdout
m = json.loads(show(f"{base}/MANIFEST.json"))
listed = {e["file"] for e in m}
tree = set(subprocess.run(["git", "ls-tree", "-r", "--name-only", commit, "--", f"{base}/{prefix}"],
                          capture_output=True, text=True).stdout.split())
tree = {t[len(base) + 1:] for t in tree}
bad = checked = 0
for e in m:
    if not e["file"].startswith(prefix):
        continue
    checked += 1
    if hashlib.sha256(show(f"{base}/{e['file']}")).hexdigest() != e["published_sha256"]:
        bad += 1
        print("MISMATCH", e["file"])
unlisted = sorted(tree - listed - {"MANIFEST.json"})
print(f"checked {checked} entries under {prefix or '<all>'}: {bad} mismatches; "
      f"{len(unlisted)} files in tree not listed{': ' + ', '.join(unlisted[:10]) if unlisted else ''}")
sys.exit(1 if bad or unlisted else 0)
