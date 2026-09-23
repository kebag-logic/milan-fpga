"""Verify the review clone is byte-identical to the exact head.

Checks, without trusting index flags: HEAD/tree identity; every tracked root
file's on-disk bytes hash to the HEAD blob with the HEAD mode; the index equals
HEAD at stage 0; porcelain status is clean; each required submodule is a real
directory whose HEAD equals the root gitlink, whose status is clean, and whose
tracked files hash to their committed blobs.

Usage: integrity.py <clone> <expected-head> <expected-tree>
"""
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

REQUIRED = ("third_party/verilog-axis", "protocol-processor", "gptp-processor")


def git(cwd, *args, data=None):
    r = subprocess.run(("git", "--no-replace-objects", *args), cwd=cwd, input=data,
                       capture_output=True)
    if r.returncode:
        raise SystemExit(f"git {args!r} in {cwd}: {r.stderr!r}")
    return r.stdout


def tracked(cwd, rev):
    """{path_bytes: (mode, type, oid)} from ls-tree -r -z at rev."""
    out = {}
    for rec in git(cwd, "ls-tree", "-r", "-z", "--full-tree", rev).split(b"\0"):
        if not rec:
            continue
        meta, name = rec.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        out[name] = (mode, kind, oid)
    return out


def disk_check(cwd, entries):
    bad = []
    blobs = [(n, e) for n, e in entries.items() if e[1] == "blob"]
    for name, (mode, _, oid) in blobs:
        p = Path(os.fsdecode(cwd.encode() if isinstance(cwd, str) else cwd)) / os.fsdecode(name)
        st = os.lstat(p)
        if mode == "120000":
            data, ok_kind = os.readlink(p).encode(), stat.S_ISLNK(st.st_mode)
            disk_mode = "120000"
        else:
            data, ok_kind = p.read_bytes(), stat.S_ISREG(st.st_mode)
            disk_mode = "100755" if st.st_mode & 0o111 else "100644"
        got = git(cwd, "hash-object", "--no-filters", "--stdin", data=data).strip().decode()
        if not ok_kind or got != oid or disk_mode != mode:
            bad.append([os.fsdecode(name), mode, disk_mode, oid, got])
    return len(blobs), bad


def main():
    clone, head, tree = sys.argv[1:4]
    res = {"head": git(clone, "rev-parse", "HEAD").strip().decode(),
           "tree": git(clone, "rev-parse", "HEAD^{tree}").strip().decode()}
    res["head_ok"] = res["head"] == head and res["tree"] == tree
    root = tracked(clone, "HEAD")
    n, bad = disk_check(clone, root)
    res["root_blobs_checked"], res["root_mismatches"] = n, bad
    idx = git(clone, "ls-files", "-s", "-z").split(b"\0")
    index = {}
    for rec in idx:
        if rec:
            meta, name = rec.split(b"\t", 1)
            mode, oid, stage = meta.decode().split()
            index[name] = (mode, oid, stage)
    res["index_equals_head"] = (set(index) == set(root) and all(
        index[k][0] == root[k][0] and index[k][1] == root[k][2] and index[k][2] == "0"
        for k in root))
    res["status_porcelain"] = git(clone, "status", "--porcelain=v1", "--ignore-submodules=none").decode()
    subs = {}
    for sub in REQUIRED:
        gitlink = root[sub.encode()]
        path = Path(clone) / sub
        info = {"gitlink": gitlink[2], "is_dir": path.is_dir() and not path.is_symlink()}
        info["head"] = git(path, "rev-parse", "HEAD").strip().decode()
        info["status"] = git(path, "status", "--porcelain=v1").decode()
        entries = tracked(str(path), "HEAD")
        info["files_checked"], info["mismatches"] = disk_check(str(path), entries)
        info["ok"] = (info["is_dir"] and info["head"] == gitlink[2] and not info["status"]
                      and not info["mismatches"])
        subs[sub] = info
    res["submodules"] = subs
    res["ALL_OK"] = (res["head_ok"] and not bad and res["index_equals_head"]
                     and not res["status_porcelain"] and all(s["ok"] for s in subs.values()))
    print(json.dumps(res, indent=1))
    return 0 if res["ALL_OK"] else 1


if __name__ == "__main__":
    sys.exit(main())
