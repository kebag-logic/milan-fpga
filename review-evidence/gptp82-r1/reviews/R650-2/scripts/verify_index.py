#!/usr/bin/env python3
"""Check a RECEIPTS.md table (| `path` | bytes | `sha256` | ...) against a
directory: every listed in-directory file exists with those bytes and sha256,
and every file in the directory except the index is listed. Optionally check
MANIFEST.json entries (path/sha256/size) under a given prefix."""
import hashlib, json, os, re, sys
d = sys.argv[1]
rows = {}
oot = []
for line in open(os.path.join(d, "RECEIPTS.md"), encoding="utf-8"):
    m = re.match(r"\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*`([0-9a-f]{64})`", line)
    if m:
        rows[m.group(1)] = (int(m.group(2)), m.group(3))
bad = 0
present = set()
for root, _, files in os.walk(d):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), d)
        if rel != "RECEIPTS.md":
            present.add(rel)
for rel, (n, h) in sorted(rows.items()):
    p = os.path.join(d, rel)
    if not os.path.isfile(p):
        oot.append(rel); continue
    b = open(p, "rb").read()
    hh = hashlib.sha256(b).hexdigest()
    if len(b) != n or hh != h:
        bad += 1; print("MISMATCH", rel, n, len(b), h, hh)
unlisted = sorted(present - set(rows))
for u in unlisted:
    bad += 1; print("UNLISTED", u)
print(f"rows={len(rows)} in_dir_checked={len(rows)-len(oot)} not_in_dir={len(oot)} files={len(present)} bad={bad}")
for o in oot: print("NOT-IN-DIR", o)
if len(sys.argv) > 3:
    man, prefix = sys.argv[2], sys.argv[3]
    ents = json.load(open(man))
    root = os.path.dirname(man)
    k = 0; mb = 0
    for e in ents:
        p = e.get("path") or e.get("file")
        if not p or not p.startswith(prefix): continue
        k += 1
        b = open(os.path.join(root, p), "rb").read()
        if hashlib.sha256(b).hexdigest() != (e.get("published_sha256") or e.get("sha256")) or ("size" in e and e["size"] != len(b)) or ("bytes" in e and e["bytes"] != len(b)):
            mb += 1; print("MANIFEST-MISMATCH", p)
    print(f"manifest entries under {prefix}: {k}, mismatches {mb}")
sys.exit(1 if bad else 0)
