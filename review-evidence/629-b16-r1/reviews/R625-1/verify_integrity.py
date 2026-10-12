#!/usr/bin/env python3
"""Read-only verification of tracked bytes, modes, index and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = "e20fd2820a9c6b9effabc529a742e732263fafa8"
TREE = "6299ec05fc1085b62defe945c9dc5c426e54d055"
REQUIRED = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=ENV)


def check(root, pin, label):
    entries = git(root, "ls-tree", "-rz", "--full-tree", pin).split(b"\0")
    expected_index = []
    errors = []
    count = 0
    links = {}
    for entry in entries:
        if not entry:
            continue
        meta, name = entry.split(b"\t", 1)
        mode, kind, oid = meta.split()
        expected_index.append(mode + b" " + oid + b" 0\t" + name)
        if kind == b"commit":
            links[os.fsdecode(name)] = oid.decode()
            continue
        path = root / os.fsdecode(name)
        try:
            st = path.lstat()
            if mode == b"120000":
                assert stat.S_ISLNK(st.st_mode)
                data = os.fsencode(os.readlink(path))
            else:
                assert stat.S_ISREG(st.st_mode)
                assert bool(st.st_mode & 0o111) == (mode == b"100755")
                data = path.read_bytes()
            got = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            assert got == oid.decode()
            count += 1
        except (OSError, AssertionError):
            errors.append(os.fsdecode(name))
    index = git(root, "ls-files", "--stage", "-z").rstrip(b"\0").split(b"\0")
    index_ok = sorted(index) == sorted(expected_index)
    head_ok = git(root, "rev-parse", "HEAD").decode().strip() == pin
    return {"repository": label, "head": pin, "head_matches": head_ok,
            "tracked_blobs_verified": count, "byte_or_mode_errors": errors,
            "index_matches_tree": index_ok, "gitlinks": links,
            "index_entries_sha256": hashlib.sha256(b"\0".join(index)).hexdigest(),
            "pass": not errors and index_ok and head_ok}


root = Path(sys.argv[1]).resolve()
rows = [check(root, HEAD, "candidate")]
assert git(root, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
for name in REQUIRED:
    row = check(root / name, rows[0]["gitlinks"][name], name)
    row["registered_submodule"] = (root / name / ".git").is_file()
    row["pass"] &= row["registered_submodule"]
    rows.append(row)
print(json.dumps({"head": HEAD, "tree": TREE, "repositories": rows,
                  "pass": all(r["pass"] for r in rows)}, indent=2))
sys.exit(0 if all(r["pass"] for r in rows) else 1)
