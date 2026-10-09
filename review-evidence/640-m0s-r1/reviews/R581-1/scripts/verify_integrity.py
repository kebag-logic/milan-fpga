#!/usr/bin/env python3
"""Verify raw tracked bytes, modes, index records and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
expected = "bc89f84e6757f8fcddf21958e99f40f17bc0ee1e"
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(where, *args):
    return subprocess.check_output(["git", "-C", str(where), *args], env=env)

def verify(where, revision):
    assert git(where, "rev-parse", "HEAD").decode().strip() == revision
    records = git(where, "ls-tree", "-rz", revision).split(b"\0")
    expected_index, links, count = [], {}, 0
    for entry in filter(None, records):
        header, name = entry.split(b"\t", 1)
        mode, kind, oid = header.split()
        expected_index.append(mode + b" " + oid + b" 0\t" + name)
        path = where / os.fsdecode(name)
        if mode == b"160000":
            links[os.fsdecode(name)] = oid.decode()
            continue
        st = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), str(path)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), str(path)
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), str(path)
            data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid.decode(), str(path)
        count += 1
    actual_index = list(filter(None, git(where, "ls-files", "--stage", "-z").split(b"\0")))
    assert sorted(actual_index) == sorted(expected_index), "index differs from committed tree"
    return {"head": revision, "tree": git(where, "rev-parse", revision + "^{tree}").decode().strip(),
            "verified_blobs_and_modes": count, "index_matches": True, "gitlinks": links}

result = {"superproject": verify(root, expected), "submodules": {}}
for name in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
    folder = root / name
    assert not folder.is_symlink()
    assert (folder / ".git").is_file()
    assert Path(git(folder, "rev-parse", "--show-superproject-working-tree").decode().strip()) == root
    result["submodules"][name] = verify(folder, result["superproject"]["gitlinks"][name])
print(json.dumps(result, indent=2))
