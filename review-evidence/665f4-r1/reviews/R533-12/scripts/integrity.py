#!/usr/bin/env python3
"""Verify commit blobs, modes, stage-zero index and required gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument("--repo", type=Path, required=True)
a = p.parse_args()
repo = a.repo.resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env)

def check(root, commit):
    records = git(root, "ls-tree", "-rz", "--full-tree", commit).split(b"\0")
    expected_index = {}
    findings = []
    count = 0
    links = {}
    for record in records:
        if not record:
            continue
        meta, rawpath = record.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        path = os.fsdecode(rawpath)
        expected_index[path] = (mode, oid, "0")
        full = root / path
        if kind == "commit":
            links[path] = oid
            continue
        try:
            st = full.lstat()
            if mode == "120000":
                assert stat.S_ISLNK(st.st_mode)
                data = os.fsencode(os.readlink(full))
            else:
                assert stat.S_ISREG(st.st_mode)
                assert bool(st.st_mode & 0o111) == (mode == "100755")
                data = full.read_bytes()
            actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            assert actual == oid
            count += 1
        except (OSError, AssertionError):
            findings.append("blob or mode mismatch: " + path)
    actual_index = {}
    for record in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if record:
            meta, path = record.split(b"\t", 1)
            key = os.fsdecode(path)
            if key in actual_index:
                findings.append("duplicate index stage: " + key)
            actual_index[key] = tuple(meta.decode().split())
    if actual_index != expected_index:
        findings.append("index differs from commit tree")
    for record in git(root, "ls-files", "-v", "-z").split(b"\0"):
        if record and (record[:1].islower() or record[:1] == b"S"):
            findings.append("hidden index flag: " + os.fsdecode(record))
    head = git(root, "rev-parse", "HEAD").decode().strip()
    if head != commit:
        findings.append("HEAD mismatch")
    return {"commit": commit, "head": head, "checked_blobs": count,
            "gitlinks": links, "findings": findings}

head = "efea74858dffc482820d4f19c26c38796a57ff75"
result = {"parent": check(repo, head), "dependencies": {}}
for path in ("protocol-processor", "gptp-processor", "third_party/verilog-axis", "third_party/lwSRP"):
    pin = result["parent"]["gitlinks"][path]
    result["dependencies"][path] = check(repo / path, pin)
result["tree"] = git(repo, "rev-parse", "HEAD^{tree}").decode().strip()
result["external"] = "Historical unused import is uninitialized; gitlink verified in parent index."
result["status"] = git(repo, "status", "--porcelain=v1").decode()
result["passed"] = (not result["status"] and result["tree"] == "4e28d2409425b352c51d79526e4b48d6c93a38b7"
                    and not result["parent"]["findings"]
                    and all(not d["findings"] for d in result["dependencies"].values()))
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["passed"] else 1)
