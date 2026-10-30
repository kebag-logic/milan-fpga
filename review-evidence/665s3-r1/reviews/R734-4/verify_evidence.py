#!/usr/bin/env python3
"""Verify only public author receipts; never open review directories."""
import hashlib, json, pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve()
rev = "06c6f5d97328e8c4c684314df156d02637224341"
base = "review-evidence/665s3-r1/"
def git(*args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(root), *args])
manifest = json.loads(git("show", rev + ":" + base + "MANIFEST.json"))
count = 0
for entry in manifest:
    name = entry["file"]
    if not name.startswith("author-r3/receipts/"):
        continue
    data = git("show", rev + ":" + base + name)
    digest = hashlib.sha256(data).hexdigest()
    assert digest == entry["published_sha256"], name
    path = out / "scratch/public-receipts" / name.removeprefix("author-r3/receipts/")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print(digest, name)
    count += 1
print("Verified published receipt hashes:", count)
commit = git("cat-file", "commit", rev)
print("Evidence commit carries embedded signature:", b"\ngpgsig " in commit)
print("Hash integrity is not independent execution or cryptographic signer authentication.")
