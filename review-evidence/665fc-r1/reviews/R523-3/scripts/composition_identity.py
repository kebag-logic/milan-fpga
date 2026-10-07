#!/usr/bin/env python3
"""Read-only, portable composition and raw checkout identity receipt."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
HEAD = "64e62816ad21791f6df3657fadb935aec5555881"
PARENT = "af5be4710c3516cc247c353213d6939fa8d23f57"
SOURCE = "db9aa8c9b135b34ff3d070a979dee70440b37cc6"
DEV = "910f338dbd050f4efd2d96991ddcf928a583d55f"
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(*args, root=ROOT):
    return subprocess.check_output(["git", "-c", "core.commitGraph=false", "-C", str(root), *args], env=ENV)

def entries(rev, root=ROOT):
    result = {}
    for row in git("ls-tree", "-rz", rev, root=root).split(b"\0"):
        if row:
            metadata, name = row.split(b"\t", 1)
            result[os.fsdecode(name)] = tuple(metadata.decode().split())
    return result

def verify_checkout(root, rev):
    tree = entries(rev, root)
    index = {}
    errors = []
    for row in git("ls-files", "--stage", "-z", root=root).split(b"\0"):
        if row:
            metadata, name = row.split(b"\t", 1)
            mode, oid, stage = metadata.decode().split()
            index.setdefault(os.fsdecode(name), []).append((mode, oid, stage))
    for name, (mode, kind, oid) in tree.items():
        if index.get(name) != [(mode, oid, "0")]:
            errors.append(f"index mismatch: {name}")
        if kind == "commit":
            continue
        path = root / name
        try:
            info = path.lstat()
            if mode == "120000":
                assert stat.S_ISLNK(info.st_mode)
                data = os.fsencode(os.readlink(path))
            else:
                assert stat.S_ISREG(info.st_mode)
                assert bool(info.st_mode & 0o111) == (mode == "100755")
                data = path.read_bytes()
            digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if digest != oid:
                errors.append(f"blob mismatch: {name}")
        except (OSError, AssertionError):
            errors.append(f"missing or wrong file kind/mode: {name}")
    errors.extend(f"extra index entry: {name}" for name in index.keys() - tree.keys())
    assert not errors, errors
    return {"entries": len(tree), "blobs_verified": sum(v[1] == "blob" for v in tree.values()), "index_modes_bytes": "PASS"}

assert git("rev-parse", "HEAD").decode().strip() == HEAD
assert git("rev-parse", "HEAD^{tree}").decode().strip() == "ad770db1dba7d8214d909589a1b93db51a1b5bd0"
assert git("show", "-s", "--format=%P", HEAD).decode().strip().split() == [PARENT, SOURCE]
base = git("merge-base", PARENT, SOURCE).decode().strip()
trees = {r: entries(r) for r in (base, PARENT, SOURCE, HEAD)}

def changed(a, b):
    return {p for p in trees[a].keys() | trees[b].keys() if trees[a].get(p) != trees[b].get(p)}

source_paths = changed(base, SOURCE)
predecessor_paths = changed(base, PARENT)
candidate_paths = changed(PARENT, HEAD)
overlap = source_paths & predecessor_paths
assert overlap == {"sw/firmware/ctrl/README.md", "sw/firmware/gtest/README.md"}
assert len(source_paths) == len(candidate_paths) == 37
outside = sorted(p for p in trees[PARENT].keys() | trees[HEAD].keys() if p not in source_paths and trees[PARENT].get(p) != trees[HEAD].get(p))
unexpected = sorted(p for p in source_paths - overlap if trees[SOURCE].get(p) != trees[HEAD].get(p))
assert not outside and not unexpected
parent_tree = git("rev-parse", PARENT + "^{tree}").decode().strip()
dev_tree = git("rev-parse", DEV + "^{tree}").decode().strip()
assert parent_tree == dev_tree
pins = {}
for name in ("third_party/verilog-axis", "protocol-processor", "gptp-processor"):
    mode, kind, oid = trees[HEAD][name]
    assert mode == "160000" and kind == "commit"
    sub = ROOT / name
    assert not sub.is_symlink() and (sub / ".git").is_file()
    assert git("rev-parse", "HEAD", root=sub).decode().strip() == oid
    assert Path(git("rev-parse", "--show-superproject-working-tree", root=sub).decode().strip()).resolve() == ROOT
    pins[name] = {"pin": oid, **verify_checkout(sub, oid)}

print(json.dumps({
    "head": HEAD, "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
    "ordered_parents": git("show", "-s", "--format=%P", HEAD).decode().strip().split(),
    "source": SOURCE, "source_base": base, "composition_parent": PARENT,
    "live_dev_recorded": DEV, "parent_and_recorded_dev_tree": parent_tree,
    "source_changed_paths": sorted(source_paths), "predecessor_changed_paths": sorted(predecessor_paths),
    "candidate_changed_paths": sorted(candidate_paths), "overlap": sorted(overlap),
    "nonoverlap_source_entry_mismatches": unexpected, "non_source_path_changes": outside,
    "source_identical_files": sorted(source_paths - overlap),
    "superproject": verify_checkout(ROOT, HEAD), "submodules": pins,
}, indent=2))
