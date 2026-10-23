#!/usr/bin/env python3
"""Read-only download and hash verification of selected public evidence."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys

OUT = Path(sys.argv[1])
REF = "2e4361bf22109bf9c158b2d3b5aba28401632a1e"
BASE = "repos/kebag-logic/milan-fpga/contents/review-evidence/632-r1/"
def fetch(path):
    return subprocess.check_output(["gh", "api", BASE + path + "?ref=" + REF,
        "-H", "Accept: application/vnd.github.raw+json"])
manifest_bytes = fetch("MANIFEST.json")
blob = hashlib.sha1(b"blob " + str(len(manifest_bytes)).encode() + b"\0" + manifest_bytes).hexdigest()
assert blob == "c3c4ad2fcf3bfe24f8e3b3f9cb595bae10896e22"
manifest = json.loads(manifest_bytes)
index = {r["file"]: r for r in manifest}
prefix = "author-r8b/receipts/round8/"
paths = [prefix + "INDEX.md",
    prefix + "docs_steps_24a292a0/README.txt",
    prefix + "docs_steps_24a292a0/docs/all.out",
    prefix + "docs_steps_24a292a0/origin-dev-and-head.txt",
    prefix + "legs_24a292a0/gptp.log",
    prefix + "legs_24a292a0/ax1x1gptp.log",
    prefix + "legs_24a292a0/HEAD.txt",
    prefix + "legs_24a292a0/summary.txt",
    prefix + "legs_24a292a0/gptp.rc",
    prefix + "legs_24a292a0/ax1x1gptp.rc",
    prefix + "dynmap_mutants_24a292a0/HEAD.txt",
    prefix + "dynmap_mutants_24a292a0/rc",
    prefix + "dynmap_mutants_24a292a0/verdict_lines.txt",
    prefix + "lint_24a292a0/rc.txt",
    prefix + "lint_24a292a0/check_baseline.log"]
paths += [p for p in index if p.startswith(prefix + "manager-r5fix/")]
def one(path):
    destination = OUT / "receipts" / path
    data = destination.read_bytes() if destination.is_file() else fetch(path)
    digest = hashlib.sha256(data).hexdigest()
    row = index[path]
    assert digest == row["published_sha256"], path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return {"path": path, "bytes": len(data), "sha256": digest,
            "matches_published_manifest": True, "path_redacted": row["path_redacted"]}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    verified = list(pool.map(one, paths))
result = {"evidence_commit": REF, "manifest_git_blob": blob,
    "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
    "manifest_entries": len(manifest), "verified_receipts": verified}
(OUT / "receipt-verification.json").write_text(json.dumps(result, indent=2) + "\n")
print("PASS: manifest Git blob and", len(verified), "published receipt SHA-256 values")
