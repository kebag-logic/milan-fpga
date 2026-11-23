#!/usr/bin/env python3
"""Verify published author evidence without opening other reviewers reports."""
import hashlib
import json
import subprocess
from pathlib import Path
import sys
root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
rev = "f6dd644d37fe4035aa263fc05e8da3524f3c3fcc"
base = "review-evidence/972-r1/"
def git(*args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(root), *args])
manifest = json.loads(git("show", rev + ":" + base + "MANIFEST.json"))
rows = []
for row in manifest:
    name = row["file"]
    if not name.startswith(("author-r1/", "author-r3/")):
        continue
    data = git("show", rev + ":" + base + name)
    sha = hashlib.sha256(data).hexdigest()
    assert sha == row["published_sha256"], name
    rows.append(f"PASS {sha} {name}")
    if name.startswith("author-r3/"):
        path = out / "scratch" / "public" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
commit = git("cat-file", "commit", rev)
header = commit.split(b"\n\n", 1)[0]
rows += [f"VERIFIED {len(rows)} author files against published_sha256", f"Evidence commit {rev}",
         "Commit cryptographic signature present: " + str(b"gpgsig " in header),
         "Hash agreement proves published packet integrity; it does not independently reproduce executions."]
(out / "packet-integrity.txt").write_text("\n".join(rows) + "\n")
print("\n".join(rows[-4:]))
