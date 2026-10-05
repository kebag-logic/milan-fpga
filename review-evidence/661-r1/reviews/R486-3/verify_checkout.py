#!/usr/bin/env python3
"""Prove exact tracked bytes, filesystem modes, index entries and required pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = "3048222541ea6be725417ba0cd957607f0b821cb"
TREE = "a640b146eb68632f2d9ca153639ba2683b172b0a"
PINS = {
    "protocol-processor": "ead8036035affd53ef4b29979190f2f4f67084c0",
    "gptp-processor": "5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d",
    "third_party/verilog-axis": "48ff7a7e2ef782cf778d47910cf85835c64b1bce",
}
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=ENV)


def verify(root, rev):
    assert git(root, "rev-parse", "HEAD").decode().strip() == rev
    entries = {}
    actual = {}
    count = 0
    for row in git(root, "ls-tree", "-rz", rev).split(b"\0"):
        if not row:
            continue
        info, name = row.split(b"\t", 1)
        mode, kind, oid = info.split()
        entries[name] = (mode, oid)
        if kind == b"commit":
            continue
        path = root / os.fsdecode(name)
        st = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
            found_mode = b"120000"
        else:
            assert stat.S_ISREG(st.st_mode), name
            data = path.read_bytes()
            found_mode = b"100755" if st.st_mode & 0o111 else b"100644"
        found_oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest().encode()
        assert (found_mode, found_oid) == (mode, oid), name
        actual[name] = (found_mode, found_oid)
        count += 1
    indexed = {}
    for row in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not row:
            continue
        info, name = row.split(b"\t", 1)
        mode, oid, stage = info.split()
        assert stage == b"0" and name not in indexed, name
        indexed[name] = (mode, oid)
    assert indexed == entries, "index does not equal tree"
    encoded = b"\0".join(n + b" " + b" ".join(actual[n]) for n in sorted(actual))
    return {"head": rev, "tree": git(root, "rev-parse", rev + "^{tree}").decode().strip(),
            "verified_blobs": count, "bytes_and_modes_sha256": hashlib.sha256(encoded).hexdigest(),
            "index_exact": True, "tracked_bytes_exact": True}, entries


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    result, entries = verify(root, HEAD)
    assert result["tree"] == TREE
    out = {"root": result, "required_submodules": {}}
    for name, pin in PINS.items():
        assert entries[name.encode()] == (b"160000", pin.encode())
        sub = root / name
        assert not sub.is_symlink() and (sub / ".git").is_file(), name
        superproject = git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip()
        assert Path(superproject).resolve() == root, name
        out["required_submodules"][name], _ = verify(sub, pin)
    out["unused_external_gitlink"] = entries[b"external"][1].decode()
    out["status"] = "PASS"
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
