#!/usr/bin/env python3
"""Verify an author packet's INDEX.md rows and the archive MANIFEST.json rows against file bytes.
Usage: verify_packet.py <archive-root> <subdir>"""
import hashlib, json, os, re, sys
root, sub = sys.argv[1], sys.argv[2]
bad = 0; n = 0
idx = open(os.path.join(root, sub, "INDEX.md"), encoding="utf-8").read()
for m in re.finditer(r"^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|$", idx, re.M):
    n += 1
    p = os.path.join(root, sub, m.group(1))
    b = open(p, "rb").read()
    ok = hashlib.sha256(b).hexdigest() == m.group(3) and len(b) == int(m.group(2).replace(",", ""))
    if not ok:
        bad += 1; print("INDEX MISMATCH", m.group(1))
listed = {m.group(1) for m in re.finditer(r"^\| `([^`]+)` \|", idx, re.M)}
present = set()
for d, _, fs in os.walk(os.path.join(root, sub)):
    for f in fs:
        rel = os.path.relpath(os.path.join(d, f), os.path.join(root, sub))
        if rel != "INDEX.md": present.add(rel)
print("index rows", n, "mismatch", bad, "unlisted", sorted(present - listed), "missing", sorted(listed - present))
man = json.load(open(os.path.join(root, "MANIFEST.json")))
mb = 0; mn = 0
for e in man:
    if not e["file"].startswith(sub + "/"): continue
    mn += 1
    b = open(os.path.join(root, e["file"]), "rb").read()
    if hashlib.sha256(b).hexdigest() != e["published_sha256"]:
        mb += 1; print("MANIFEST MISMATCH", e["file"])
print("manifest rows for", sub, mn, "mismatch", mb)
