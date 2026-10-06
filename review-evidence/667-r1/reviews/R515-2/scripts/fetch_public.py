#!/usr/bin/env python3
"""Fetch only the named public evidence; never read another review's report."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

REPOSITORY = "kebag-logic/milan-fpga"
AUTHOR_COMMIT = "90d0bcbfb83ee4f5d47edadd734acd1e1056759b"
REVIEW_COMMIT = "10ed097ff73b91f7a749484acfc7223800b80e1a"
PREFIX = "review-evidence/667-r1/"
REVIEW_FILES = [
    "MANIFEST.sha256",
    "receipts/epoch-base-run.log", "receipts/epoch-base-run.rc",
    "receipts/epoch-head-run.log", "receipts/epoch-head-run.rc",
    "receipts/epoch-dev-run.log", "receipts/epoch-dev-run.rc",
    "receipts/epoch-dev-comparison.json", "receipts/epoch-failure-lines.json",
    "receipts/epoch-comparison.json", "receipts/evidence-audit.json",
    "receipts/tree-integrity.json", "receipts/authority-identities.json",
    "scripts/check_dev_epoch.py", "scripts/check_epoch.py",
]


def api(endpoint):
    return json.loads(subprocess.check_output([
        "gh", "api", f"repos/{REPOSITORY}/{endpoint}"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    packet = args.packet.resolve()
    receipts = packet / "receipts"
    receipts.mkdir(exist_ok=True)
    tasks = []
    for commit, mode in [(AUTHOR_COMMIT, "author"), (REVIEW_COMMIT, "review")]:
        tree = api(f"git/trees/{commit}?recursive=1")
        assert not tree.get("truncated"), "Incomplete evidence inventory"
        for entry in tree["tree"]:
            path = entry["path"]
            if entry["type"] != "blob":
                continue
            if mode == "author" and path.startswith(PREFIX):
                local = packet / "scratch/public-source" / path.removeprefix(PREFIX)
            elif mode == "review" and path.startswith(PREFIX + "reviews/R515-1/"):
                suffix = path.removeprefix(PREFIX + "reviews/R515-1/")
                if suffix not in REVIEW_FILES:
                    continue
                local = receipts / "prior" / suffix
            else:
                continue
            tasks.append((commit, entry, local))

    def fetch(task):
        commit, entry, local = task
        payload = api(f"git/blobs/{entry['sha']}")
        assert payload["encoding"] == "base64"
        data = base64.b64decode(payload["content"])
        assert len(data) == entry["size"]
        oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert oid == entry["sha"]
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_bytes(data)
        return {"commit": commit, "path": entry["path"], "git_blob": oid,
                "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                "local": str(local.relative_to(packet)),
                "url": f"https://github.com/{REPOSITORY}/blob/{commit}/{entry['path']}"}

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(fetch, tasks))
    (receipts / "public-fetch.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"Verified public Git blob identities for {len(results)} files")


if __name__ == "__main__":
    main()
