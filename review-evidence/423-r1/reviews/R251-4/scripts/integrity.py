#!/usr/bin/env python3
"""Verify a review clone is exactly the reviewed commit, byte for byte.

Usage: integrity.py <clone> <head-oid> <tree-oid>

Checks HEAD and its tree; hashes every tracked root blob from disk (symlinks
by target bytes) against the committed object ID and mode; requires the index
to equal HEAD at stage 0 with no assume-unchanged/skip-worktree flags and an
empty porcelain status; for each required submodule checks the gitlink, that
the checkout is a real initialized repository at that revision, and hashes
every tracked file against the pinned tree.  Prints JSON; exit 0 only if all
checks pass.
"""

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

REQUIRED = ("third_party/verilog-axis", "protocol-processor", "gptp-processor")


def git(repo, *args):
    r = subprocess.run(("git", "-C", str(repo), "--no-replace-objects", *args), capture_output=True)
    if r.returncode:
        raise RuntimeError(f"git {args!r}: {r.stderr!r}")
    return r.stdout


def blob_oid(data, fmt):
    h = hashlib.sha1() if fmt == "sha1" else hashlib.sha256()
    h.update(b"blob %d\0" % len(data) + data)
    return h.hexdigest()


def verify_tree(repo, rev, skip_gitlinks=True):
    fmt = git(repo, "rev-parse", "--show-object-format").decode().strip()
    bad, count = [], 0
    for rec in git(repo, "ls-tree", "-r", "-z", "--full-tree", rev).split(b"\0"):
        if not rec:
            continue
        meta, name = rec.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        if kind == "commit":
            continue
        path = Path(repo) / os.fsdecode(name)
        count += 1
        try:
            st = os.lstat(path)
        except OSError as exc:
            bad.append([os.fsdecode(name), f"missing: {exc}"])
            continue
        if mode == "120000":
            ok_type = stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(path)) if ok_type else b""
        else:
            ok_type = stat.S_ISREG(st.st_mode)
            data = path.read_bytes() if ok_type else b""
            exe = bool(st.st_mode & stat.S_IXUSR)
            if ok_type and exe != (mode == "100755"):
                bad.append([os.fsdecode(name), f"mode {mode} but executable={exe}"])
        if not ok_type:
            bad.append([os.fsdecode(name), "wrong file type"])
        elif blob_oid(data, fmt) != oid:
            bad.append([os.fsdecode(name), "content hash mismatch"])
    return count, bad


def main():
    clone, head, tree = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    res = {"clone_head": git(clone, "rev-parse", "HEAD").decode().strip(),
           "clone_tree": git(clone, "rev-parse", "HEAD^{tree}").decode().strip()}
    res["head_ok"] = res["clone_head"] == head and res["clone_tree"] == tree
    count, bad = verify_tree(clone, "HEAD")
    res["root_blobs"], res["root_bad"] = count, bad
    diff_index = git(clone, "diff-index", "--cached", "--no-renames", "HEAD").decode()
    stages = [ln for ln in git(clone, "ls-files", "-s").decode().splitlines() if ln.split()[2] != "0"]
    #! ls-files -v prints H for an ordinary tracked file; anything else
    #! (h assume-unchanged, S skip-worktree, ...) can hide a local edit.
    flagged = [ln for ln in git(clone, "ls-files", "-v").decode().splitlines()
               if ln[:1] != "H"]
    res["index_equals_head"] = diff_index == "" and not stages
    res["index_flags"] = flagged[:10]
    res["status"] = git(clone, "status", "--porcelain=v1", "--ignore-submodules=none").decode().splitlines()
    subs = {}
    for sub in REQUIRED:
        entry = git(clone, "ls-tree", "HEAD", "--", sub).decode().split()
        pin = entry[2] if entry and entry[0] == "160000" else None
        p = clone / sub
        info = {"gitlink": pin, "is_dir": p.is_dir() and not p.is_symlink()}
        try:
            info["checkout_head"] = git(p, "rev-parse", "HEAD").decode().strip()
            info["toplevel_ok"] = Path(git(p, "rev-parse", "--show-toplevel").decode().strip()).resolve() == p.resolve()
            n, b = verify_tree(p, pin)
            info["files"], info["bad"] = n, b
            info["status"] = git(p, "status", "--porcelain=v1").decode().splitlines()
        except Exception as exc:  # recorded, counted as failure
            info["error"] = str(exc)
        info["ok"] = (pin is not None and info.get("checkout_head") == pin and info.get("toplevel_ok")
                      and info["is_dir"] and not info.get("bad") and not info.get("status")
                      and "error" not in info)
        subs[sub] = info
    res["submodules"] = subs
    res["ALL_OK"] = (res["head_ok"] and not bad and res["index_equals_head"] and not flagged
                     and not res["status"] and all(s["ok"] for s in subs.values()))
    print(json.dumps(res, indent=1))
    return 0 if res["ALL_OK"] else 1


if __name__ == "__main__":
    sys.exit(main())
