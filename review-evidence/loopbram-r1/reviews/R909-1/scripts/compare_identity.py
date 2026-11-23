#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Compare base and head identity.json: every default artifact must be
byte-identical; the enabled control must differ. Exit 1 on any mismatch."""
import json
import sys
from pathlib import Path

base = json.loads(Path(sys.argv[1]).read_text())
head = json.loads(Path(sys.argv[2]).read_text())
bad = 0
for key, b in sorted(base.items()):
    h = head[key]
    same_files = b["files"] == h["files"]
    same = same_files and b["aem_image_sha256"] == h["aem_image_sha256"] and b["argv"] == h["argv"] \
        and b["model_id"] == h["model_id"]
    print(f"{key}: {len(b['files'])} artifacts, image {b['aem_image_bytes']} B, "
          f"{'IDENTICAL' if same else 'DIFFERENT'}")
    if not same_files:
        for f in sorted(set(b["files"]) | set(h["files"])):
            if b["files"].get(f) != h["files"].get(f):
                print("   differs:", f)
    bad += not same
for key, h in sorted(head.items()):
    if key.endswith("/enabled"):
        d = head[key.replace("/enabled", "/default")]
        changed = sorted(f for f in h["files"] if h["files"][f] != d["files"].get(f))
        print(f"{key}: control differs from default in {len(changed)} artifacts; image "
              f"{d['aem_image_bytes']} -> {h['aem_image_bytes']} B; flag in argv: "
              f"{'--input-loopback-lane' in h['argv']}")
        bad += not changed
print("IDENTITY", "FAIL" if bad else "PASS")
raise SystemExit(1 if bad else 0)
