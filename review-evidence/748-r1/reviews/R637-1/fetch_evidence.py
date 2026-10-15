#!/usr/bin/env python3
"""Fetch only the published author receipts and verify their published digests."""
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parent
REV = "9ae6b8b2e900a3c6d076a2eb345916231515f045"
def fetch(row):
    name = row["file"]
    data = json.loads(subprocess.check_output(["gh", "api", f"repos/kebag-logic/milan-fpga/contents/review-evidence/748-r1/{name}?ref={REV}"]))
    blob = base64.b64decode(data["content"])
    digest = hashlib.sha256(blob).hexdigest()
    assert digest == row["published_sha256"], name
    target = ROOT / "public-evidence" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(blob)
    return f"PASS {digest} {name}"
rows = [r for r in json.loads((ROOT / "author-MANIFEST.json").read_text()) if r["file"].startswith("author/evidence/")]
with ThreadPoolExecutor(max_workers=6) as pool:
    lines = list(pool.map(fetch, rows))
report = "\n".join(lines) + "\n"
(ROOT / "evidence-fetch.log").write_text(report)
print(report)
