#!/usr/bin/env python3
"""Download and hash public receipts, without opening any reviewer report."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys

packet = Path(sys.argv[1]).resolve()
revision = "c262f8de6c498f412312ad3abd96437c9d25e594"
prefix = "review-evidence/763-r1/"
(packet / "scratch").mkdir(parents=True, exist_ok=True)
for name, endpoint, raw in (
    ("public-manifest.json", f"contents/{prefix}MANIFEST.json?ref={revision}", True),
    ("evidence-tree.json", f"git/trees/{revision}?recursive=1", False),
):
    destination = packet / "scratch" / name
    if not destination.exists():
        args = ["gh", "api"]
        if raw:
            args += ["-H", "Accept: application/vnd.github.raw+json"]
        destination.write_bytes(subprocess.check_output(
            args + ["repos/kebag-logic/milan-fpga/" + endpoint]))
manifest = json.loads((packet / "scratch/public-manifest.json").read_text())
tree = json.loads((packet / "scratch/evidence-tree.json").read_text())
assert not tree["truncated"]
actual = {x["path"][len(prefix):] for x in tree["tree"]
          if x["path"].startswith(prefix) and x["type"] == "blob"}
expected = {x["file"] for x in manifest} | {"MANIFEST.json"}
assert actual == expected, (actual - expected, expected - actual)

def fetch(row):
    path = row["file"]
    if not path.startswith("author/receipts/"):
        return {"file": path, "read": False}
    data = subprocess.check_output(["gh", "api", "-H", "Accept: application/vnd.github.raw+json",
        f"repos/kebag-logic/milan-fpga/contents/{prefix}{path}?ref={revision}"])
    out = packet / "scratch/public" / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    assert digest == row["published_sha256"], path
    return {"file": path, "read": True, "sha256": digest, "bytes": len(data)}

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(fetch, manifest))
(packet / "public-hash-audit.json").write_text(json.dumps({"revision": revision,
    "tree_membership_equal": True, "files": results}, indent=2) + "\n")
print("Public manifest exactly matches published files:", len(manifest))
print("Receipt hashes verified:", sum(r["read"] for r in results))
