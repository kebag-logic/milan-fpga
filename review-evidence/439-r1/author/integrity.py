#!/usr/bin/env python3
"""Audit tracked bytes, kinds, modes and index against HEAD without trusting status."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
OUT = Path(__file__).resolve().parent
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
REQUIRED = {"protocol-processor", "gptp-processor", "third_party/verilog-axis"}

def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], env=ENV, check=True, capture_output=True).stdout

def inventory(root, revision):
    records = []
    problems = []
    for row in git(root, "ls-tree", "-rz", revision).split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        rel = name.decode()
        target = root / rel
        record = dict(path=rel, mode=mode, kind=kind, oid=oid)
        if kind == "commit":
            records.append(record)
            continue
        try:
            info = target.lstat()
            record.update(uid=info.st_uid, gid=info.st_gid, disk_mode=oct(stat.S_IMODE(info.st_mode)))
            if stat.S_ISLNK(info.st_mode):
                actual = os.fsencode(os.readlink(target))
                record["disk_kind"] = "symlink"
                actual_mode = "120000"
            elif stat.S_ISREG(info.st_mode):
                actual = target.read_bytes()
                record["disk_kind"] = "file"
                actual_mode = "100755" if info.st_mode & 0o111 else "100644"
            else:
                raise ValueError("unexpected file kind")
            blob = hashlib.sha1(b"blob " + str(len(actual)).encode() + b"\0" + actual).hexdigest()
            record.update(bytes=len(actual), sha256=hashlib.sha256(actual).hexdigest(), disk_blob=blob)
            if blob != oid or mode != actual_mode:
                problems.append(rel + ": bytes or kind/mode differ from " + revision)
        except (OSError, ValueError) as error:
            record["error"] = str(error)
            problems.append(rel + ": " + str(error))
        records.append(record)
    index = git(root, "ls-files", "--stage", "-z")
    expected = {(r["path"], r["mode"], r["oid"], "0") for r in records}
    actual_index = set()
    for row in index.split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, oid, stage = meta.decode().split()
            actual_index.add((name.decode(), mode, oid, stage))
    if actual_index != expected:
        problems.append("index differs from " + revision)
    return dict(records=records, index=index.decode(), index_flags=git(root, "ls-files", "-v", "-z").decode(), problems=problems)

root = Path.cwd()
head = git(root, "rev-parse", "HEAD").decode().strip()
report = dict(head=head, tree=git(root, "rev-parse", "HEAD^{tree}").decode().strip(),
              base="483a133ed08867ea0d300d2b4a027b5b48a4282f", branch=git(root, "branch", "--show-current").decode().strip(),
              default_ownership=dict(uid=os.getuid(), gid=os.getgid()), parent=inventory(root, head), submodules={})
for record in report["parent"]["records"]:
    if record["kind"] != "commit":
        continue
    rel = record["path"]
    item = dict(pin=record["oid"], required=rel in REQUIRED)
    report["submodules"][rel] = item
    if rel not in REQUIRED:
        item["state"] = "not required; not initialized by author"
        continue
    sub = root / rel
    item["head"] = git(sub, "rev-parse", "HEAD").decode().strip()
    item["git_dir"] = git(sub, "rev-parse", "--absolute-git-dir").decode().strip()
    item["superproject"] = git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip()
    item["git_file"] = (sub / ".git").read_text()
    item["inventory"] = inventory(sub, record["oid"])
    if item["head"] != item["pin"] or Path(item["superproject"]) != root:
        item["inventory"]["problems"].append("revision/registration mismatch")
path = OUT / (sys.argv[1] + "-integrity.json")
path.write_text(json.dumps(report, indent=2) + "\n")
problems = report["parent"]["problems"] + [f"{name}: {issue}" for name,item in report["submodules"].items() for issue in item.get("inventory",{}).get("problems",[])]
print(f"head={head} tree={report['tree']} tracked={len(report['parent']['records'])} required_pins={len(REQUIRED)} problems={problems!r}")
print(f"manifest={path} sha256={hashlib.sha256(path.read_bytes()).hexdigest()}")
sys.exit(bool(problems))
