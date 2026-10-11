#!/usr/bin/env python3
"""Usage: verify_tree.py REPO REV [--submodules]. Prove bytes, modes and index.

Uses committed tree objects rather than status or index flags as the byte oracle.
Only the three required local-gate submodules are traversed.
"""
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys

ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], env=ENV)


def verify(repo, rev, submodules=False, label="root"):
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    assert head == rev, (label, "HEAD", head, rev)
    entries = {}
    count = 0
    for record in git(repo, "ls-tree", "-rz", "--full-tree", rev).split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        entries[path] = (mode, oid, "0")
        if kind == "commit":
            continue
        f = repo / os.fsdecode(path)
        st = f.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(st.st_mode), (label, path, "not symlink")
            raw = os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(st.st_mode), (label, path, "not regular")
            actual_mode = "100755" if st.st_mode & 0o111 else "100644"
            assert actual_mode == mode, (label, path, actual_mode, mode)
            raw = f.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        assert digest == oid, (label, path, "blob differs")
        count += 1
    index = {}
    for record in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if record:
            meta, path = record.split(b"\t", 1)
            mode, oid, stage = meta.decode().split()
            assert path not in index, (label, path, "multiple index stages")
            index[path] = (mode, oid, stage)
    assert index == entries, (label, "index/tree differ")
    print(f"{label}: HEAD {head}; tree {git(repo, 'rev-parse', rev + '^{tree}').decode().strip()}; "
          f"{count} blob bytes/modes verified; {len(index)} index entries exact")
    if submodules:
        for name in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
            mode, pin, stage = entries[os.fsencode(name)]
            assert mode == "160000" and stage == "0"
            sub = repo / name
            assert not sub.is_symlink() and (sub / ".git").is_file()
            parent = git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip()
            assert Path(parent).resolve() == repo.resolve(), (name, "wrong superproject")
            verify(sub, pin, False, name)
    print(f"{label}: PASS")


if __name__ == "__main__":
    verify(Path(sys.argv[1]).resolve(), sys.argv[2], "--submodules" in sys.argv[3:])
