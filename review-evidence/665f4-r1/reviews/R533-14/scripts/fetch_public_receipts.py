#!/usr/bin/env python3
"""Download only the named public author receipts, never review reports."""
import concurrent.futures
import hashlib
import json
import pathlib
import urllib.request

PACKET = pathlib.Path(__file__).resolve().parents[1]
REV = "2276e34a9a7a615cdf65b4e6c026129680ede1f9"
PREFIX = "review-evidence/665f4-r1/author-r14/"
RAW = "https://raw.githubusercontent.com/kebag-logic/milan-fpga/"
scratch = PACKET / "scratch"
scratch.mkdir(exist_ok=True)
tree_path = scratch / "evidence-tree.json"
if not tree_path.exists():
    url = f"https://api.github.com/repos/kebag-logic/milan-fpga/git/trees/{REV}?recursive=1"
    tree_path.write_bytes(urllib.request.urlopen(url, timeout=45).read())
tree = json.loads(tree_path.read_text())
assert not tree.get("truncated"), "Public tree inventory is incomplete"
entries = [x for x in tree["tree"] if x["type"] == "blob" and x["path"].startswith(PREFIX)
           and ("/" not in x["path"][len(PREFIX):]
                or x["path"][len(PREFIX):].startswith(("round14-receipts/", "round14-helpers/")))]

def get(entry):
    relative = entry["path"][len(PREFIX):]
    url = RAW + REV + "/" + entry["path"]
    data = urllib.request.urlopen(url, timeout=45).read()
    oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert oid == entry["sha"], relative
    dest = PACKET / "scratch/public-author-r14" / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return {"path": relative, "url": url, "git_blob": oid,
            "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(get, entries))
(PACKET / "receipts/public-author-receipt-hashes.json").write_text(
    json.dumps({"public_commit": REV, "files": results}, indent=2) + "\n")
print(f"PASS: {len(results)} public author files match their published Git blobs")

dev = "17f62ef64a66562384e8a93b1d6be6f86e51f95c"
data = urllib.request.urlopen(RAW + dev + "/scripts/act_ci.py", timeout=45).read()
(PACKET / "scratch/live-dev-act_ci.py").write_bytes(data)
print("Read trusted-base source as inert bytes; SHA256=" + hashlib.sha256(data).hexdigest())
url = RAW + REV + "/review-evidence/665f4-r1/MANIFEST.json"
(scratch / "evidence-manifest.json").write_bytes(urllib.request.urlopen(url, timeout=45).read())
