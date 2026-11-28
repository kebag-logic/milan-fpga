#!/usr/bin/env python3
"""Verify the published author-r8 evidence packet against both manifests.

Usage: verify_packet.py <extracted review-evidence/usbnet-r1 directory>

Checks, for the author-r8 subtree:
  1. every file present matches the publication manifest's published_sha256;
  2. every round7/round8 author MANIFEST.sha256 entry is either byte-verified
     (published file hash equals the author hash), or explained by a path
     redaction (publication manifest original_sha256 equals the author hash
     and path_redacted is true), or absent from publication (listed, not
     archived) - counted separately;
  3. no unexplained mismatch remains.
"""
import hashlib
import json
import os
import sys


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main(root):
    pub = {e["file"]: e for e in json.load(open(os.path.join(root, "MANIFEST.json")))}
    bad = 0
    present = 0
    for dp, _, fs in os.walk(os.path.join(root, "author-r8")):
        for f in fs:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root)
            present += 1
            e = pub.get(rel)
            if e is None:
                print("UNLISTED", rel)
                bad += 1
            elif sha(p) != e["published_sha256"]:
                print("PUBLISHED-MISMATCH", rel)
                bad += 1
    print("published files checked:", present)
    for rnd in ("round7", "round8"):
        base = os.path.join(root, "author-r8", rnd, "receipts")
        counts = {"byte": 0, "redacted": 0, "absent": 0, "unexplained": 0}
        for line in open(os.path.join(base, "MANIFEST.sha256")):
            h, name = line.rstrip("\n").split("  ", 1)
            rel = os.path.join("author-r8", rnd, "receipts", name)
            p = os.path.join(root, rel)
            e = pub.get(rel)
            if not os.path.exists(p):
                counts["absent"] += 1
                if e is not None:
                    print("LISTED-BUT-MISSING", rel)
                    bad += 1
                continue
            if sha(p) == h:
                counts["byte"] += 1
            elif e and e["path_redacted"] and e["original_sha256"] == h:
                counts["redacted"] += 1
            else:
                counts["unexplained"] += 1
                print("UNEXPLAINED", rel)
                bad += 1
        print(rnd, counts)
    print("RESULT", "PASS" if bad == 0 else "FAIL", bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
