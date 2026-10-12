#!/usr/bin/env python3
"""Compare tracked bytes, executable modes, index entries and dependency pins."""
import hashlib
import json
import os
import pathlib
import stat
import subprocess
import sys

root, packet = map(pathlib.Path, sys.argv[1:])
expected = "1add0cfbcc778c5292a5935631ca7b47c612b990"
def git(directory, *args):
    return subprocess.check_output(["git", *args], cwd=directory)

def verify(directory, commit):
    actual = git(directory, "rev-parse", "HEAD").decode().strip()
    assert actual == commit, (directory.name, actual, commit)
    entries = {}
    for entry in git(directory, "ls-tree", "-rz", "HEAD").split(b"\0"):
        if not entry:
            continue
        metadata, path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        entries[os.fsdecode(path)] = (mode, kind, oid)
    index = {}
    for entry in git(directory, "ls-files", "--stage", "-z").split(b"\0"):
        if not entry:
            continue
        metadata, path = entry.split(b"\t", 1)
        mode, oid, stage = metadata.decode().split()
        assert stage == "0"
        index[os.fsdecode(path)] = (mode, oid)
    assert index == {name: (mode, oid) for name, (mode, _, oid) in entries.items()}
    files = 0
    links = {}
    for name, (mode, kind, oid) in entries.items():
        path = directory / name
        if kind == "commit":
            links[name] = oid
            continue
        status = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(status.st_mode), name
            content = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(status.st_mode), name
            actual_mode = "100755" if status.st_mode & 0o111 else "100644"
            assert actual_mode == mode, (name, mode, actual_mode)
            content = path.read_bytes()
        computed = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        assert computed == oid, (name, computed, oid)
        files += 1
    assert git(directory, "diff", "--check") == b""
    status = git(directory, "status", "--porcelain=v1", "--untracked-files=all", "--ignored").decode()
    assert not status, (directory.name, status)
    return {"head": actual, "tree": git(directory, "rev-parse", "HEAD^{tree}").decode().strip(),
            "tracked_blob_bytes_and_modes_verified": files,
            "index_matches_tree": True, "gitlinks": links, "status_including_ignored": status}

result = {"root": verify(root, expected)}
for name in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
    result[name] = verify(root / name, result["root"]["gitlinks"][name])
before = git(root, "ls-tree", "-r", "c6bd08c6").decode().splitlines()
baseline_links = dict((line.split("\t", 1)[1], line.split()[2]) for line in before if line.startswith("160000 "))
assert baseline_links == result["root"]["gitlinks"]
result["all_five_gitlinks_unchanged_from_base"] = True
result["firmware_implementation_config_workflow_diff"] = git(root, "diff", "--name-only", "c6bd08c6..HEAD", "--", ".github", "configs", "sw/firmware", ":!sw/firmware/ctrl/aecp/README.md").decode()
assert not result["firmware_implementation_config_workflow_diff"]
unit = pathlib.Path("/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-726-r629-4.service")
if unit.exists():
    result["resource_receipt"] = {f: (unit / f).read_text().strip() for f in ("memory.max", "memory.peak", "memory.events")}
(packet / "receipts/checkout-verification.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
