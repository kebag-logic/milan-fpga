#!/usr/bin/env python3
"""Verify the public #117 review-evidence tree against its manifests.

Usage: verify_evidence_manifests.py <extracted review-evidence/117-r1 dir>
Checks: every MANIFEST.json published_sha256 equals the file bytes; every
packet MANIFEST.sha256 line either matches the published bytes or is a
redacted file whose MANIFEST.json original_sha256 equals the packet line;
every file in the tree is listed in MANIFEST.json (except MANIFEST.json).
"""
import hashlib, json, os, sys

root = sys.argv[1]
man = json.load(open(os.path.join(root, "MANIFEST.json")))
by = {e["file"]: e for e in man}
bad = 0
for e in man:
    p = os.path.join(root, e["file"])
    if not os.path.isfile(p):
        print("MISSING", e["file"]); bad += 1; continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != e["published_sha256"]:
        print("PUBLISHED-MISMATCH", e["file"]); bad += 1
    if (e["original_sha256"] != e["published_sha256"]) != bool(e["path_redacted"]):
        print("REDACTION-FLAG-INCONSISTENT", e["file"]); bad += 1
red = [e["file"] for e in man if e["path_redacted"]]
print("manifest.json entries", len(man), "redacted", len(red))
for r in red:
    print("  redacted:", r)
listed = set(by)
for dp, dn, fn in os.walk(root):
    for f in fn:
        rel = os.path.relpath(os.path.join(dp, f), root)
        if rel != "MANIFEST.json" and rel not in listed:
            print("UNLISTED", rel); bad += 1
for pk in ("bench-a200", "bench-a202"):
    n = 0
    for line in open(os.path.join(root, pk, "MANIFEST.sha256")):
        h, f = line.rstrip("\n").split(None, 1)
        f = f.lstrip("*")
        rel = os.path.normpath(os.path.join(pk, f))
        n += 1
        e = by.get(rel)
        if e is None:
            print("PACKET-LINE-NOT-PUBLISHED", rel); bad += 1; continue
        if h == e["published_sha256"]:
            continue
        if h == e["original_sha256"] and e["path_redacted"]:
            continue
        print("PACKET-LINE-MISMATCH", rel); bad += 1
    print(pk, "packet manifest lines", n)
print("RESULT", "PASS" if bad == 0 else "FAIL", "bad", bad)
sys.exit(1 if bad else 0)
