#!/usr/bin/env python3
"""Compare raw checkout bytes, file modes and stage-zero index with committed trees."""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys
HEAD = "77a74b2f4e289c5a5a89687e07a6925cfedf6860"
TREE = "83462698a273b938f8cc108da7c6581acda83573"
REQUIRED = ("protocol-processor", "gptp-processor", "third_party/verilog-axis",
            "third_party/tsn-c-stack", "third_party/lwSRP")

def git(root, *args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(root), *args])

def inspect(root, rev, label):
    assert git(root, "rev-parse", "HEAD").decode().strip() == rev, label
    records = git(root, "ls-tree", "-r", "-z", rev).split(b"\0")
    expected_index = []
    links = {}
    blobs = 0
    for record in filter(None, records):
        info, raw_name = record.split(b"\t", 1)
        mode, kind, oid = info.split()
        expected_index.append(mode + b" " + oid + b" 0\t" + raw_name)
        name = os.fsdecode(raw_name)
        path = root / name
        if kind == b"commit":
            links[name] = oid.decode()
            continue
        metadata = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(metadata.st_mode), (label, name, "not symlink")
            data = os.fsencode(os.readlink(path))
        else:
            assert mode in (b"100644", b"100755") and stat.S_ISREG(metadata.st_mode), (label, name, "file kind")
            actual_mode = b"100755" if metadata.st_mode & 0o111 else b"100644"
            assert actual_mode == mode, (label, name, "mode")
            data = path.read_bytes()
        hashed = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert hashed == oid, (label, name, "blob")
        blobs += 1
    index = list(filter(None, git(root, "ls-files", "--stage", "-z").split(b"\0")))
    assert index == expected_index, (label, "index differs")
    flags = list(filter(None, git(root, "ls-files", "-v", "-z").split(b"\0")))
    assert all(r[:1] == b"H" for r in flags), (label, "hidden index flags")
    print(f"PASS {label}: HEAD {rev}; {blobs} raw blobs and modes; complete stage-zero index; no hidden flags")
    return links

def main():
    root = Path(sys.argv[1]).resolve()
    assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
    links = inspect(root, HEAD, "parent")
    for name in REQUIRED:
        sub = root / name
        assert (sub / ".git").is_file(), (name, "not an initialized submodule")
        assert git(sub, "rev-parse", "--show-superproject-working-tree").strip(), (name, "not registered")
        inspect(sub, links[name], name)
    before = git(root, "ls-tree", "dd163e41", *REQUIRED, "external")
    after = git(root, "ls-tree", HEAD, *REQUIRED, "external")
    assert before == after, "gitlinks changed since task base"
    print("PASS all required gitlinks and unused external gitlink unchanged from dd163e41")
    print("PASS reviewed HEAD and tree exact; no tracked source restoration required")

if __name__ == "__main__":
    main()
