#!/usr/bin/env python3
"""Read selected published gate receipts, verifying their pinned Git blob IDs."""
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parents[1]
tree = json.loads((packet / "receipts/public-evidence-tree.json").read_text())
prefix = "review-evidence/pp167-r1/author-r2/round2/"
names = ["area-comparison.json", "count-two-proof.json", "evidence-index.json",
         "final-receipts.json", "probe-proof.json", "record-comparison.json",
         "round1-record-comparison.json", "scope-proof.json", "suite-comparison.json",
         "processor-static-comparison.json", "parent-comparison.json",
         "plant-base.json", "plant-head.json", "campaign-notify-artifacts.json"]
out = packet / "receipts/public-author"
out.mkdir(exist_ok=True)
def fetch(name):
    entry = next(x for x in tree["tree"] if x["path"] == prefix + name)
    raw = subprocess.check_output(["gh", "api", "repos/kebag-logic/milan-fpga/git/blobs/" + entry["sha"]])
    data = base64.b64decode(json.loads(raw)["content"])
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual == entry["sha"]
    (out / name).write_bytes(data)
    return {"path": prefix + name, "git_blob": actual, "sha256": hashlib.sha256(data).hexdigest()}
with ThreadPoolExecutor(max_workers=4) as pool:
    records = list(pool.map(fetch, names))
(packet / "receipts/public-evidence-integrity.json").write_text(json.dumps(records, indent=2) + "\n")
print(f"Verified {len(records)} published author receipts at {tree['sha']}")
