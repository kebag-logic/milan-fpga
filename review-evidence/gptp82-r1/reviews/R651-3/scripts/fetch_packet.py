#!/usr/bin/env python3
"""Fetch only the public author-r3 packet; validate each Git blob identity."""
import concurrent.futures, hashlib, json, pathlib, subprocess, sys, urllib.request
root = pathlib.Path(__file__).resolve().parents[1]
commit = "6f640b75f3ce16dd015ab8bd6363db1ea9ddffac"
repo = "kebag-logic/milan-fpga"
prefix = "review-evidence/gptp82-r1/"
tree = json.loads(subprocess.check_output(["gh", "api", f"repos/{repo}/git/trees/{commit}?recursive=1"]))
assert not tree.get("truncated")
files = [x for x in tree["tree"] if x["type"] == "blob" and (x["path"].startswith(prefix + "author-r3/") or x["path"] == prefix + "MANIFEST.json")]
out = root / "scratch/public"
def fetch(x):
    url = f"https://raw.githubusercontent.com/{repo}/{commit}/" + x["path"]
    data = urllib.request.urlopen(url, timeout=60).read()
    digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert digest == x["sha"], x["path"]
    p = out / x["path"][len(prefix):]
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    return {"path": str(p.relative_to(out)), "git_blob": digest, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    got = list(pool.map(fetch, files))
(root / "receipts/public-download.json").write_text(json.dumps({"commit": commit, "files": got}, indent=2) + "\n")
print(f"PASS {len(got)} public files match pinned Git blobs; no review reports fetched")
