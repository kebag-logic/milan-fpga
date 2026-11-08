#!/usr/bin/env python3
"""Check author-r6 receipts: published bytes vs MANIFEST.json published_sha256,
and author SHA256SUMS vs MANIFEST.json original_sha256 (pre-redaction digests).
usage: verify_author_r6.py <MANIFEST.json> <extracted 640-m10-r1 dir> <subdir>"""
import hashlib, json, os, sys
man, root, sub = sys.argv[1], sys.argv[2], sys.argv[3]
ents = {e["file"]: e for e in json.load(open(man)) if e["file"].startswith(sub + "/")}
sums = {}
for ln in open(os.path.join(root, sub, "evidence", "SHA256SUMS")):
    h, p = ln.rstrip("\n").split(None, 1)
    sums[sub + "/" + p.lstrip("*").removeprefix("./")] = h
on_disk = set()
for d, _, fs in os.walk(os.path.join(root, sub)):
    for f in fs:
        on_disk.add(os.path.relpath(os.path.join(d, f), root))
bad = 0
for f in sorted(on_disk):
    e = ents.get(f)
    h = hashlib.sha256(open(os.path.join(root, f), "rb").read()).hexdigest()
    if e is None:
        if f.endswith("SHA256SUMS"): print("UNLISTED-IN-MANIFEST (sums file)", f); continue
        print("UNLISTED", f); bad += 1; continue
    if e["published_sha256"] != h: print("PUBLISHED-MISMATCH", f); bad += 1
for f, e in sorted(ents.items()):
    if f not in on_disk: print("MANIFEST-ONLY (not published)", f, "redacted=", e.get("path_redacted"))
    s = sums.get(f)
    if s is None:
        if not f.endswith("SHA256SUMS"): print("NOT-IN-SUMS", f)
    elif s != e["original_sha256"]: print("ORIGINAL-MISMATCH", f); bad += 1
for f in sorted(set(sums) - set(ents)): print("SUMS-ONLY", f)
n_red = sum(1 for e in ents.values() if e["published_sha256"] != e["original_sha256"])
print(f"manifest entries {len(ents)}, published files {len(on_disk)}, sums {len(sums)}, redacted-bytes {n_red}, failures {bad}")
sys.exit(1 if bad else 0)
