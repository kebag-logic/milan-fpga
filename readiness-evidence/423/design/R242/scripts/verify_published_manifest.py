#!/usr/bin/env python3
"""Re-fetch readiness-evidence/423 at the published commit and verify it.

Checks (all must hold, exit 0 only then):
  1. every blob under readiness-evidence/423/ in the public tree of
     6181e900cd9f7ae618e1603e2ea867a5bb4d41a6 re-hashes to its Git blob id;
  2. every MANIFEST.json row's published_sha256 equals the sha256 of that
     public file, and original_sha256 == published_sha256 where
     path_redacted is false;
  3. the local copy (argv[1], default ../published-fixture-6181e900) is
     byte-identical to the public blobs.
Read-only against GitHub; needs an authenticated `gh`.
"""
import base64
import hashlib
import json
import os
import subprocess
import sys

REPO = "kebag-logic/milan-fpga"
COMMIT = "6181e900cd9f7ae618e1603e2ea867a5bb4d41a6"
PREFIX = "readiness-evidence/423/"


def gh(path):
    return json.loads(subprocess.run(["gh", "api", path], check=True,
                                     capture_output=True).stdout)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    local = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        here, "..", "published-fixture-6181e900")
    tree = gh(f"repos/{REPO}/git/trees/{COMMIT}?recursive=1")
    bad = 0
    if tree.get("truncated"):
        print("FAIL tree listing truncated")
        return 1
    files = {}
    for e in tree["tree"]:
        if e["type"] != "blob" or not e["path"].startswith(PREFIX):
            continue
        data = base64.b64decode(gh(f"repos/{REPO}/git/blobs/{e['sha']}")["content"])
        oid = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        rel = e["path"][len(PREFIX):]
        files[rel] = data
        ok = oid == e["sha"]
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} blob {e['sha']} {rel}")
        try:
            with open(os.path.join(local, rel), "rb") as fh:
                same = fh.read() == data
        except FileNotFoundError:
            same = False
        bad += not same
        print(f"{'ok  ' if same else 'FAIL'} local-copy-identical {rel}")
    manifest = json.loads(files["MANIFEST.json"])
    for row in manifest:
        data = files.get(row["file"])
        digest = hashlib.sha256(data).hexdigest() if data is not None else None
        ok = digest == row["published_sha256"]
        if not row["path_redacted"]:
            ok = ok and row["original_sha256"] == row["published_sha256"]
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} manifest {row['file']} sha256={digest}")
    listed = {row["file"] for row in manifest}
    print("not-in-manifest (covered only by blob ids):",
          sorted(set(files) - listed))
    print("RESULT", "PASS" if not bad else f"FAIL ({bad})")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
