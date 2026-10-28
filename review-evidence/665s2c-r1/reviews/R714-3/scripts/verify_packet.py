#!/usr/bin/env python3
"""Check downloaded files of the author's round-3 packet against the packet's MANIFEST.json.

Usage: python3 -I verify_packet.py <MANIFEST.json> <directory holding author-r3 files>
Prints OK or MISMATCH per file; exits 1 on any mismatch or unlisted file.
"""
import hashlib
import json
import os
import sys

manifest = {e["file"]: e["published_sha256"] for e in json.load(open(sys.argv[1]))}
bad = 0
for root, _, files in os.walk(sys.argv[2]):
    for name in sorted(files):
        path = os.path.join(root, name)
        key = "author-r3/" + os.path.relpath(path, sys.argv[2])
        digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
        state = "OK" if manifest.get(key) == digest else "MISMATCH"
        bad += state != "OK"
        print(state, key)
sys.exit(1 if bad else 0)
