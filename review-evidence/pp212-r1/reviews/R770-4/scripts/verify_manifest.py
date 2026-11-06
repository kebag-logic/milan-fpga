#!/usr/bin/env python3
"""Check MANIFEST.json published_sha256 against blobs at an evidence commit.
Usage: verify_manifest.py <repo> <commit> <dir> [prefix-filter]"""
import hashlib, json, subprocess, sys
repo, rev, d = sys.argv[1:4]
flt = sys.argv[4] if len(sys.argv) > 4 else ""
m = json.loads(subprocess.run(["git", "-C", repo, "show", f"{rev}:{d}/MANIFEST.json"], capture_output=True, check=True).stdout)
ls = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev, "--", d], capture_output=True, text=True, check=True).stdout.split()
tree = {p[len(d) + 1:] for p in ls} - {"MANIFEST.json"}
listed = {e["file"] for e in m}
bad = 0; n = 0
for e in m:
    if not e["file"].startswith(flt):
        continue
    n += 1
    b = subprocess.run(["git", "-C", repo, "show", f"{rev}:{d}/{e['file']}"], capture_output=True).stdout
    h = hashlib.sha256(b).hexdigest()
    if h != e["published_sha256"]:
        bad += 1; print("MISMATCH", e["file"])
    if e["original_sha256"] != e["published_sha256"] and not e.get("path_redacted"):
        print("NOTE redacted-content", e["file"])
unl = sorted(p for p in tree - listed if p.startswith(flt))
print(f"checked {n} entries under '{flt}': {bad} mismatches; unlisted files: {len(unl)}")
for p in unl: print("UNLISTED", p)
sys.exit(1 if bad or unl else 0)
