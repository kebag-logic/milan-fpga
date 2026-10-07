#!/usr/bin/env python3
"""Compare the original checkout bytes, modes, index and gitlinks with the head.

Usage: python3 scripts/verify_integrity.py SOURCE PACKET
"""
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

source, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
head = "5f9b9d99e1d94485fc00a1b1539baf2ae861cb65"
tree = "e8bc64162172057dc185b67d0b4a19839819a78d"

def git(*args):
    return subprocess.check_output(["git", *args], cwd=source)

assert git("rev-parse", "HEAD").decode().strip() == head
assert git("rev-parse", "HEAD^{tree}").decode().strip() == tree
expected = {}
for row in git("ls-tree", "-rz", "HEAD").split(b"\0"):
    if not row:
        continue
    meta, name = row.split(b"\t")
    mode, kind, oid = meta.decode().split()
    expected[name.decode()] = (mode, oid)
index = {}
for row in git("ls-files", "--stage", "-z").split(b"\0"):
    if not row:
        continue
    meta, name = row.split(b"\t")
    mode, oid, stage = meta.decode().split()
    assert stage == "0"
    index[name.decode()] = (mode, oid)
assert index == expected
rows = []
gitlinks = []
for name, (mode, oid) in expected.items():
    if mode == "160000":
        gitlinks.append(dict(path=name, oid=oid))
        continue
    path = source / name
    data = path.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    disk_mode = "100755" if path.stat().st_mode & stat.S_IXUSR else "100644"
    assert (disk_mode, actual) == (mode, oid), name
    rows.append(dict(path=name, mode=mode, blob=oid, bytes_verified=True, index_verified=True))
assert not gitlinks, "This review expects the standalone tree to have no gitlinks"
assert not git("status", "--porcelain", "--untracked-files=all")
assert not git("diff", "19f5796..HEAD", "--", "src")
assert not git("diff", "e4f9995b791489c53b8ccb8a8dc09ec508e32e6b..HEAD", "--", "src", "tests", "CMakeLists.txt", "build.sh", "zephyr", "Kconfig.zephyr", "behave.ini")
subprocess.run(["git", "diff", "--check", "19f5796..HEAD"], cwd=source, check=True)
result = dict(head=head, tree=tree, tracked_files=len(rows), files=rows, gitlinks=gitlinks,
              index_exact=True, worktree_exact=True, source_unchanged_from_base=True,
              executable_tree_matches_merged_test_fix=True, whitespace_check_rc=0)
(packet / "receipts/integrity.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k:v for k,v in result.items() if k != "files"}, indent=2))
