#!/usr/bin/env python3
"""Review-clone integrity: HEAD and tree are the exact head, the index equals
the HEAD tree, every tracked regular/executable blob on disk hashes to its
recorded object id with the recorded mode, nothing is untracked or ignored,
and the required submodules sit at their gitlinks.

Usage: integrity.py <clone> <commit> <tree> > integrity.json
"""
import json
import os
import stat
import subprocess
import sys


def git(clone: str, *args: str) -> str:
    return subprocess.run(["git", "-C", clone, *args], capture_output=True, check=True,
                          env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}).stdout.decode()


def main() -> int:
    clone, commit, tree = sys.argv[1:4]
    out = {"head": git(clone, "rev-parse", "HEAD").strip(),
           "tree": git(clone, "rev-parse", "HEAD^{tree}").strip()}
    out["head_ok"] = out["head"] == commit and out["tree"] == tree
    out["index_tree"] = git(clone, "write-tree").strip()
    out["index_equals_head_tree"] = out["index_tree"] == tree
    entries = [l.split("\t", 1) for l in git(clone, "ls-tree", "-r", "-z", "--full-tree", "HEAD").split("\0") if l]
    bad, counts = [], {"100644": 0, "100755": 0, "160000": 0, "120000": 0}
    for meta, path in entries:
        mode, kind, oid = meta.split()
        counts[mode] = counts.get(mode, 0) + 1
        full = os.path.join(clone, path)
        if mode in ("100644", "100755"):
            st = os.lstat(full)
            disk = subprocess.run(["git", "-C", clone, "hash-object", "--no-filters", "--", path],
                                  capture_output=True, check=True).stdout.decode().strip()
            exe = bool(st.st_mode & stat.S_IXUSR)
            if disk != oid or exe != (mode == "100755") or not stat.S_ISREG(st.st_mode):
                bad.append([path, mode, oid, disk, exe])
        elif mode == "160000":
            if os.path.isdir(os.path.join(full, ".git")) or os.path.isfile(os.path.join(full, ".git")):
                sub = subprocess.run(["git", "-C", full, "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()
                dirty = subprocess.run(["git", "-C", full, "status", "--porcelain"], capture_output=True).stdout.decode()
                out.setdefault("submodules", {})[path] = {"gitlink": oid, "checkout": sub,
                                                          "at_pin": sub == oid, "clean": dirty == ""}
            else:
                out.setdefault("submodules", {})[path] = {"gitlink": oid, "checkout": None}
    flags = {l[:1] for l in git(clone, "ls-files", "-v").splitlines()}
    out["ls_files_flags"] = sorted(flags)
    out["status_porcelain_ignored"] = git(clone, "status", "--porcelain", "--ignored")
    out["entry_counts"] = counts
    out["blob_mismatches"] = bad
    req = ("third_party/verilog-axis", "protocol-processor", "gptp-processor")
    subs = out.get("submodules", {})
    out["required_submodules_ok"] = all(subs.get(r, {}).get("at_pin") and subs.get(r, {}).get("clean") for r in req)
    out["verdict"] = ("PASS" if out["head_ok"] and out["index_equals_head_tree"] and not bad
                      and flags <= {"H"} and out["status_porcelain_ignored"] == ""
                      and out["required_submodules_ok"] else "FAIL")
    json.dump(out, sys.stdout, indent=1)
    print()
    return 0 if out["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
