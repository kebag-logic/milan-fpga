#!/usr/bin/env python3
"""Fetch only public source evidence needed by verify_claims.py into scratch."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parent
SCRATCH = PACKET / "scratch"
SCRATCH.mkdir(exist_ok=True)
REPOSITORY = "kebag-logic/milan-fpga"
COMMIT = "8d4e0732588d09f1f94f41aea7c7c39110da09a2"
FILES = [
    "round2-baseline-F.json", "round2-effective-recipes.json",
    "round2-candidate-records.json", "round2-refresh-source-closure.json",
    "round2-synth-86901.md", "round2-complete-image-evidence.json",
    "round2-render-differential.json", "round2-render-adopted-clean-epoch.log",
    "round2-render-prior-clean-epoch.log",
]

def api(route, raw=False):
    args = ["gh", "api"]
    if raw:
        args += ["-H", "Accept: application/vnd.github.raw+json"]
    return subprocess.check_output([*args, route])

tree = json.loads(api(f"repos/{REPOSITORY}/git/trees/{COMMIT}?recursive=1"))
entries = {entry["path"]: entry for entry in tree["tree"]}

def fetch_file(name):
    path = "review-evidence/682-r1/author/" + name
    data = api(f"repos/{REPOSITORY}/contents/{path}?ref={COMMIT}", raw=True)
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert blob == entries[path]["sha"]
    (SCRATCH / name).write_bytes(data)
    return dict(path=path, git_blob=blob, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    receipts = list(pool.map(fetch_file, FILES))
(PACKET / "public_evidence_receipts.json").write_text(json.dumps(receipts, indent=2) + "\n")
for number in (156, 159, 160, 161, 162, 164):
    data = api(f"repos/Mister-M-alt/protocol-processor-control-plane-avb-milan/pulls/{number}")
    (SCRATCH / f"processor-pr-{number}.json").write_bytes(data)
print("Fetched and verified nine immutable evidence files and six public processor PR objects.")
