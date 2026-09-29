#!/usr/bin/env python3
"""Check an evidence archive's publisher MANIFEST.json against the published bytes.

usage: archive_manifest.py <label>=<review-evidence/b1-r1 dir> [...]
"""
import hashlib
import json
import sys
from pathlib import Path

bad = 0
for spec in sys.argv[1:]:
    label, root = spec.split("=", 1)
    root = Path(root)
    entries = json.loads((root / "MANIFEST.json").read_text())
    ok = sum(1 for x in entries if (root / x["file"]).is_file()
             and hashlib.sha256((root / x["file"]).read_bytes()).hexdigest() == x["published_sha256"])
    changed = sum(1 for x in entries if x["original_sha256"] != x["published_sha256"])
    listed = {x["file"] for x in entries}
    extra = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()} - listed - {"MANIFEST.json"}
    print(f"{label}: {len(entries)} entries, {ok} match their published SHA-256, "
          f"{changed} path-redacted by the archiver, {len(extra)} files outside the manifest")
    bad += ok != len(entries) or bool(extra)
sys.exit(1 if bad else 0)
