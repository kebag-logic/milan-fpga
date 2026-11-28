#!/usr/bin/env python3
"""Round R958-7: the review clone still holds the exact head's bytes.

Usage: python3 -I verify_checkout.py <superproject-clone>

For the superproject and each initialised submodule: every index entry's
working file is re-hashed with `git hash-object` and its mode compared; the
index tree is compared with HEAD's tree; untracked and modified paths are
counted; each submodule HEAD is compared with the superproject gitlink. An
uninitialised submodule keeps its gitlink and is reported as such. Read-only
apart from git's own object lookups.
"""
import os
import stat
import subprocess
import sys

REPO = os.path.abspath(sys.argv[1])
HEAD = "25132e3029557d2d992dc42f2a77c6840e5c05d3"
TREE = "222e3e20fa0f6313632775aabf4f74a26c4417fc"


def git(cwd, *args, data=None):
    return subprocess.run(["git", "-C", cwd, *args], check=True, capture_output=True, input=data).stdout


def check_repo(cwd, label):
    bad = 0
    entries = git(cwd, "ls-files", "-s", "-z").split(b"\0")[:-1]
    files, links = [], []
    for entry in entries:
        meta, path = entry.split(b"\t", 1)
        mode, sha, _stage = meta.split()
        (links if mode == b"160000" else files).append((mode.decode(), sha.decode(), path))
    regular = [f for f in files if f[0] != "120000"]
    hashes = git(cwd, "hash-object", "--no-filters", "--stdin-paths",
                 data=b"\n".join(p for _m, _s, p in regular) + b"\n").decode().split()
    for (mode, sha, path), got in zip(regular, hashes):
        st = os.lstat(os.path.join(cwd.encode(), path))
        want_x = mode == "100755"
        if got != sha or bool(st.st_mode & stat.S_IXUSR) != want_x or not stat.S_ISREG(st.st_mode):
            bad += 1
            print(f"  MISMATCH {label}:{path.decode()}")
    for mode, sha, path in (f for f in files if f[0] == "120000"):
        full = os.path.join(cwd.encode(), path)
        got = git(cwd, "hash-object", "--stdin", data=os.readlink(full)).decode().strip() if os.path.islink(full) else ""
        if got != sha:
            bad += 1
            print(f"  MISMATCH symlink {label}:{path.decode()}")
    dirty = [ln for ln in git(cwd, "status", "--porcelain", "--untracked-files=all",
                              "--ignore-submodules=none").decode().split("\n") if ln]
    index_tree = git(cwd, "write-tree").decode().strip()
    head_tree = git(cwd, "rev-parse", "HEAD^{tree}").decode().strip()
    ok = bad == 0 and not dirty and index_tree == head_tree
    print(f"{'PASS' if ok else 'FAIL'} {label}: {len(files)} blobs re-hashed, {bad} mismatched, "
          f"{len(dirty)} status lines, index tree {'==' if index_tree == head_tree else '!='} HEAD tree")
    return ok, links


def main():
    all_ok = True
    head = git(REPO, "rev-parse", "HEAD").decode().strip()
    tree = git(REPO, "rev-parse", "HEAD^{tree}").decode().strip()
    print(f"{'PASS' if (head, tree) == (HEAD, TREE) else 'FAIL'} superproject HEAD {head} tree {tree}")
    all_ok &= (head, tree) == (HEAD, TREE)
    ok, links = check_repo(REPO, "superproject")
    all_ok &= ok
    for _mode, sha, path in links:
        sub = os.path.join(REPO, path.decode())
        if not os.path.exists(os.path.join(sub, ".git")):
            print(f"INFO {path.decode()}: not initialised; gitlink {sha} preserved in the index")
            continue
        sub_head = git(sub, "rev-parse", "HEAD").decode().strip()
        same = sub_head == sha
        print(f"{'PASS' if same else 'FAIL'} {path.decode()}: HEAD {sub_head} {'==' if same else '!='} gitlink")
        ok, _ = check_repo(sub, path.decode())
        all_ok &= ok and same
    print(f"RESULT {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
