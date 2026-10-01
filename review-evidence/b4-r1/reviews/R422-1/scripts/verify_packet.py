#!/usr/bin/env python3
"""Verify the published evidence packet against its manifests and the page.

usage: verify_packet.py <review-evidence/b4-r1 dir> <451_TDM8_TIMING_SOC_BOARD.md>

1. Every file in the archive MANIFEST.json hashes to its published_sha256;
   entries whose original and published hashes differ are listed (redactions).
2. author/MANIFEST.sha256 lines are checked; a mismatch is accepted only where
   the archive manifest records that file as redacted with original_sha256
   equal to the author manifest's hash.
3. Every evidence-file row of the page's hash table matches bytes and SHA-256.
"""
import hashlib
import json
import os
import re
import sys

root, page = sys.argv[1], sys.argv[2]
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
arch = json.load(open(os.path.join(root, "MANIFEST.json")))
bad = 0
red = {}
for e in arch:
    p = os.path.join(root, e["file"])
    if not os.path.exists(p) or h(p) != e["published_sha256"]:
        bad += 1
        print("ARCHIVE MISMATCH", e["file"])
    if e["original_sha256"] != e["published_sha256"]:
        red[e["file"]] = e["original_sha256"]
print(f"archive manifest: {len(arch)} entries, {bad} mismatches; redacted: {sorted(red)}")
am = os.path.join(root, "author", "MANIFEST.sha256")
ok = acc = fail = 0
for line in open(am):
    sha, rel = line.split(None, 1)
    rel = rel.strip().lstrip("*")
    p = os.path.join(root, "author", rel)
    if h(p) == sha:
        ok += 1
    elif red.get("author/" + rel) == sha:
        acc += 1
        print("author manifest: redacted, original hash recorded equal:", rel)
    else:
        fail += 1
        print("AUTHOR MANIFEST MISMATCH", rel)
print(f"author manifest: {ok} ok, {acc} redaction-accounted, {fail} unexplained")
rows = re.findall(r"^\| `([^`]+)`[^|]*\| ([0-9,]+) \| `([0-9a-f]{64})` \|", open(page).read(), re.M)
pf = 0
for rel, size, sha in rows:
    p = os.path.join(root, "author", rel)
    if not os.path.exists(p):
        print(f"page row {rel}: not in packet (raw artifact, held off-packet)")
        continue
    good = os.path.getsize(p) == int(size.replace(",", "")) and h(p) == sha
    pf += not good
    print(f"page row {rel}: {'OK' if good else 'MISMATCH'}")
print(f"page hash rows: {len(rows)}, mismatches {pf}")
sys.exit(1 if bad or fail or pf else 0)
