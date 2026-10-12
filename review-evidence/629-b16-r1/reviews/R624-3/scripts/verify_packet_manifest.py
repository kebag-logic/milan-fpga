#!/usr/bin/env python3
"""Check the published evidence directory against its MANIFEST.json (each file's published_sha256) and the
author's round-3 MANIFEST.sha256 against the manifest's original_sha256 (the files the publication masked
are bound by both hashes).

usage: verify_packet_manifest.py <review-evidence/629-b16-r1 directory> <out.json>
"""
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
m = json.loads((ROOT / "MANIFEST.json").read_text())
bad = [e["file"] for e in m if hashlib.sha256((ROOT / e["file"]).read_bytes()).hexdigest() != e["published_sha256"]]
listed = {e["file"] for e in m}
on_disk = {os.path.relpath(os.path.join(r, f), ROOT) for r, _, fs in os.walk(ROOT) for f in fs} - {"MANIFEST.json"}
orig = {}
for line in (ROOT / "author-r3/MANIFEST.sha256").read_text().splitlines():
    h, p = line.split(None, 1)
    orig[p.strip().lstrip("*").removeprefix("./")] = h
mm = {e["file"].removeprefix("author-r3/"): e for e in m if e["file"].startswith("author-r3/")}
r3_mismatch = [p for p, h in orig.items() if p not in mm or mm[p]["original_sha256"] != h]
out = dict(entries=len(m), published_mismatch=bad, unlisted=sorted(on_disk - listed), missing=sorted(listed - on_disk),
           path_redacted=sum(e["path_redacted"] for e in m),
           author_r3_manifest_entries=len(orig), author_r3_vs_original_mismatch=r3_mismatch,
           author_r3_redacted=sorted(p for p, e in mm.items() if e["path_redacted"]))
OUT.write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in out.items()}))
sys.exit(1 if bad or r3_mismatch or out["unlisted"] or out["missing"] else 0)
