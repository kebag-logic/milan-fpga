#!/usr/bin/env python3
"""R548-2: verify a clone's tracked bytes, modes, index and submodule gitlinks.

Usage: python3 -I r548_2_integrity.py <clone> <expected-head> <expected-tree>

Checks HEAD and its tree; that the index equals HEAD's tree; for every index
entry the working file's blob hash and mode (regular, executable, symlink);
for every gitlink an initialised submodule's HEAD equals the pinned commit
and its own tracked bytes are clean (an uninitialised one is reported); no
assume-unchanged or skip-worktree flag; and no untracked or ignored file in
the parent. Exit 0 only when all hold.
"""
import os
import stat
import subprocess
import sys
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          check=True).stdout


def main() -> int:
    repo, head, tree = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]
    bad = []
    if git(repo, "rev-parse", "HEAD").strip() != head:
        bad.append("HEAD differs")
    if git(repo, "rev-parse", "HEAD^{tree}").strip() != tree:
        bad.append("HEAD tree differs")
    if git(repo, "write-tree").strip() != tree:
        bad.append("index tree differs from HEAD tree")
    flags = [ln for ln in git(repo, "ls-files", "-v").splitlines() if ln[:1].islower() or ln[:1] == "S"]
    if flags:
        bad.append(f"{len(flags)} assume-unchanged/skip-worktree entries")
    entries = git(repo, "ls-files", "-s", "-z").split("\0")
    files = links = 0
    paths = []
    for entry in filter(None, entries):
        meta, path = entry.split("\t", 1)
        mode, sha, _ = meta.split()
        full = repo / path
        if mode == "160000":
            links += 1
            if not (full / ".git").exists():
                print(f"gitlink {path} {sha}: not initialised")
                continue
            sub = git(full, "rev-parse", "HEAD").strip()
            dirty = git(full, "status", "--porcelain").strip()
            print(f"gitlink {path} {sha}: HEAD {sub} {'match' if sub == sha else 'MISMATCH'}, "
                  f"{'clean' if not dirty else 'DIRTY'}")
            if sub != sha or dirty:
                bad.append(f"gitlink {path}")
            continue
        files += 1
        paths.append(path)
        st = os.lstat(full)
        kind = ("120000" if stat.S_ISLNK(st.st_mode) else
                "100755" if st.st_mode & 0o111 else "100644")
        if kind != mode:
            bad.append(f"mode {path}: {kind} != {mode}")
    hashes = subprocess.run(["git", "-C", str(repo), "hash-object", "--no-filters", "--stdin-paths"],
                            input="\n".join(paths) + "\n", capture_output=True, text=True,
                            check=True).stdout.split()
    index = {e.split("\t", 1)[1]: e.split()[1] for e in filter(None, entries)}
    for path, sha in zip(paths, hashes):
        if index[path] != sha:
            bad.append(f"bytes {path}")
    extra = git(repo, "status", "--porcelain", "--ignored", "--untracked-files=all",
                "--ignore-submodules=none").strip()
    if extra:
        bad.append("untracked/ignored/modified: " + extra.replace("\n", "; ")[:400])
    print(f"tracked files {files}, gitlinks {links}, problems {len(bad)}")
    for line in bad[:50]:
        print("[FAIL]", line)
    print("INTEGRITY", "PASS" if not bad else "FAIL")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
