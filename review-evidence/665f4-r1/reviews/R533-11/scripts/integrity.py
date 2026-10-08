#!/usr/bin/env python3
"""Prove tracked bytes, Git modes, stage-zero index and required dependency pins."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ROOT = Path.cwd()
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
HEAD = "b98eb2d5a21522bab3bc6bb943332cf8edf11893"
PACKET = Path(__file__).resolve().parents[1]

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=ENV)

def verify(root, expected):
    errors = []
    head = git(root, "rev-parse", "HEAD").decode().strip()
    if head != expected: errors.append("head mismatch")
    entries = {}
    count = 0
    links = {}
    for record in git(root, "ls-tree", "-rz", expected).split(b"\0"):
        if not record: continue
        meta, name = record.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        path = os.fsdecode(name)
        entries[path] = (mode, oid, "0")
        if kind == "commit":
            links[path] = oid
            continue
        f = root / path
        try:
            st = f.lstat()
            if mode == "120000":
                valid = stat.S_ISLNK(st.st_mode)
                data = os.fsencode(os.readlink(f)) if valid else b""
            else:
                valid = stat.S_ISREG(st.st_mode) and bool(st.st_mode & 0o111) == (mode == "100755")
                data = f.read_bytes() if stat.S_ISREG(st.st_mode) else b""
            actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if not valid or actual != oid: errors.append(path + ": bytes or mode differ")
        except OSError:
            errors.append(path + ": missing or unreadable")
        count += 1
    index = {}
    for record in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not record: continue
        meta, name = record.split(b"\t", 1)
        path = os.fsdecode(name)
        if path in index: errors.append(path + ": duplicate index entry")
        index[path] = tuple(meta.decode().split())
    if index != entries: errors.append("index differs from tree")
    hidden = [os.fsdecode(x) for x in git(root, "ls-files", "-v", "-z").split(b"\0")
              if x and (x[:1].islower() or x[:1] == b"S")]
    if hidden: errors.append("hidden index flags")
    return {"head": head, "tree": git(root, "rev-parse", expected+"^{tree}").decode().strip(),
            "tracked_blobs": count, "bytes_modes_index_match": not errors,
            "hidden_index_flags": hidden, "gitlinks": links, "errors": errors}

result = {"parent": verify(ROOT, HEAD), "dependencies": {}}
for path in ("protocol-processor", "gptp-processor", "third_party/lwSRP", "third_party/verilog-axis"):
    result["dependencies"][path] = verify(ROOT / path, result["parent"]["gitlinks"][path])
result["builder_to_head_diff"] = git(ROOT, "diff", "803e8c3c9e7506c4f004d562437ae4f374fbad8e", HEAD).decode()
result["protected_changes_from_source_base"] = git(ROOT, "diff", "--name-only",
    "d8b355fe0f41d49dca6cae1cd8b3826e2edde364", HEAD, "hdl", "sw/mailbox", "configs", "sw/litex").decode().splitlines()
result["status"] = git(ROOT, "status", "--porcelain=v1").decode()
(PACKET / "receipts/integrity.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
raise SystemExit(int(any(x["errors"] for x in [result["parent"], *result["dependencies"].values()])))
