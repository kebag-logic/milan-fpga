#!/usr/bin/env python3
"""Compare an OOC inputs.json (path -> sha256) against a git revision's blobs."""
import hashlib, json, subprocess, sys
repo, rev, path = sys.argv[1], sys.argv[2], sys.argv[3]
data = json.load(open(path))
files = {k: v for k, v in data.items() if isinstance(v, str) and len(v) == 64}
bad = 0
for rel, digest in sorted(files.items()):
    try:
        blob = subprocess.run(["git", "-C", repo, "show", f"{rev}:{rel}"], capture_output=True, check=True).stdout
    except subprocess.CalledProcessError:
        print("MISSING", rel); bad += 1; continue
    if hashlib.sha256(blob).hexdigest() != digest:
        print("DIFF", rel); bad += 1
tracked = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev, "hdl/"], capture_output=True, text=True).stdout.split()
extra = [t for t in tracked if t not in files]
print(f"{rev}: {len(files)} hashed inputs, {bad} mismatches; tracked hdl files not in inputs: {len(extra)} {extra[:5]}")
sys.exit(1 if bad else 0)
