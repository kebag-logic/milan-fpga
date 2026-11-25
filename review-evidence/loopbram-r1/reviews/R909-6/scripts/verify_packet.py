#!/usr/bin/env python3
"""Check every author-r7 file at an evidence commit against the evidence MANIFEST.json's sha256 fields."""
import hashlib, json, subprocess, sys
repo, commit, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
git = lambda *a: subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True).stdout
man = json.loads(git("show", f"{commit}:review-evidence/loopbram-r1/MANIFEST.json"))
entries = {}
for e in man:
    path = e.get("path") or e.get("published_path") or e.get("file")
    if path and prefix in path:
        entries[path] = e
files = [l for l in git("ls-tree", "-r", "--name-only", commit, f"review-evidence/loopbram-r1/{prefix}").decode().splitlines()]
bad = 0
for f in files:
    data = git("show", f"{commit}:{f}")
    h = hashlib.sha256(data).hexdigest()
    rel = f.split("review-evidence/loopbram-r1/", 1)[1]
    e = entries.get(f) or entries.get(rel)
    want = e and (e.get("published_sha256") or e.get("sha256"))
    ok = want == h
    bad += not ok
    print(("ok  " if ok else "BAD ") + h[:16] + " " + rel)
print(f"files={len(files)} manifest_entries={len(entries)} bad={bad}")
sys.exit(1 if bad else 0)
