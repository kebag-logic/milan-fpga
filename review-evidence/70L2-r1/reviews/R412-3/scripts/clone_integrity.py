#!/usr/bin/env python3
"""Verify a review clone is byte-for-byte its exact head (read-only).

usage: clone_integrity.py <clone> <expected-head>

Checks: HEAD and the index tree equal the head's commit and tree; `git status`
reports nothing, untracked and ignored included; no index entry carries the
assume-unchanged or skip-worktree bit; every index entry equals the head
tree's (path, mode, blob); every tracked file's bytes hash to its blob and its
executable bit matches its mode (symlinks by target); every gitlink is the
checked-out, clean commit of its submodule (or uninitialised, reported).
Prints one line per check and `INTEGRITY OK` or `INTEGRITY FAILED`."""
import os
import subprocess
import sys

clone, expected = sys.argv[1], sys.argv[2]
env = {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1", "LC_ALL": "C"}


def git(*args, cwd=clone, data=None):
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True,
                          capture_output=True, input=data).stdout


ok = True


def check(label, good, detail=""):
    global ok
    ok = ok and good
    print(f"{'ok  ' if good else 'FAIL'} {label}{': ' + detail if detail else ''}")


head = git("rev-parse", "HEAD").decode().strip()
check("HEAD is the expected head", head == expected, head)
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
check("index tree equals HEAD tree", git("write-tree").decode().strip() == tree, tree)
status = git("status", "--porcelain=v2", "--ignored", "--untracked-files=all").decode()
check("status empty (untracked and ignored included)", status == "", status[:300])
flags = [line for line in git("ls-files", "-v").decode().splitlines()
         if not line.startswith("H ")]
check("no assume-unchanged / skip-worktree entries", not flags, str(flags[:5]))
index = {}
for line in git("ls-files", "-s", "-z").decode().split("\0"):
    if line:
        meta, path = line.split("\t", 1)
        mode, blob, stage = meta.split()
        index[path] = (mode, blob, stage)
head_tree = {}
for line in git("ls-tree", "-r", "-z", "HEAD").decode().split("\0"):
    if line:
        meta, path = line.split("\t", 1)
        mode, _kind, blob = meta.split()
        head_tree[path] = (mode, blob, "0")
check("index equals HEAD tree by path, mode, blob and stage", index == head_tree,
      f"{len(index)} entries")
bad = []
paths = [p for p, (mode, _b, _s) in index.items() if mode != "160000"]
for path in paths:
    mode, blob, _ = index[path]
    full = os.path.join(clone, path)
    if mode == "120000":
        if not os.path.islink(full):
            bad.append(("not a symlink", path))
            continue
        data = os.readlink(full).encode()
    else:
        if os.path.islink(full) or not os.path.isfile(full):
            bad.append(("not a regular file", path))
            continue
        with open(full, "rb") as handle:
            data = handle.read()
        executable = bool(os.stat(full).st_mode & 0o111)
        if executable != (mode == "100755"):
            bad.append(("mode", path))
    got = git("hash-object", "--stdin", "--no-filters", data=data).decode().strip()
    if got != blob:
        bad.append(("bytes", path))
check("every tracked file hashes to its blob with its mode", not bad,
      f"{len(paths)} files; {bad[:5]}")
for path, (mode, blob, _) in sorted(index.items()):
    if mode != "160000":
        continue
    full = os.path.join(clone, path)
    if not os.path.exists(os.path.join(full, ".git")):
        print(f"info {path}: gitlink {blob}, submodule not initialised")
        continue
    sub_head = git("rev-parse", "HEAD", cwd=full).decode().strip()
    dirty = git("status", "--porcelain", "--untracked-files=all", cwd=full).decode()
    check(f"submodule {path} at its gitlink and clean",
          sub_head == blob and dirty == "", f"{sub_head} dirty={len(dirty.splitlines())}")
print("INTEGRITY OK" if ok else "INTEGRITY FAILED")
sys.exit(0 if ok else 1)
