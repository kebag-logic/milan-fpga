#!/usr/bin/env python3
"""Fetch and verify only the pinned public author receipts."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
ref = "b71327c650cd5a941ebbb73e64695650a21861cb"
prefix = "repos/kebag-logic/milan-fpga/contents/review-evidence/gptp96-r1/"

def get(relative):
    return subprocess.check_output(["gh", "api", prefix + relative + "?ref=" + ref,
                                    "-H", "Accept: application/vnd.github.raw+json"])

raw = get("MANIFEST.json")
manifest_path = packet / "scratch/public-MANIFEST.json"
manifest_path.parent.mkdir(parents=True, exist_ok=True)
manifest_path.write_bytes(raw)
entries = [entry for entry in json.loads(raw)
           if entry["file"].startswith("author-r4/receipts/")]

def verify(entry):
    relative = entry["file"]
    data = get(relative)
    target = packet / "scratch/public" / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    return dict(path=relative, expected=entry["published_sha256"], actual=digest,
                ok=digest == entry["published_sha256"])

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as workers:
    results = list(workers.map(verify, entries))
(packet / "receipts").mkdir(exist_ok=True)
(packet / "receipts/public-digests.json").write_text(json.dumps(results, indent=2) + "\n")
assert all(result["ok"] for result in results)
print(f"Verified {len(results)} pinned public receipts.")
