#!/usr/bin/env python3
"""Prove tracked filesystem bytes, modes, indexes and required submodule pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

PACKET = Path(__file__).resolve().parent
EXPECTED = "fa1294279c42f181b6f43c6e6bd812039798705c"
REQUIRED = ["protocol-processor", "gptp-processor", "third_party/verilog-axis"]
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(root, *args):
    return subprocess.run(["git", "-c", "core.commitGraph=false", "-C", str(root), *args],
                          env=ENV, check=True, capture_output=True).stdout


def audit(root, revision, label):
    assert git(root, "rev-parse", "HEAD").decode().strip() == revision, label
    expected = {}
    for row in git(root, "ls-tree", "-rz", revision).split(b"\0"):
        if row:
            meta, path = row.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            expected[path.decode()] = (mode, oid)
    actual_index = {}
    for row in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if row:
            meta, path = row.split(b"\t", 1)
            mode, oid, stage = meta.decode().split()
            assert stage == "0", (label, path, stage)
            assert path.decode() not in actual_index
            actual_index[path.decode()] = (mode, oid)
    assert actual_index == expected, (label, "index differs from pinned tree")
    checked = []
    links = {}
    for path, (mode, oid) in sorted(expected.items()):
        file = root / path
        if mode == "160000":
            links[path] = oid
            continue
        info = file.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(info.st_mode), (label, path, "symlink expected")
            data = os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(info.st_mode), (label, path, "regular file expected")
            assert mode == ("100755" if info.st_mode & 0o111 else "100644"), (label, path, "mode")
            data = file.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid, (label, path, "tracked bytes")
        checked.append([path, mode, oid])
    assert not git(root, "status", "--porcelain", "--untracked-files=all"), (label, "status")
    return {"revision": revision, "tree": git(root, "rev-parse", revision + "^{tree}").decode().strip(),
            "tracked_blobs_checked": len(checked), "index_equals_tree": True,
            "filesystem_bytes_and_modes_equal_tree": True, "status_clean": True,
            "gitlinks": links, "checked_blobs": checked}


def main():
    root = Path.cwd()
    receipts = {"candidate": audit(root, EXPECTED, "candidate")}
    for name in REQUIRED:
        sub = root / name
        assert sub.is_dir() and not sub.is_symlink()
        assert (sub / ".git").is_file(), (name, "registered submodule expected")
        superproject = git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip()
        assert Path(superproject).resolve() == root.resolve(), name
        pin = receipts["candidate"]["gitlinks"][name]
        receipts[name] = audit(sub, pin, name)
    (PACKET / "checkout-audit.json").write_text(json.dumps(receipts, indent=2) + "\n")
    for name, result in receipts.items():
        print(name, result["revision"], "PASS", result["tracked_blobs_checked"],
              "tracked blobs, filesystem modes and index verified")
    print("external: gitlink/index checked; checkout is intentionally uninitialized and not required")


if __name__ == "__main__":
    main()
