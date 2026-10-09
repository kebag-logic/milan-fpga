#!/usr/bin/env python3
"""Check exact HEAD, tree, index, raw tracked bytes, modes and gitlinks.
Usage: verify_checkout.py CHECKOUT
"""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
head = "5024dcad23140597bc1ffa58d1613990b9f73279"
tree = "f407bb708ac9fa9d0b725808b99106756e2e00dc"
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args])
assert git("rev-parse", "HEAD").decode().strip() == head
assert git("rev-parse", "HEAD^{tree}").decode().strip() == tree
assert git("write-tree").decode().strip() == tree
assert not git("diff", "--raw", "HEAD")
index = {}
for entry in git("ls-files", "--stage", "-z").split(b"\0"):
    if not entry: continue
    metadata, path = entry.split(b"\t", 1)
    mode, sha, stage = metadata.split()
    assert stage == b"0", (path, stage)
    index[os.fsdecode(path)] = (mode.decode(), sha.decode())
count = 0
links = []
for entry in git("ls-tree", "-rz", "HEAD").split(b"\0"):
    if not entry: continue
    metadata, path_bytes = entry.split(b"\t", 1)
    mode, kind, sha = metadata.decode().split()
    path = os.fsdecode(path_bytes)
    assert index.pop(path) == (mode, sha), path
    if mode == "160000":
        actual = subprocess.check_output(["git", "-C", str(root/path), "rev-parse", "HEAD"]).decode().strip()
        assert actual == sha, path
        links.append({"path": path, "sha": sha})
        continue
    file = root/path
    if mode == "120000":
        assert file.is_symlink(), path
        raw = os.fsencode(os.readlink(file))
    else:
        assert file.is_file() and not file.is_symlink(), path
        raw = file.read_bytes()
        executable = bool(file.stat().st_mode & 0o111)
        assert executable == (mode == "100755"), path
    actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert actual == sha, path
    count += 1
assert not index
print(json.dumps({"head": head, "tree": tree, "index_tree": tree,
    "tracked_blobs_verified": count, "raw_bytes_and_modes": "PASS",
    "gitlinks": links, "submodule_status": git("submodule", "status", "--recursive").decode(),
    "porcelain_status": git("status", "--porcelain=v1").decode()}, indent=2))
