#!/usr/bin/env python3
"""Fetch only public source execution receipts, without reviewer reports."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

REPOSITORY = "kebag-logic/milan-fpga"
REVISION = "ff22678d017ecc58e271c917a76cb3423f4a0498"
PREFIX = "review-evidence/734-r1/author-r5"
NAMES = ["r5-head.json", "r5-merge-tree.json", "r5-publication.json", "r5-workflow.json", "r5-workflow.log", "r5-run_boundary.py.txt", "r5-batch_gates.py.txt", "r5-contract-final.json", "r5-contract-final.log", "r5-events-final.json", "r5-events-final.summary.txt", "r5-scope.json", "r5-scope.log", "r5-scope-classifications.json", "r5-scope-table-exact.json", "r5-scope-table-exact.log", "r5-scope_table.py", "r5-image-hashes.json", "r4-image-hashes.json", "r5-images.json", "r5-images.log", "r5-image-controls.json", "r5-image-controls.log", "r5-imported-paths.tsv", "r5-MANIFEST.sha256", "r5-docs-final.json", "r5-docs-final.log"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    destination = args.packet / "public-source"
    destination.mkdir(exist_ok=True)

    def fetch(name):
        path = f"{PREFIX}/{name}"
        endpoint = f"repos/{REPOSITORY}/contents/{path}?ref={REVISION}"
        record = json.loads(subprocess.check_output(["gh", "api", endpoint]))
        data = base64.b64decode(record["content"])
        oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert oid == record["sha"], name
        (destination / name).write_bytes(data)
        return {"file": f"public-source/{name}", "url": f"https://github.com/{REPOSITORY}/blob/{REVISION}/{path}", "git_blob": oid, "sha256": hashlib.sha256(data).hexdigest()}

    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(fetch, NAMES))
    (args.packet / "public-source-provenance.json").write_text(json.dumps(records, indent=2) + "\n")
    print(f"Verified and retained {len(records)} public source execution receipts at {REVISION}")


if __name__ == "__main__":
    main()
