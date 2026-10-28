#!/usr/bin/env python3
"""Check every published file under <root> against MANIFEST.json entries
whose path starts with <prefix>; report missing, extra and mismatched."""
import hashlib, json, os, sys
root, prefix = sys.argv[1], sys.argv[2]
man = json.load(open(os.path.join(root, "MANIFEST.json")))
want = {e["file"]: e["published_sha256"] for e in man if e["file"].startswith(prefix)}
have = {}
for d, _, fs in os.walk(os.path.join(root, prefix)):
    for f in fs:
        p = os.path.join(d, f)
        have[os.path.relpath(p, root)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
bad = [k for k in want if k in have and have[k] != want[k]]
print(f"listed={len(want)} present={len(have)} missing={len(set(want)-set(have))} "
      f"unlisted={len(set(have)-set(want))} mismatched={len(bad)}")
for k in sorted(set(want)-set(have)): print("MISSING", k)
for k in sorted(set(have)-set(want)): print("UNLISTED", k)
for k in bad: print("MISMATCH", k)
redacted = [e["file"] for e in man if e["file"].startswith(prefix) and e["original_sha256"] != e["published_sha256"]]
print("redacted-content entries:", len(redacted)); [print("  ", r) for r in redacted]
sys.exit(1 if bad or (set(want)-set(have)) else 0)
