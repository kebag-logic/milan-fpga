#!/usr/bin/env python3
"""Fetch and verify the public author packet; never reads reviewer reports."""
import concurrent.futures, hashlib, json, pathlib, subprocess
P = pathlib.Path(__file__).resolve().parent
REF = "c3f1d08d87370a2a06c6a8725c269f8bc7ab3071"
PREFIX = "review-evidence/gptp84-r1/"

def api(endpoint, raw=False):
    cmd = ["gh", "api", endpoint]
    if raw: cmd += ["-H", "Accept: application/vnd.github.raw+json"]
    return subprocess.check_output(cmd)

out = P / "public-evidence"
out.mkdir(exist_ok=True)
manifest_bytes = api(f"repos/kebag-logic/milan-fpga/contents/{PREFIX}MANIFEST.json?ref={REF}", True)
(out / "MANIFEST.json").write_bytes(manifest_bytes)
manifest = json.loads(manifest_bytes)
items = [x for x in manifest if x["file"].startswith("author-r2/")]

def fetch(x):
    data = api(f"repos/kebag-logic/milan-fpga/contents/{PREFIX}{x['file']}?ref={REF}", True)
    assert hashlib.sha256(data).hexdigest() == x["published_sha256"], x["file"]
    dest = out / x["file"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return x["file"]

with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    done = list(pool.map(fetch, items))
print(f"Published SHA-256 verified: {len(done)}/{len(items)} author-r2 files at {REF}")
commit = api(f"repos/kebag-logic/milan-fpga/commits/{REF}")
(out / "commit.json").write_bytes(commit)
v = json.loads(commit)["commit"]["verification"]
print("Evidence commit signature:", json.dumps(v))
