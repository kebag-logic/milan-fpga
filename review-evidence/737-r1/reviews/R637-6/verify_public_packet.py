#!/usr/bin/env python3
"""Verify selected public receipt bytes against their published manifest."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
p.add_argument("packet", type=Path)
a = p.parse_args()
ref = "26dd882d2011d55693da7791a89670ec9d517bd3:review-evidence/737-r1/"
manifest = json.loads(subprocess.check_output(["git", "show", ref + "MANIFEST.json"], cwd=a.repo))
selected = json.loads((a.packet / "receipts/published-hashes.json").read_text())
rows = []
for item in selected:
    source = next(row for row in manifest if row["file"] == item["file"])
    assert source == item
    published = subprocess.check_output(["git", "show", ref + item["file"]], cwd=a.repo)
    retained = (a.packet / "receipts/published" / item["file"]).read_bytes()
    digest = hashlib.sha256(retained).hexdigest()
    assert published == retained and digest == item["published_sha256"]
    rows.append(dict(path=item["file"], sha256=digest, verified=True))
result = dict(commit=ref.split(":")[0], receipts=rows,
              authentication="Digest bindings only; no packet signature supplied.")
(a.packet / "receipts/public-packet-verification.json").write_text(json.dumps(result, indent=2)+"\n")
print(f"PASS: {len(rows)} public receipts match their published manifest and Git blobs")
