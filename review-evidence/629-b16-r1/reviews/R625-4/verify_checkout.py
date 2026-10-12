#!/usr/bin/env python3
"""Verify raw tracked bytes, file kinds, modes, index and required submodules.

Usage: python3 verify_checkout.py REPO OUTPUT.json
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = "61ae86419c50f2707d6ee1dc5433bc6dee66ce84"
TREE = "ed284e802555e2e1cb92f15d95dafa2702d3fc1d"
REQUIRED = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=ENV)


def check(root, rev):
    records = git(root, "ls-tree", "-rz", rev).split(b"\0")
    failures, links, expected = [], {}, []
    count = 0
    for record in filter(None, records):
        meta, name = record.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        rel = os.fsdecode(name)
        expected.append(mode.encode() + b" " + oid.encode() + b" 0\t" + name)
        if kind == "commit":
            links[rel] = oid
            continue
        p = root / rel
        count += 1
        try:
            st = p.lstat()
            if mode == "120000":
                assert stat.S_ISLNK(st.st_mode), "not symlink"
                data = os.fsencode(os.readlink(p))
            else:
                assert stat.S_ISREG(st.st_mode), "not regular file"
                assert bool(st.st_mode & 0o111) == (mode == "100755"), "mode mismatch"
                data = p.read_bytes()
            digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            assert digest == oid, "blob mismatch"
        except Exception as exc:
            failures.append({"path": rel, "error": str(exc)})
    index = git(root, "ls-files", "--stage", "-z").split(b"\0")
    index_equal = sorted(filter(None, index)) == sorted(expected)
    return {"blobs_checked": count, "failures": failures, "index_equal": index_equal,
            "gitlinks": links, "head": git(root, "rev-parse", "HEAD").decode().strip(),
            "tree": git(root, "rev-parse", rev + "^{tree}").decode().strip()}


def main():
    root, out = map(Path, sys.argv[1:3])
    result = {"parent": check(root, HEAD), "submodules": {}}
    for rel in REQUIRED:
        pin = result["parent"]["gitlinks"][rel]
        sub = check(root / rel, pin)
        sub["expected_pin"] = pin
        sub["registered"] = bool(git(root / rel, "rev-parse", "--show-superproject-working-tree").strip())
        result["submodules"][rel] = sub
    entries = [result["parent"], *result["submodules"].values()]
    result["pass"] = (result["parent"]["head"] == HEAD and result["parent"]["tree"] == TREE
        and all(not x["failures"] and x["index_equal"] for x in entries)
        and all(x["registered"] and x["head"] == x["expected_pin"] for x in result["submodules"].values()))
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
