#!/usr/bin/env python3
"""Verify exact head, tree, index, tracked bytes/modes and all gitlinks, read-only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HEAD = "169073fe9751b873d140b46d4363e02ad4f56b88"
TREE = "4396587d7017497d185c38d3c497ab3b7e04cb42"
BASE = "5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    a = parser.parse_args()
    repo = a.repo.resolve()

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=repo)

    assert git("rev-parse", "HEAD").decode().strip() == HEAD
    assert git("rev-parse", "HEAD^{tree}").decode().strip() == TREE
    assert git("merge-base", BASE, HEAD).decode().strip() == BASE
    # Reading stage entries verifies the existing index without refreshing it.
    index = {}
    for raw in git("ls-files", "--stage", "-z").split(b"\0"):
        if raw:
            info, path = raw.split(b"\t", 1)
            mode, oid, stage = info.split()
            assert stage == b"0"
            index[path] = (mode, oid)
    expected, gitlinks, checked = {}, [], []
    for raw in git("ls-tree", "-rz", HEAD).split(b"\0"):
        if not raw:
            continue
        info, path = raw.split(b"\t", 1)
        mode, kind, oid = info.split()
        expected[path] = (mode, oid)
        file = repo / os.fsdecode(path)
        if mode == b"160000":
            actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=file).strip()
            assert actual == oid
            gitlinks.append({"path": os.fsdecode(path), "oid": oid.decode()})
            continue
        assert kind == b"blob"
        st = file.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(file))
            actual_mode = b"120000"
        else:
            assert stat.S_ISREG(st.st_mode)
            data = file.read_bytes()
            actual_mode = b"100755" if st.st_mode & 0o111 else b"100644"
        assert actual_mode == mode, os.fsdecode(path)
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid.decode(), os.fsdecode(path)
        checked.append({"path": os.fsdecode(path), "mode": mode.decode(), "blob": actual})
    assert index == expected, "index differs from exact-head tree"
    status = git("status", "--porcelain=v1", "--untracked-files=all").decode()
    assert status == "", status
    diff = git("diff", BASE, HEAD, "--", "hdl", "tb", "bench", "scripts").decode()
    assert diff == ""
    subprocess.run(["git", "diff", "--check", BASE, HEAD], cwd=repo, check=True)
    ignored = git("status", "--porcelain=v1", "--ignored").decode()
    result = dict(head=HEAD, tree=TREE, base=BASE, index_equals_head=True,
                  tracked_blob_count=len(checked), tracked_bytes_and_modes_equal_head=True,
                  tracked_blobs=checked, required_gitlinks=gitlinks,
                  gitlink_count=len(gitlinks), status=status, status_with_ignored=ignored,
                  no_hdl_tb_bench_scripts_delta=True, diff_check="PASS")
    a.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS exact head/tree; index; {len(checked)} tracked blobs and modes; {len(gitlinks)} required gitlinks; clean status")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
