#!/usr/bin/env python3
"""Re-hash every file a published review-evidence packet lists in its MANIFEST.json.

usage: verify_packet_manifest.py <review-evidence/629-tone-r1 dir>

Prints the count of entries, mismatches against published_sha256, and the entries whose published bytes
differ from the lane packet's original (a redaction), then exits 1 on any mismatch.
"""
import hashlib
import json
import os
import sys

d = sys.argv[1]
m = json.load(open(os.path.join(d, "MANIFEST.json")))
bad, red = 0, []
for e in m:
    h = hashlib.sha256(open(os.path.join(d, e["file"]), "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        bad += 1
        print("MISMATCH", e["file"])
    if e["original_sha256"] != e["published_sha256"] or e.get("path_redacted"):
        red.append(e["file"])
print(f"entries {len(m)}, mismatches {bad}, redacted after the lane packet: {red}")
sys.exit(1 if bad else 0)
