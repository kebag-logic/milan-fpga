#!/usr/bin/env python3
"""Verify a review checkout is byte-exact at the assigned head.

Checks: HEAD and its tree; the index writes the same tree; every tracked entry's
worktree bytes hash to its index blob and its mode (regular, executable, symlink,
gitlink) matches; `git status --porcelain --ignored=no` is empty; and the gitlink
(submodule) inventory. usage: verify_state.py REPO HEAD_SHA TREE_SHA OUT.json
"""
import json
import os
import stat
import subprocess
import sys


def git(repo, *args, text=True):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True,
                          text=text).stdout


def main() -> int:
    repo, head, tree, out = sys.argv[1:5]
    rec = {"head": git(repo, "rev-parse", "HEAD").strip(),
           "head_tree": git(repo, "rev-parse", "HEAD^{tree}").strip(),
           "index_tree": git(repo, "write-tree").strip(),
           "status": git(repo, "status", "--porcelain"),
           "expected_head": head, "expected_tree": tree}
    entries = git(repo, "ls-files", "-s", "-z").split("\0")
    bad, gitlinks, n = [], [], 0
    for e in filter(None, entries):
        meta, path = e.split("\t", 1)
        mode, blob, _stage = meta.split()
        n += 1
        full = os.path.join(repo, path)
        if mode == "160000":
            gitlinks.append({"path": path, "commit": blob})
            continue
        st = os.lstat(full)
        if mode == "120000":
            ok_mode = stat.S_ISLNK(st.st_mode)
            data = os.readlink(full).encode()
        else:
            ok_mode = stat.S_ISREG(st.st_mode) and (
                bool(st.st_mode & 0o100) == (mode == "100755"))
            with open(full, "rb") as fh:
                data = fh.read()
        h = subprocess.run(["git", "hash-object", "--no-filters", "--stdin"], input=data,
                           capture_output=True, check=True).stdout.decode().strip()
        if h != blob or not ok_mode:
            bad.append({"path": path, "mode": mode, "blob": blob, "worktree_blob": h,
                        "mode_ok": ok_mode})
    rec.update({"tracked_entries": n, "mismatches": bad, "gitlinks": gitlinks})
    rec["verdict"] = ("EXACT" if (rec["head"] == head and rec["head_tree"] == tree
                                  and rec["index_tree"] == tree and not rec["status"]
                                  and not bad) else "DIFFERS")
    with open(out, "w") as fh:
        json.dump(rec, fh, indent=1)
        fh.write("\n")
    print(json.dumps({k: rec[k] for k in ("head", "head_tree", "index_tree", "tracked_entries",
                                          "verdict")} | {"mismatches": len(bad),
                                                          "gitlinks": len(gitlinks),
                                                          "status_empty": not rec["status"]}))
    return 0 if rec["verdict"] == "EXACT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
