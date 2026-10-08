#!/usr/bin/env python3
"""Download only public executable evidence, never reviewer reports."""
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parents[1]
scratch = packet / "scratch"
prefix = "review-evidence/686-r1/"
repository = "repos/kebag-logic/milan-fpga"

def api(path):
    return json.loads(subprocess.check_output(["gh", "api", repository + path]))

revisions = {
    "original": "84add8ed571d376f8a1b39c3c6f71c4e80eed32a",
    "fixed": "16f2f7ea",
    "candidate": "319f3567ed693bc5dffd422164a768c142485a2d",
}
trees = {}
for label, revision in revisions.items():
    data = api(f"/git/trees/{revision}?recursive=1")
    assert not data["truncated"]
    trees[label] = {e["path"]: e for e in data["tree"] if e["type"] == "blob"}
    filename = {"original":"archive-tree.json", "fixed":"fix-tree.json", "candidate":"candidate-tree.json"}[label]
    (scratch / filename).write_text(json.dumps(data))

selected = []
for label, tree in trees.items():
    for path, entry in tree.items():
        if not path.startswith(prefix):
            continue
        short = path[len(prefix):]
        wanted = short == "MANIFEST.json"
        if label == "fixed":
            wanted |= short.startswith("author-r2/resource-receipts/")
        if label == "candidate" and short.startswith("manager-candidate/"):
            part = short.removeprefix("manager-candidate/")
            wanted |= part.startswith(("manager-builder/", "full-native/"))
            wanted |= part in ("manager-builder-initial-integrity.json", "full-native-initial-integrity.json",
                               "manager-builder.json", "full-native.json", "pinned-tool-identity.json")
        if wanted:
            selected.append((label, short, entry))

def download(row):
    label, short, entry = row
    destination = scratch / "public-evidence" / label / short
    if destination.exists():
        content = destination.read_bytes()
    else:
        data = api("/git/blobs/" + entry["sha"])
        assert data["encoding"] == "base64"
        content = base64.b64decode(data["content"])
    blob = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
    assert blob == entry["sha"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    return dict(archive=label, path=prefix + short, git_blob=blob, sha256=hashlib.sha256(content).hexdigest())

with ThreadPoolExecutor(max_workers=8) as pool:
    records = list(pool.map(download, selected))
original = json.loads((scratch / "public-evidence/original/MANIFEST.json").read_text())
fixed = {r["file"]: r for r in json.loads((scratch / "public-evidence/fixed/MANIFEST.json").read_text())}
preserved = 0
for row in original:
    if row["file"].startswith("author-r2/resource-receipts/") and not row["file"].endswith("/MANIFEST.sha256"):
        assert row == fixed[row["file"]], row["file"]
        preserved += 1
(packet / "receipts/evidence-downloads.json").write_text(json.dumps(records, indent=2) + "\n")
print(f"Verified {len(records)} downloaded public blobs against their Git object IDs")
print(f"Original provenance preserved for {preserved} resource files; checksum manifest itself updated")
