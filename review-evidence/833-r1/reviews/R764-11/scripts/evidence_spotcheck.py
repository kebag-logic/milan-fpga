#!/usr/bin/env python3
"""Check downloaded author-r11 receipts against the evidence MANIFEST.json published_sha256.

Usage: python3 -I evidence_spotcheck.py <MANIFEST.json> <dir of files named path-with-/-as-_>
"""
import hashlib
import json
import os
import sys

manifest = {e["file"]: e for e in json.load(open(sys.argv[1]))}
for name in sorted(os.listdir(sys.argv[2])):
    key = "author-r11/" + name.replace("receipts_", "receipts/", 1).replace("item1_", "item1/") \
        .replace("item2_", "item2/").replace("final_", "final/")
    digest = hashlib.sha256(open(os.path.join(sys.argv[2], name), "rb").read()).hexdigest()
    entry = manifest.get(key)
    print("MATCH" if entry and entry["published_sha256"] == digest else "MISMATCH", key, digest[:16])
