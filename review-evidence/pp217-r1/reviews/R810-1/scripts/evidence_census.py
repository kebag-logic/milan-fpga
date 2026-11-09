#!/usr/bin/env python3
"""evidence_census.py <packet-root>: every MANIFEST.json entry is present with its published sha256."""
import hashlib, json, os, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
missing, bad = [], []
for e in m:
    fp = os.path.join(root, e["file"])
    if not os.path.isfile(fp):
        missing.append(e["file"]); continue
    if hashlib.sha256(open(fp, "rb").read()).hexdigest() != e["published_sha256"]:
        bad.append(e["file"])
on_disk = sum(len(f) for _, _, f in os.walk(root))
print(f"manifest entries {len(m)}, files on disk {on_disk} (incl. MANIFEST.json), missing {len(missing)}, sha256 mismatches {len(bad)}")
for p in missing: print("MISSING", p)
for p in bad: print("BADSHA", p)
for d in ("author/receipts/proc", "author/receipts/twin", "author/receipts/repro-base", "author/receipts/parent", "author/tools"):
    n = sum(len(f) for _, _, f in os.walk(os.path.join(root, d)))
    print(f"{d}: {n} files")
sys.exit(1 if missing or bad else 0)
