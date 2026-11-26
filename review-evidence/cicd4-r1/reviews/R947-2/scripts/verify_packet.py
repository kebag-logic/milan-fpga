#!/usr/bin/env python3
"""Verify every file of an extracted evidence packet against its MANIFEST.json. Usage: verify_packet.py PACKET_DIR"""
import hashlib, json, os, sys
d = sys.argv[1]; m = json.load(open(os.path.join(d, "MANIFEST.json")))
bad = [e["file"] for e in m if hashlib.sha256(open(os.path.join(d, e["file"]), "rb").read()).hexdigest() != e["published_sha256"]]
red = [e["file"] for e in m if e["path_redacted"] or e["original_sha256"] != e["published_sha256"]]
have = {os.path.relpath(os.path.join(r, f), d) for r, _, fs in os.walk(d) for f in fs} - {"MANIFEST.json"}
listed = {e["file"] for e in m}
print(f"entries {len(m)} mismatched {bad} unlisted {sorted(have - listed)} missing {sorted(listed - have)}")
print(f"path-redacted entries (published differs from original by redaction): {red}")
sys.exit(1 if bad or have - listed or listed - have else 0)
