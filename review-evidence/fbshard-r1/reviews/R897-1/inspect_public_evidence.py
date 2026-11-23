#!/usr/bin/env python3
"""Read only selected published executable receipts, authenticating their hashes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
revision = "26ba6dd9bfa2f73c191b38aab918c7c1dfefa660"
prefix = "review-evidence/fbshard-r1/"
def read(path):
    return subprocess.check_output(["git", "-C", str(root), "show", f"{revision}:{prefix}{path}"])
manifest = {row["file"]: row for row in json.loads(read("MANIFEST.json"))}
files = ["INDEX.md", "final-shard-0of3.log", "final-shard-1of3.log", "final-shard-2of3.log",
         "final-judge-3-shards.log", "head-judge-3-shards.log", "control-gate-union-proof.log",
         "plant-dropped-capture.log", "plant-duplicated-capture.log", "plant-table.log",
         "head-ci-and-docs-gates.log", "head-ci_events-selftest.log", "hosted-unsharded-45071981993.txt",
         "tools/compare_sets.py"]
result = []
for name in files:
    path = "author/receipts/" + name
    data = read(path)
    sha = hashlib.sha256(data).hexdigest()
    assert sha == manifest[path]["published_sha256"]
    lines = data.decode().splitlines()
    print(path, sha)
    if name.endswith(".log"):
        for line in lines[-5:]:
            print(line)
    result.append({"path": path, "sha256": sha, "lines": len(lines)})
(packet / "public-evidence.json").write_text(json.dumps({"revision": revision, "prefix": prefix, "examined": result}, indent=2) + "\n")
