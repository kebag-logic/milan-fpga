#!/usr/bin/env python3
"""Read-only exact-head, index, worktree, SPDX, and canonical-text audit."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess

HEAD = "f800a2bb920c543934d6286a47fe20dde3efa2c5"
BASE = "a4cbe41de1c80d43f26e0d348cbdb45075273a4f"
TREE = "f950b4f333aeb8b2cb267c7c2040645ff6f8050c"
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("repo", type=Path)
p.add_argument("packet", type=Path)
args = p.parse_args()
repo, packet = args.repo.resolve(), args.packet.resolve()

def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args])

def tree(ref):
    result = {}
    for record in git("ls-tree", "-rz", ref).split(b"\0"):
        if record:
            info, path = record.split(b"\t")
            result[path.decode()] = tuple(info.decode().split())
    return result

assert git("rev-parse", "HEAD").decode().strip() == HEAD
assert git("rev-parse", "HEAD^{tree}").decode().strip() == TREE
assert git("rev-list", "--count", BASE + ".." + HEAD).strip() == b"1"
assert git("rev-parse", HEAD + "^").decode().strip() == BASE
before, after = tree(BASE), tree(HEAD)
assert before.keys() == after.keys()
assert [name for name in after if after[name] != before[name]] == ["LICENSE"]
index = {}
for record in git("ls-files", "--stage", "-z").split(b"\0"):
    if record:
        info, path = record.split(b"\t")
        mode, oid, stage = info.decode().split()
        assert stage == "0"
        index[path.decode()] = (mode, oid)
assert index == {name: (row[0], row[2]) for name, row in after.items()}
headers = 0
gitlinks = []
for name, (mode, kind, oid) in after.items():
    path = repo / name
    if mode == "160000":
        gitlinks.append((name, oid))
        assert subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"]).decode().strip() == oid
        continue
    assert kind == "blob" and mode in ("100644", "100755")
    assert path.is_file() and not path.is_symlink()
    data = path.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual == oid, name
    assert bool(path.stat().st_mode & 0o111) == (mode == "100755"), name
    marker = "canonical LICENSE"
    if name != "LICENSE":
        lines = data.splitlines()
        header_line = 1 if lines[0].startswith(b"#!") else 0
        assert b"SPDX-License-Identifier: Apache-2.0" in lines[header_line], name
        assert before[name] == after[name]
        headers += 1
        marker = f"unchanged SPDX header line {header_line + 1}"
    print(f"PASS {mode} {oid} {name}: worktree bytes, index, mode; {marker}")

canonical = packet / "receipts/apache-LICENSE-2.0.txt"
license_data = (repo / "LICENSE").read_bytes()
base_license = git("show", BASE + ":LICENSE")
assert base_license == b"SPDX-License-Identifier: Apache-2.0\n\n" + license_data
result = subprocess.run(["cmp", str(repo / "LICENSE"), str(canonical)])
print(f"cmp LICENSE canonical: rc={result.returncode}")
assert result.returncode == 0
for name, data in [("LICENSE", license_data), ("canonical", canonical.read_bytes())]:
    print(f"SHA256 {name}: {hashlib.sha256(data).hexdigest()}; bytes={len(data)}")
hosted = json.loads((packet / "receipts/head-license.json").read_text())
assert hosted["sha"] == after["LICENSE"][2]
assert hosted["license"]["spdx_id"] == "Apache-2.0"
assert base64.b64decode(hosted["content"]) == license_data
print("PASS exact-head public license API: matching blob bytes and Apache-2.0 detection")
scratch = packet / "scratch/license-probes"
scratch.mkdir(parents=True, exist_ok=True)
variants = {
    "old-header": base_license,
    "missing-final-newline": license_data.rstrip(b"\n"),
    "crlf": license_data.replace(b"\n", b"\r\n"),
}
for name, data in variants.items():
    target = scratch / name
    target.write_bytes(data)
    rc = subprocess.run(["cmp", "-s", str(target), str(canonical)]).returncode
    print(f"PASS canonical negative control {name}: cmp rc={rc}, expected 1")
    assert rc == 1
assert git("diff", "--no-ext-diff", "--exit-code") == b""
assert git("diff", "--cached", "--no-ext-diff", "--exit-code", HEAD) == b""
print(f"Tracked files={len(after)}; unchanged non-LICENSE SPDX headers={headers}; gitlinks={gitlinks}")
print("No required submodule gitlinks or .gitmodules exist at this head." if not gitlinks else "Gitlinks verified.")
print("Status including untracked files:")
print(git("status", "--porcelain=v1", "--untracked-files=all").decode(), end="")
print("PASS audit complete")
