#!/usr/bin/env python3
"""Prove initialized required submodules by raw blob bytes, modes, and index."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0")
    def git(root, *args):
        return subprocess.check_output(["git", "-c", "core.fsmonitor=false", "-C", str(root), *args], env=env)
    results = []
    for path in ["protocol-processor", "gptp-processor", "third_party/verilog-axis", "third_party/tsn-c-stack"]:
        root = args.root / path
        pin = git(args.root, "ls-tree", "HEAD", path).decode().split()[2]
        assert git(root, "rev-parse", "HEAD").decode().strip() == pin
        expected, checked = {}, 0
        for record in git(root, "ls-tree", "-rz", pin).split(b"\0"):
            if not record:
                continue
            meta, name = record.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            expected[name.decode()] = (mode, oid)
            if mode == "160000":
                continue
            target = root / name.decode()
            info = target.lstat()
            actual_mode = "120000" if target.is_symlink() else "100755" if info.st_mode & 0o111 else "100644"
            data = os.readlink(target).encode() if target.is_symlink() else target.read_bytes()
            digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            assert (actual_mode, digest) == (mode, oid), (path, name.decode())
            checked += 1
        index = {}
        for record in git(root, "ls-files", "--stage", "-z").split(b"\0"):
            if record:
                meta, name = record.split(b"\t", 1)
                mode, oid, stage = meta.decode().split()
                assert stage == "0"
                index[name.decode()] = (mode, oid)
        assert index == expected, path
        results.append({"path": path, "pin": pin, "verified_blobs": checked, "bytes_and_modes_match": True, "index_matches_pin": True})
    args.output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
