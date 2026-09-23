#!/usr/bin/env python3
"""R227-4 final integrity of the review clone after all probes.

Usage: verify_integrity.py <clone> <commit> <tree>

Checks, with GIT_NO_REPLACE_OBJECTS=1 on every Git call:
- HEAD and HEAD^{tree} are the reviewed identities;
- the index equals HEAD (path, mode, blob) at stage 0 only, with no
  assume-unchanged or skip-worktree flag;
- every tracked blob's working-tree bytes hash to its blob id
  (`git hash-object --no-filters`, symlinks by target) and its file type and
  executable bit match the recorded mode;
- `git status --porcelain --ignored --untracked-files=all` is empty;
- each initialised submodule is at its gitlink and clean, including ignored
  files; an uninitialised one has an empty directory.
"""

import os
import stat
import subprocess
import sys
from pathlib import Path

ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(repo: Path, *args: str, data: bytes | None = None) -> str:
    """Run one Git command and return stdout, failing on a non-zero exit."""
    done = subprocess.run(["git", "-C", str(repo), *args], input=data,
                          capture_output=True, env=ENV, check=True)
    return done.stdout.decode()


def blob_of(repo: Path, path: Path, mode: str) -> str:
    """The blob id of the working-tree bytes at `path`."""
    if mode == "120000":
        return git(repo, "hash-object", "--stdin",
                   data=os.readlink(path).encode()).strip()
    return git(repo, "hash-object", "--no-filters", "--", str(path)).strip()


def main() -> int:
    """Print one line per check and exit non-zero on any failure."""
    clone, commit, tree = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    failures = []
    head = git(clone, "rev-parse", "HEAD").strip()
    head_tree = git(clone, "rev-parse", "HEAD^{tree}").strip()
    print(f"HEAD {head} tree {head_tree}")
    if head != commit or head_tree != tree:
        failures.append("HEAD or tree differs from the reviewed identity")
    recorded = {}
    for line in git(clone, "ls-tree", "-r", "--full-tree", "HEAD").splitlines():
        meta, path = line.split("\t", 1)
        mode, _kind, oid = meta.split()
        recorded[path] = (mode, oid)
    index = {}
    for line in git(clone, "ls-files", "-s").splitlines():
        meta, path = line.split("\t", 1)
        mode, oid, stage = meta.split()
        if stage != "0":
            failures.append(f"unmerged index record {path} stage {stage}")
        index[path] = (mode, oid)
    if index != recorded:
        failures.append("index differs from HEAD")
    # `H` is an ordinary cached entry; `S` is skip-worktree and a lowercase
    # tag is assume-unchanged, the two flags that hide a working-tree edit.
    flagged = [line for line in git(clone, "ls-files", "-v").splitlines()
               if line[:1] != "H"]
    if flagged:
        failures.append(f"hidden index flags: {flagged[:5]}")
    blobs = gitlinks = 0
    for path, (mode, oid) in sorted(recorded.items()):
        full = clone / path
        if mode == "160000":
            gitlinks += 1
            if (full / ".git").exists():
                sub = git(full, "rev-parse", "HEAD").strip()
                dirty = git(full, "status", "--porcelain", "--ignored",
                            "--untracked-files=all")
                print(f"submodule {path} {sub} clean={not dirty}")
                if sub != oid or dirty:
                    failures.append(f"submodule {path} off pin or dirty")
            else:
                empty = full.is_dir() and not any(full.iterdir())
                print(f"submodule {path} uninitialised, empty={empty}")
                if not empty:
                    failures.append(f"submodule {path} has unregistered content")
            continue
        blobs += 1
        info = full.lstat()
        if mode == "120000":
            ok_type = stat.S_ISLNK(info.st_mode)
        else:
            ok_type = stat.S_ISREG(info.st_mode) and \
                bool(info.st_mode & 0o100) == (mode == "100755")
        if not ok_type or blob_of(clone, full, mode) != oid:
            failures.append(f"blob or mode differs: {path}")
    status = git(clone, "status", "--porcelain", "--ignored",
                 "--untracked-files=all")
    print(f"blobs checked {blobs}, gitlinks {gitlinks}, "
          f"status lines {len(status.splitlines())}")
    if status:
        failures.append("working tree not clean, including ignored files")
    for failure in failures:
        print(f"FAIL {failure}")
    print("INTEGRITY " + ("PASS" if not failures else "FAIL"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
