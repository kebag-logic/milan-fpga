#!/usr/bin/env python3
"""R239: prove the review clone still holds the exact reviewed source.

Checks, with GIT_NO_REPLACE_OBJECTS=1 on every git call:
  1. HEAD commit and tree are the reviewed identities.
  2. The index equals HEAD's tree record for record (mode, oid, stage 0).
  3. No index entry carries assume-unchanged or skip-worktree ('h'/'S' in ls-files -v).
  4. Every worktree file/symlink hashes to its blob, with the recorded kind and
     executable bit (bytes read from disk; the index is not trusted for this).
  5. No untracked or ignored path exists in the parent worktree.
  6. The three required submodules are checked out at their gitlinks, and every
     file of each pinned tree hashes to its blob on disk, with kind/mode.
Exit 0 only if every check holds.
"""
import os
import stat
import subprocess
import sys

CLONE = "$VALIDATION_STORAGE/reviews/r239-372-r1"
HEAD = "60c5225fe5f93209bf313c51b7a722f25f9aaa7d"
TREE = "64182178131d03f157fe1a4ec767edee618bc6ff"
REQUIRED = ("third_party/verilog-axis", "protocol-processor", "gptp-processor")
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(repo, *args, data=None):
    return subprocess.run(["git", "-C", repo, *args], input=data, capture_output=True,
                          check=True, env=ENV).stdout


def tree_records(repo, rev):
    out = git(repo, "ls-tree", "-r", "-z", rev)
    recs = {}
    for rec in out.split(b"\0"):
        if rec:
            meta, path = rec.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            recs[path.decode()] = (mode, kind, oid)
    return recs


def prove_bytes(repo, recs, label):
    """(ok, bad) over regular files and symlinks of `recs` in worktree `repo`."""
    ok = bad = 0
    for path, (mode, kind, oid) in sorted(recs.items()):
        if kind != "blob":
            continue
        full = os.path.join(repo, path)
        try:
            st = os.lstat(full)
        except FileNotFoundError:
            print(f"{label}: MISSING {path}")
            bad += 1
            continue
        if mode == "120000":
            if not stat.S_ISLNK(st.st_mode):
                print(f"{label}: KIND {path} is not a symlink")
                bad += 1
                continue
            data = os.readlink(full).encode()
        else:
            if not stat.S_ISREG(st.st_mode):
                print(f"{label}: KIND {path} is not a regular file")
                bad += 1
                continue
            execbit = bool(st.st_mode & stat.S_IXUSR)
            if execbit != (mode == "100755"):
                print(f"{label}: MODE {path} exec={execbit} recorded={mode}")
                bad += 1
                continue
            with open(full, "rb") as fh:
                data = fh.read()
        got = git(repo, "hash-object", "--stdin", data=data).strip().decode()
        if got != oid:
            print(f"{label}: BYTES {path}")
            bad += 1
        else:
            ok += 1
    return ok, bad


def main():
    failures = 0
    head = git(CLONE, "rev-parse", "HEAD").strip().decode()
    tree = git(CLONE, "rev-parse", "HEAD^{tree}").strip().decode()
    print(f"HEAD {head} tree {tree}")
    if head != HEAD or tree != TREE:
        print("IDENTITY MISMATCH")
        failures += 1
    recs = tree_records(CLONE, HEAD)
    index = {}
    for rec in git(CLONE, "ls-files", "-s", "-z").split(b"\0"):
        if rec:
            meta, path = rec.split(b"\t", 1)
            mode, oid, stage = meta.decode().split()
            index[path.decode()] = (mode, oid, stage)
    idx_bad = 0
    for path, (mode, kind, oid) in recs.items():
        if index.get(path) != (mode, oid, "0"):
            print(f"INDEX {path}: {index.get(path)} vs {(mode, oid, '0')}")
            idx_bad += 1
    extra = set(index) - set(recs)
    for path in sorted(extra):
        print(f"INDEX extra {path}")
    idx_bad += len(extra)
    print(f"index records: {len(index)} tree records: {len(recs)} mismatches: {idx_bad}")
    failures += idx_bad
    flags = [line for line in git(CLONE, "ls-files", "-v").decode().splitlines() if line[:1] in ("h", "S", "s")]
    print(f"assume-unchanged/skip-worktree entries: {len(flags)}")
    failures += len(flags)
    ok, bad = prove_bytes(CLONE, recs, "parent")
    print(f"parent worktree bytes: match={ok} mismatch={bad} "
          f"(gitlinks={sum(1 for v in recs.values() if v[1] == 'commit')})")
    failures += bad
    status = git(CLONE, "status", "--porcelain=v2", "--ignored", "--untracked-files=all").decode().strip()
    print(f"status --ignored --untracked-files=all lines: {len(status.splitlines()) if status else 0}")
    if status:
        print(status[:2000])
        failures += 1
    for sub in REQUIRED:
        pin = recs[sub][2]
        subrepo = os.path.join(CLONE, sub)
        at = git(subrepo, "rev-parse", "HEAD").strip().decode()
        srecs = tree_records(subrepo, pin)
        flags = [line for line in git(subrepo, "ls-files", "-v").decode().splitlines()
                 if line[:1] in ("h", "S", "s")]
        sok, sbad = prove_bytes(subrepo, srecs, sub)
        sstatus = git(subrepo, "status", "--porcelain", "--untracked-files=all").decode().strip()
        good = at == pin and sbad == 0 and not flags and not sstatus
        print(f"submodule {sub}: gitlink {pin} checkout {at} bytes match={sok} mismatch={sbad} "
              f"hidden-flags={len(flags)} status-lines={len(sstatus.splitlines()) if sstatus else 0} "
              f"-> {'OK' if good else 'FAIL'}")
        failures += 0 if good else 1
    print("INTEGRITY", "PASS" if failures == 0 else f"FAIL ({failures})")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
