#!/usr/bin/env python3
"""Check source bytes, modes, index and gitlinks, and regenerate both ROMs at base/head."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tarfile

HEAD = "9975764846e7e63bccf0b68a5188d5cc7f23f890"
TREE = "5e0b23b212b2fb4da5735821694ec43e66421d0f"
BASE = "2cbed0a987c1e68402658d69459ab7e5aa571adc"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--packet", type=Path, required=True)
    a = ap.parse_args()
    (a.packet / "scratch").mkdir(parents=True, exist_ok=True)
    (a.packet / "receipts").mkdir(parents=True, exist_ok=True)
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=a.root)
    assert git("rev-parse", "HEAD").decode().strip() == HEAD
    assert git("rev-parse", "HEAD^{tree}").decode().strip() == TREE
    entries = []
    expected_index = {}
    gitlinks = {}
    for row in git("ls-tree", "-rz", "HEAD").split(b"\0"):
        if not row:
            continue
        meta, rawpath = row.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        path = rawpath.decode()
        expected_index[path] = (mode, oid, "0")
        target = a.root / path
        if kind == "commit":
            gitlinks[path] = oid
            child = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=target).decode().strip()
            assert child == oid, path
            continue
        data = os.readlink(target).encode() if mode == "120000" else target.read_bytes()
        actual = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        assert actual == oid, path
        observed_mode = "120000" if target.is_symlink() else ("100755" if target.stat().st_mode & stat.S_IXUSR else "100644")
        assert observed_mode == mode, path
        entries.append({"path": path, "mode": mode, "blob": oid})
    index = {}
    for row in git("ls-files", "--stage", "-z").split(b"\0"):
        if row:
            meta, path = row.split(b"\t", 1)
            index[path.decode()] = tuple(meta.decode().split())
    assert index == expected_index
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    result = {"head": HEAD, "tree": TREE, "tracked_blobs_verified": len(entries),
              "bytes_modes_index": "PASS", "gitlinks": gitlinks,
              "worktree_status": "clean", "detached": subprocess.run(
                  ["git", "symbolic-ref", "-q", "HEAD"], cwd=a.root, capture_output=True).returncode == 1}
    print(json.dumps(result, indent=2))
    (a.packet / "receipts/final-integrity.json").write_text(json.dumps(result, indent=2) + "\n")
    (a.packet / "receipts/tracked-blobs.json").write_text(json.dumps(entries, indent=2) + "\n")
    images = {}
    for label, commit in (("base", BASE), ("head", HEAD)):
        root = a.packet / "scratch" / ("identity-" + label)
        root.mkdir(exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(git("archive", commit))) as tf:
            tf.extractall(root, filter="data")
        images[label] = {}
        for source, output in (("hdl/aecp/ucode/gen_ucode.py", "ucode.hex"),
                               ("hdl/acmp/rom/gen_ltn_rom.py", "ltn_rom.hex")):
            subprocess.run(["python3", "-B", source, "-o", output], cwd=root, check=True)
            data = (root / output).read_bytes()
            images[label][output] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    assert images["base"] == images["head"]
    sv = git("diff", "--name-only", BASE, HEAD, "--", "hdl/**/*.sv").decode()
    assert not sv
    print(json.dumps({"roms": images, "production_sv_diff": sv}, indent=2))
    (a.packet / "receipts/rom-identity.json").write_text(json.dumps(images, indent=2) + "\n")


if __name__ == "__main__":
    main()
