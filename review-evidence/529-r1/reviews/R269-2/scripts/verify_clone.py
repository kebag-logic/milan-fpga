#!/usr/bin/env python3
"""Prove a review clone still holds the exact head's bytes.

usage: verify_clone.py CLONE EXPECT_HEAD EXPECT_TREE
Checks, printing one line each and exiting non-zero on any failure:
  * HEAD and its tree are the expected ones;
  * the index is exactly HEAD's tree (write-tree) and has one stage-0 record per path;
  * no index entry carries assume-unchanged or skip-worktree;
  * every tracked regular file / symlink hashes, from the bytes on disk, to its
    index blob id, with the recorded mode (100644 / 100755 / 120000);
  * no untracked or ignored residue (git status --ignored);
  * each required gitlink is mode 160000 at its pin, its checkout HEAD is that pin,
    and its worktree is clean.
The hashing reads files directly, so an index told to stay quiet cannot hide an edit.
"""
import hashlib
import os
import stat
import subprocess
import sys

REQUIRED = ("third_party/verilog-axis", "protocol-processor", "gptp-processor")


def git(repo, *args, raw=False):
    out = subprocess.run(["git", "-C", repo, *args], capture_output=True, check=True,
                         env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}).stdout
    return out if raw else out.decode()


def main():
    clone, want_head, want_tree = sys.argv[1:4]
    bad = 0

    def report(ok, msg):
        nonlocal bad
        bad += not ok
        print(("OK   " if ok else "FAIL ") + msg)

    head = git(clone, "rev-parse", "HEAD").strip()
    tree = git(clone, "rev-parse", "HEAD^{tree}").strip()
    report(head == want_head, f"HEAD {head}")
    report(tree == want_tree, f"HEAD tree {tree}")
    report(git(clone, "write-tree").strip() == tree, "index write-tree equals HEAD tree")
    recs = git(clone, "ls-files", "-s", "-z", raw=True).split(b"\0")
    entries, stages = [], set()
    for r in recs:
        if not r:
            continue
        meta, path = r.split(b"\t", 1)
        mode, oid, stage = meta.decode().split()
        entries.append((mode, oid, path.decode()))
        stages.add(stage)
    report(stages == {"0"}, f"index stages {sorted(stages)} over {len(entries)} records")
    flags = [ln for ln in git(clone, "ls-files", "-v").splitlines()
             if ln[:1].islower() or ln[:1] == "S"]
    report(not flags, f"assume-unchanged / skip-worktree entries: {len(flags)}")
    mism = 0
    for mode, oid, path in entries:
        full = os.path.join(clone, path)
        if mode == "160000":
            continue
        try:
            st = os.lstat(full)
        except FileNotFoundError:
            mism += 1
            print(f"     missing {path}")
            continue
        if mode == "120000":
            ok_mode = stat.S_ISLNK(st.st_mode)
            data = os.readlink(full).encode() if ok_mode else b""
        else:
            ok_mode = stat.S_ISREG(st.st_mode) and (
                bool(st.st_mode & stat.S_IXUSR) == (mode == "100755"))
            data = open(full, "rb").read() if stat.S_ISREG(st.st_mode) else b""
        h = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        if not ok_mode or h != oid:
            mism += 1
            print(f"     mismatch {mode} {path}")
    report(mism == 0, f"tracked blob byte/mode mismatches: {mism}")
    residue = [ln for ln in git(clone, "status", "--porcelain", "--ignored",
                                "--ignore-submodules=none").splitlines()]
    report(not residue, f"untracked/ignored/modified residue lines: {len(residue)}")
    for ln in residue[:20]:
        print(f"     {ln}")
    pins = {p: o for m, o, p in entries if m == "160000"}
    for sub in REQUIRED:
        pin = pins.get(sub)
        report(pin is not None, f"gitlink {sub} mode 160000 pin {pin}")
        if pin:
            shead = git(os.path.join(clone, sub), "rev-parse", "HEAD").strip()
            dirty = git(os.path.join(clone, sub), "status", "--porcelain", "--ignored").strip()
            report(shead == pin, f"  {sub} checkout HEAD {shead}")
            report(not dirty, f"  {sub} worktree clean")
    print("RESULT:", "CLEAN" if bad == 0 else f"{bad} FAILURE(S)")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
