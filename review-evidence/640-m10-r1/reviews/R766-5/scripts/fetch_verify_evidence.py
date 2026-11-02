#!/usr/bin/env python3
"""Fetch a published evidence subtree by git blob id and verify it.

Usage: fetch_verify_evidence.py TREE_JSON OUTDIR PREFIX [PREFIX ...]

TREE_JSON is the recursive git tree of the evidence commit (gh api
.../git/trees/<sha>?recursive=1).  Every blob under each PREFIX is fetched
read-only with `gh api .../git/blobs/<sha>`, its git blob id is recomputed,
and MANIFEST.json's published_sha256 is checked for each fetched file.
"""
import base64
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys

REPO = "repos/kebag-logic/milan-fpga"
ROOT = "review-evidence/640-m10-r1/"


def fetch(entry, outdir):
    raw = subprocess.run(["gh", "api", f"{REPO}/git/blobs/{entry['sha']}"],
                         check=True, capture_output=True).stdout
    data = base64.b64decode(json.loads(raw)["content"])
    gid = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    rel = entry["path"][len(ROOT):]
    dst = os.path.join(outdir, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(data)
    return rel, gid == entry["sha"], hashlib.sha256(data).hexdigest()


def main():
    tree_json, outdir, prefixes = sys.argv[1], sys.argv[2], sys.argv[3:]
    tree = json.load(open(tree_json))["tree"]
    want = [e for e in tree if e["type"] == "blob" and e["path"].startswith(ROOT)
            and any(e["path"][len(ROOT):].startswith(p) for p in prefixes)]
    with concurrent.futures.ThreadPoolExecutor(16) as ex:
        res = list(ex.map(lambda e: fetch(e, outdir), want))
    bad_gid = [r for r, ok, _ in res if not ok]
    man = json.load(open(os.path.join(outdir, "MANIFEST.json")))
    entries = man if isinstance(man, list) else man.get("files", man.get("entries", []))
    bypath = {e.get("path", e.get("file")): e for e in entries}
    mism, unlisted = [], []
    for rel, _, sha in res:
        if rel == "MANIFEST.json":
            continue
        e = bypath.get(rel)
        if e is None:
            unlisted.append(rel)
        elif e.get("published_sha256") != sha:
            mism.append(rel)
    print(f"fetched {len(res)} blobs; blob-id mismatches {len(bad_gid)}")
    print(f"manifest entries {len(entries)}; checked {len(res) - 1}; "
          f"published_sha256 mismatches {len(mism)}; unlisted {len(unlisted)}")
    for x in bad_gid + mism + unlisted:
        print("  ", x)
    return 1 if (bad_gid or mism or unlisted) else 0


if __name__ == "__main__":
    sys.exit(main())
