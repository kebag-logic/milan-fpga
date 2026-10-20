#!/usr/bin/env python3
"""Fetch only public round-two execution receipts, verify publication hashes."""
import base64
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parent
REV = "bf51200d95edd1d371b269f6e3b459036dc2d891"
manifest = json.loads((ROOT / "published-manifest.json").read_text())
prefixes = tuple("author-r2/receipts/" + x + "/" for x in
                 ("r2-rxmon", "r2-tsnfuzz", "r2-regen", "r2-static", "r2-builder"))
rows = [x for x in manifest if x["file"].startswith(prefixes)]
def fetch(row):
    rel = row["file"]
    target = ROOT / "published" / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        url = "repos/kebag-logic/milan-fpga/contents/review-evidence/765-r1/" + rel + "?ref=" + REV
        data = subprocess.check_output(["gh", "api", url])
        payload = json.loads(data)
        if payload.get("content"):
            target.write_bytes(base64.b64decode(payload["content"]))
        else:
            blob = json.loads(subprocess.check_output(["gh", "api", payload["git_url"]]))
            target.write_bytes(base64.b64decode(blob["content"]))
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    assert actual == row["published_sha256"], rel
    return {"file": rel, "sha256": actual, "published_hash_matches": True,
            "path_redacted": row["path_redacted"]}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    checks = list(pool.map(fetch, rows))
(ROOT / "publication-hash-check.json").write_text(json.dumps(checks, indent=2) + "\n")
print("PASS:", len(checks), "public execution receipts match published_sha256 at", REV)
