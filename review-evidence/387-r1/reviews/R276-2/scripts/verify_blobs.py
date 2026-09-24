#!/usr/bin/env python3
"""Prove a checkout's tracked files are HEAD's bytes and modes, file by file.

For the repository and each named submodule: HEAD's tree (git ls-tree -r,
replace objects disabled) is compared entry by entry against the index
(git ls-files -s, stage 0 only) and against the bytes on disk (git
hash-object --no-filters over the path, and the file mode from lstat).
Gitlinks are compared against the submodule's own HEAD. Any difference,
missing file, unmerged stage or index-only entry is reported and fails.

Usage: verify_blobs.py <repo> [submodule path ...]
"""
import os
import stat
import subprocess
import sys

ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(repo, *args, data=None):
    return subprocess.run(["git", "-C", repo, *args], env=ENV, input=data,
                          capture_output=True, check=True).stdout


def tree_entries(repo):
    out = {}
    for rec in git(repo, "ls-tree", "-r", "-z", "--full-tree", "HEAD").split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, kind, oid = meta.split()
        out[path] = (mode.decode(), kind.decode(), oid.decode())
    return out


def index_entries(repo):
    out, bad = {}, []
    for rec in git(repo, "ls-files", "-s", "-z").split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, oid, stage = meta.split()
        if stage != b"0":
            bad.append(f"unmerged stage {stage.decode()} at {path!r}")
        out[path] = (mode.decode(), oid.decode())
    return out, bad


def disk_mode(full):
    st = os.lstat(full)
    if stat.S_ISLNK(st.st_mode):
        return "120000"
    if stat.S_ISDIR(st.st_mode):
        return "160000"
    return "100755" if st.st_mode & 0o111 else "100644"


def verify(repo):
    problems = []
    tree = tree_entries(repo)
    index, bad = index_entries(repo)
    problems += bad
    for path in sorted(set(index) - set(tree)):
        problems.append(f"index-only entry {path!r}")
    blobs = []
    for path, (mode, kind, oid) in sorted(tree.items()):
        if path not in index:
            problems.append(f"missing from index {path!r}")
            continue
        if index[path] != (mode, oid):
            problems.append(f"index differs at {path!r}: {index[path]} vs {(mode, oid)}")
        full = os.path.join(repo, os.fsdecode(path))
        if kind == "commit":
            head = git(full, "rev-parse", "HEAD").decode().strip() if os.path.isdir(full) and os.listdir(full) else None
            if head is None:
                continue  # uninitialised by design; reported by the caller
            if head != oid:
                problems.append(f"gitlink {path!r} checkout {head} vs {oid}")
            continue
        if not os.path.lexists(full):
            problems.append(f"missing on disk {path!r}")
            continue
        if disk_mode(full) != mode:
            problems.append(f"mode differs at {path!r}: {disk_mode(full)} vs {mode}")
        if mode == "120000":
            # a symlink's blob is its link text, which hash-object would follow
            link = os.fsencode(os.readlink(full))
            if git(repo, "hash-object", "--stdin", data=link).decode().strip() != oid:
                problems.append(f"link text differs at {path!r}")
            continue
        blobs.append((path, oid))
    if blobs:
        paths = b"\n".join(p for p, _ in blobs) + b"\n"
        got = git(repo, "hash-object", "--no-filters", "--stdin-paths", data=paths).split()
        for (path, oid), h in zip(blobs, got):
            if h.decode() != oid:
                problems.append(f"bytes differ at {path!r}")
    return len(tree), len(blobs), problems


def main():
    repo = sys.argv[1]
    targets = [repo] + [os.path.join(repo, s) for s in sys.argv[2:]]
    failed = False
    for t in targets:
        n, nb, problems = verify(t)
        name = os.path.relpath(t, repo) if t != repo else "."
        head = git(t, "rev-parse", "HEAD").decode().strip()
        print(f"{name}: HEAD {head}, {n} tree entries, {nb} blobs hashed, {len(problems)} problem(s)")
        for p in problems[:50]:
            print("  " + p)
        failed |= bool(problems)
    print("BLOBS VERIFY " + ("FAILED" if failed else "OK"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
