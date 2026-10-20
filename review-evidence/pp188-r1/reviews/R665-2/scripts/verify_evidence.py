#!/usr/bin/env python3
"""Check the published author packet against its manifest.

Usage: python3 -I verify_evidence.py PACKET_ROOT PREFIX
  PACKET_ROOT is review-evidence/pp188-r1 of a checkout of the evidence
  repository at the published commit; PREFIX selects the entries (author-r2/).
Every manifest entry under PREFIX must exist and hash to its published_sha256,
and every file present under PREFIX must be listed. Exit 0 only then.
"""
import hashlib
import json
import os
import sys


def main() -> int:
    root, prefix = sys.argv[1], sys.argv[2]
    entries = [e for e in json.load(open(os.path.join(root, "MANIFEST.json")))
               if e["file"].startswith(prefix)]
    listed, ok, bad, missing = set(), 0, [], []
    for e in entries:
        listed.add(e["file"])
        path = os.path.join(root, e["file"])
        if not os.path.exists(path):
            missing.append(e["file"])
            continue
        with open(path, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        if digest == e["published_sha256"]:
            ok += 1
        else:
            bad.append(e["file"])
    present = set()
    for d, _, files in os.walk(os.path.join(root, prefix)):
        for name in files:
            present.add(os.path.relpath(os.path.join(d, name), root))
    unlisted = sorted(present - listed)
    print(f"entries {len(entries)} ok {ok} bad {len(bad)} missing {len(missing)} "
          f"unlisted {len(unlisted)}")
    for name in bad + missing + unlisted:
        print("  ", name)
    return 0 if not (bad or missing or unlisted) else 1


if __name__ == "__main__":
    raise SystemExit(main())
