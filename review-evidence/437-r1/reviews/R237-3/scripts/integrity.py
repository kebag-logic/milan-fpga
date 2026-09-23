#!/usr/bin/env python3
"""Review-clone integrity at the exact head.

Usage: integrity.py <clone> <head-sha> <out.json>
Checks: HEAD is <head-sha>; every tracked blob's working bytes hash to the
tree's blob id and its mode (regular / executable / symlink) matches; the
index holds exactly the tree's entries at stage 0 with no assume-unchanged
or skip-worktree flag; `git status --porcelain --ignored` is empty; each
gitlink's checkout is at the recorded commit with a clean worktree, or is
uninitialised (reported, not failed, for `external`).
"""
import json
import os
import stat
import subprocess
import sys


def git(repo: str, *args: str) -> str:
    return subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, check=True).stdout


def main() -> int:
    repo, head, out_path = sys.argv[1:4]
    problems, counts = [], {"blob": 0, "exec": 0, "symlink": 0, "gitlink": 0}
    if git(repo, "rev-parse", "HEAD").strip() != head:
        problems.append("HEAD is not the exact head")
    tree = {}
    for line in git(repo, "ls-tree", "-r", "--full-tree", "HEAD").splitlines():
        meta, path = line.split("\t", 1)
        mode, kind, oid = meta.split()
        tree[path] = (mode, kind, oid)
    index = {}
    for line in git(repo, "ls-files", "-s").splitlines():
        meta, path = line.split("\t", 1)
        mode, oid, st = meta.split()
        index.setdefault(path, []).append((mode, oid, st))
    if set(index) != set(tree):
        problems.append(f"index and tree paths differ: {sorted(set(index) ^ set(tree))[:5]}")
    for path, (mode, kind, oid) in tree.items():
        if index.get(path) != [(mode, oid, "0")]:
            problems.append(f"index record differs: {path}")
        full = os.path.join(repo, path)
        if kind == "commit":
            counts["gitlink"] += 1
            continue
        st = os.lstat(full)
        if mode == "120000":
            counts["symlink"] += 1
            ok = stat.S_ISLNK(st.st_mode) and git(repo, "hash-object", "--stdin") is not None
            target = os.readlink(full).encode()
            got = subprocess.run(["git", "-C", repo, "hash-object", "--stdin"], input=target,
                                 capture_output=True, check=True).stdout.decode().strip()
            if not ok or got != oid:
                problems.append(f"symlink differs: {path}")
            continue
        counts["exec" if mode == "100755" else "blob"] += 1
        if not stat.S_ISREG(st.st_mode) or bool(st.st_mode & stat.S_IXUSR) != (mode == "100755"):
            problems.append(f"mode or kind differs: {path}")
    # one batch hash of every regular file's working bytes (no filters)
    regular = [p for p, (m, k, _) in tree.items() if k == "blob" and m != "120000"]
    hashed = subprocess.run(["git", "-C", repo, "hash-object", "--no-filters", "--stdin-paths"],
                            input="\n".join(regular) + "\n", capture_output=True, text=True,
                            check=True).stdout.split()
    for path, got in zip(regular, hashed):
        if got != tree[path][2]:
            problems.append(f"bytes differ: {path}")
    flags = {l[0] for l in git(repo, "ls-files", "-v").splitlines()}
    if flags - {"H", "S"} or "S" in flags:
        problems.append(f"index flags other than H: {sorted(flags)}")
    status = git(repo, "status", "--porcelain", "--ignored", "--ignore-submodules=none")
    subs = {}
    for path, (mode, kind, oid) in tree.items():
        if kind != "commit":
            continue
        full = os.path.join(repo, path)
        try:
            at = git(full, "rev-parse", "HEAD").strip()
            top = git(full, "rev-parse", "--show-toplevel").strip()
            dirty = git(full, "status", "--porcelain")
            initialised = os.path.realpath(top) == os.path.realpath(full)
        except subprocess.CalledProcessError:
            at, dirty, initialised = None, "", False
        subs[path] = {"gitlink": oid, "checkout": at if initialised else None,
                      "clean": initialised and not dirty}
        if initialised and (at != oid or dirty):
            problems.append(f"submodule not at its gitlink or dirty: {path}")
        if not initialised and path != "external":
            problems.append(f"required submodule not initialised: {path}")
    result = {"head": head, "counts": counts, "entries": len(tree),
              "status_porcelain_ignored": status, "submodules": subs, "problems": problems}
    json.dump(result, open(out_path, "w"), indent=1)
    print(json.dumps({k: v for k, v in result.items() if k != "status_porcelain_ignored"}, indent=1))
    print("status lines:", len(status.splitlines()))
    return 1 if problems or status.strip() else 0


if __name__ == "__main__":
    sys.exit(main())
