#!/usr/bin/env python3
"""Fetch named files of the published #803 evidence tree and check each
against the published MANIFEST.json sha256. usage: fetch_check.py <manifest>
<outdir> <relpath>...  Prints one line per file: OK/MISMATCH sha relpath."""
import hashlib, json, os, subprocess, sys

REF = "09a8771feb37f2c541fdbed05bd53c20f0fba60b"
BASE = "repos/kebag-logic/milan-fpga/contents/review-evidence/803-r1/"

man = {e["file"]: e for e in json.load(open(sys.argv[1]))}
out = sys.argv[2]
for rel in sys.argv[3:]:
    data = subprocess.run(["gh", "api", f"{BASE}{rel}?ref={REF}", "-H",
                           "Accept: application/vnd.github.raw"],
                          check=True, capture_output=True).stdout
    dst = os.path.join(out, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "wb").write(data)
    h = hashlib.sha256(data).hexdigest()
    exp = man.get(rel, {}).get("published_sha256")
    print("OK" if h == exp else "MISMATCH", h, rel)
