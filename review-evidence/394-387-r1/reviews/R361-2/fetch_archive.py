#!/usr/bin/env python3
"""Fetch review-evidence/394-387-r1 at a pinned commit and verify each blob.

Usage: fetch_archive.py <commit> <out_dir>
Reads the commit's recursive tree through the read-only GitHub API, downloads
every blob under review-evidence/394-387-r1/, and refuses any blob whose bytes
do not hash to its git object id. Prints one line per file (git id, bytes,
path) and a total. Exit 1 on any mismatch.
"""
import base64
import hashlib
import json
import os
import subprocess
import sys

REPO = "kebag-logic/milan-fpga"
PREFIX = "review-evidence/394-387-r1/"


def api(path):
    return json.loads(subprocess.run(["gh", "api", path], check=True,
                                     capture_output=True).stdout)


def main() -> int:
    commit, out = sys.argv[1:3]
    tree = api(f"repos/{REPO}/git/trees/{commit}?recursive=1")
    if tree["truncated"]:
        print("tree truncated")
        return 1
    n = 0
    for e in tree["tree"]:
        if e["type"] != "blob" or not e["path"].startswith(PREFIX):
            continue
        data = base64.b64decode(api(f"repos/{REPO}/git/blobs/{e['sha']}")["content"])
        if hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() != e["sha"]:
            print(f"MISMATCH {e['path']}")
            return 1
        dest = os.path.join(out, e["path"][len(PREFIX):])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(data)
        n += 1
        print(f"{e['sha']} {len(data)} {e['path']}")
    print(f"fetched and git-id verified: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
