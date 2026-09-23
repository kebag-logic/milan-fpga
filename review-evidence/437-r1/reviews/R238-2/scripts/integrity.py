#!/usr/bin/env python3
"""Review-clone integrity: HEAD and tree identity, every index record's blob
hashed from the bytes on disk, file kinds and modes, index == HEAD tree, no
assume-unchanged / skip-worktree flags, no untracked or ignored paths, and
the required submodules at their gitlinks.

Usage: integrity.py <clone> <expected-head> <expected-tree> <out.json>
"""
import json
import os
import stat
import subprocess
import sys

GIT_ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(repo, *args, raw=False):
    out = subprocess.run(["git", "-C", repo, *args], capture_output=True, check=True, env=GIT_ENV).stdout
    return out if raw else out.decode()


def main():
    repo, head, tree, out_path = sys.argv[1:5]
    report = {"head": git(repo, "rev-parse", "HEAD").strip(),
              "tree": git(repo, "rev-parse", "HEAD^{tree}").strip()}
    report["head_ok"] = report["head"] == head
    report["tree_ok"] = report["tree"] == tree
    records = [r for r in git(repo, "ls-files", "-s", "-z", raw=True).split(b"\0") if r]
    bad, counts, gitlinks = [], {"regular": 0, "executable": 0, "symlink": 0, "gitlink": 0}, {}
    for rec in records:
        meta, path = rec.split(b"\t", 1)
        mode, blob, stage = meta.decode().split()
        path = path.decode()
        full = os.path.join(repo, path)
        if stage != "0":
            bad.append(f"{path}: stage {stage}")
            continue
        if mode == "160000":
            counts["gitlink"] += 1
            gitlinks[path] = blob
            continue
        st = os.lstat(full)
        if mode == "120000":
            counts["symlink"] += 1
            ok = stat.S_ISLNK(st.st_mode)
            data = os.readlink(full).encode() if ok else b""
        else:
            counts["executable" if mode == "100755" else "regular"] += 1
            ok = stat.S_ISREG(st.st_mode) and bool(st.st_mode & 0o100) == (mode == "100755")
            data = open(full, "rb").read() if ok else b""
        actual = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True,
                                check=True).stdout.decode().strip() if ok else None
        if not ok or actual != blob:
            bad.append(f"{path}: mode {mode} kind/mode ok={ok} blob {blob} actual {actual}")
    report["records"] = len(records)
    report["counts"] = counts
    report["mismatches"] = bad
    report["index_vs_head"] = git(repo, "diff-index", "--cached", "--name-only", "HEAD")
    report["flags"] = sorted({line[:1] for line in git(repo, "ls-files", "-v").splitlines()})
    report["untracked_or_ignored"] = git(repo, "status", "--porcelain=v1", "--ignored", "-uall",
                                         "--ignore-submodules=none")
    subs = {}
    for path, blob in gitlinks.items():
        full = os.path.join(repo, path)
        if os.path.exists(os.path.join(full, ".git")):
            sub_head = git(full, "rev-parse", "HEAD").strip()
            subs[path] = {"gitlink": blob, "head": sub_head, "match": sub_head == blob,
                          "status": git(full, "status", "--porcelain=v1", "--ignored", "-uall")}
        else:
            subs[path] = {"gitlink": blob, "initialized": False}
    report["submodules"] = subs
    report["submodule_status"] = git(repo, "submodule", "status")
    report["ok"] = (report["head_ok"] and report["tree_ok"] and not bad and not report["index_vs_head"]
                    and report["flags"] == ["H"] and not report["untracked_or_ignored"]
                    and all(s.get("match", True) and not s.get("status") for s in subs.values()))
    json.dump(report, open(out_path, "w"), indent=1)
    print(json.dumps({k: report[k] for k in ("head_ok", "tree_ok", "records", "counts", "flags", "ok")}))
    print(report["submodule_status"], end="")


if __name__ == "__main__":
    main()
