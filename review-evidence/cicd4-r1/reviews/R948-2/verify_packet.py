#!/usr/bin/env python3
"""Verify and extract only the published author evidence; no review reports."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
summary = []
for commit, folder in (("6be24f180ccc2c0ddda4b5d3ffa40ba09d7885e3", "cicd4-r1"),
                       ("9141378262c3331229a56c23d2c2fbb14cd87b48", "cicd4-r2")):
    prefix = "review-evidence/" + folder
    def blob(path):
        return subprocess.check_output(["git", "show", commit + ":" + prefix + "/" + path], cwd=root)
    manifest = json.loads(blob("MANIFEST.json"))
    checked = 0
    for record in manifest:
        name = record["file"]
        if not name.startswith("author/"):
            continue
        data = blob(name)
        assert hashlib.sha256(data).hexdigest() == record["published_sha256"], name
        dest = out / "scratch" / folder / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        checked += 1
    signed = b"gpgsig " in subprocess.check_output(["git", "cat-file", "commit", commit], cwd=root)
    summary.append({"commit": commit, "folder": folder, "verified_author_files": checked,
                    "commit_signature_present": signed})
print(json.dumps(summary, indent=2))
