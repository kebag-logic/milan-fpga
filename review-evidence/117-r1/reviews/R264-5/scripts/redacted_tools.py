#!/usr/bin/env python3
"""List the redacted tool files of a pinned 117-r1 MANIFEST.json (original hash prefix, identity flag).

Usage: redacted_tools.py <MANIFEST.json>
"""
import json
import sys

for e in json.load(open(sys.argv[1])):
    if "/tools/" in e["file"] and e["original_sha256"] != e["published_sha256"]:
        print(e["file"], "identity_redacted=", e.get("identity_redacted", False), "orig", e["original_sha256"][:8])
