#!/usr/bin/env python3
"""Fetch only the assigned public evidence snapshot and verify its manifest."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request

PACKET = Path(__file__).resolve().parents[1]
PIN = "2e889399824b70f9ed9a20c53d925e61a617a976"
PREFIX = f"https://raw.githubusercontent.com/kebag-logic/milan-fpga/{PIN}/review-evidence/pp22-r1/"
manifest = json.loads((PACKET / "public/evidence-MANIFEST.json").read_text())

def fetch(row):
    name = row["file"]
    assert name.startswith("author/") and ".." not in name.split("/")
    data = urllib.request.urlopen(PREFIX + name, timeout=60).read()
    digest = hashlib.sha256(data).hexdigest()
    assert digest == row["published_sha256"], name
    dest = PACKET / "public/evidence" / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return {"file": name, "bytes": len(data), "sha256": digest, "verified": True}

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(fetch, manifest))
(PACKET / "receipts/public-evidence-integrity.json").write_text(json.dumps(results, indent=2) + "\n")
print(f"Verified {len(results)} public files at {PIN}")
