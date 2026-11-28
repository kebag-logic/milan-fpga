#!/usr/bin/env python3
"""Verify the author packet against its MANIFEST.json and compare base/head firmware manifests.

Usage: verify_packet.py <dir containing MANIFEST.json and author/>
"""
import collections
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
entries = json.loads((root / "MANIFEST.json").read_text())
listed, bad = set(), 0
for e in entries:
    data = (root / e["file"]).read_bytes()
    ok = hashlib.sha256(data).hexdigest() == e["published_sha256"]
    bad += not ok
    listed.add(e["file"])
    print(f"{'OK ' if ok else 'BAD'} {e['file']}")
present = {str(p.relative_to(root)) for p in (root / "author").rglob("*") if p.is_file()}
print(f"listed {len(listed)} present {len(present)} unlisted {sorted(present - listed)} "
      f"missing {sorted(listed - present)} bad {bad}")
fw = root / "author/receipts/firmware"
for tree in ("dsc", "dev"):
    b = (fw / f"{tree}-base.manifest.tsv").read_bytes()
    h = (fw / f"{tree}-head.manifest.tsv").read_bytes()
    kinds = collections.Counter(line.split(b"\t")[0].decode() for line in h.splitlines() if line)
    print(f"firmware {tree}: base==head {b == h}; sha256 {hashlib.sha256(h).hexdigest()[:16]}; {dict(kinds)}")
