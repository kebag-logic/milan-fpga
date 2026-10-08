#!/usr/bin/env python3
"""Fetch only the immutable, public pp167-r1 evidence tree; verify blob identity."""
import base64, concurrent.futures, hashlib, json, pathlib, subprocess
packet = pathlib.Path(__file__).resolve().parents[1]
entries = json.loads((packet / "public/evidence-tree.json").read_text())
def fetch(e):
    if e["type"] != "blob": return None
    raw = subprocess.check_output(["gh", "api", "repos/kebag-logic/milan-fpga/git/blobs/" + e["sha"]])
    data = base64.b64decode(json.loads(raw)["content"])
    digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert digest == e["sha"], e["path"]
    dest = packet / "public/evidence" / e["path"].removeprefix("review-evidence/pp167-r1/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return {"path": e["path"], "blob": digest, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    rows = [r for r in pool.map(fetch, entries) if r is not None]
(packet / "receipts/public-evidence-integrity.json").write_text(json.dumps(rows, indent=2) + "\n")
print(f"Verified {len(rows)} public blobs at 93a14a4ce6b5a74ae166b6f33e52045efe9fe0b7")
