#!/usr/bin/env python3
"""Fetch named blobs of a public tree and verify each git blob id.
Usage: fetch_blobs.py <tree-listing> <outdir> <path-substring>...  (listing: type sha size path)"""
import base64, hashlib, json, subprocess, sys
from pathlib import Path
listing, out, keys = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
for line in listing.read_text().splitlines():
    kind, sha, _, path = line.split()
    if kind != "blob" or not any(k in path for k in keys):
        continue
    raw = subprocess.run(["gh", "api", f"repos/kebag-logic/milan-fpga/git/blobs/{sha}"],
                         check=True, capture_output=True).stdout
    data = base64.b64decode(json.loads(raw)["content"])
    ok = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() == sha
    dest = out / path.replace("review-evidence/763-r1/", "")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    print(f"{'OK ' if ok else 'BAD'} {sha} {hashlib.sha256(data).hexdigest()} {path}")
