#!/usr/bin/env python3
"""Verify only the explicitly supplied public author packet and its manifest."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument("--scratch", type=Path, required=True)
a = p.parse_args()
commit = "648503cfeee36d03d7baf2a7b8608e1310caae49"
root = "review-evidence/640-m5-r1"
def read(path):
    obj = json.loads(subprocess.check_output([
        "gh", "api", "repos/kebag-logic/milan-fpga/contents/" + root + "/" + path + "?ref=" + commit]))
    data = base64.b64decode(obj["content"])
    assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == obj["sha"]
    return data, obj["sha"]
manifest, _ = read("MANIFEST.json")
for entry in json.loads(manifest):
    assert entry["file"] in {"author/HANDOFF.md", "author/PR-BODY.md"}
    data, blob = read(entry["file"])
    digest = hashlib.sha256(data).hexdigest()
    assert digest == entry["published_sha256"]
    dest = a.scratch / entry["file"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    print(json.dumps({"source_commit": commit, "path": root + "/" + entry["file"],
                      "blob": blob, "sha256": digest, "bytes": len(data), "manifest_match": True}))
print("PASS supplied public author packet digests; this is provenance, not a re-execution of its gates")
