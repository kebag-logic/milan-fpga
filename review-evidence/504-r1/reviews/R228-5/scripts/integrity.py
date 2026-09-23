#!/usr/bin/env python3
"""Prove the candidate checkout is the exact committed head, byte for byte.

Usage: CLONE=<checkout> python3 integrity.py <label>  (writes JSON to stdout)

Checks, with GIT_NO_REPLACE_OBJECTS=1 on every Git call:
  * HEAD and HEAD^{tree} equal the expected candidate identities;
  * every regular/executable/symlink entry of HEAD's tree hashes, from the
    bytes on disk, to the blob HEAD records, with the recorded mode;
  * the index equals HEAD (no staged change, no unmerged stage) and carries
    no assume-unchanged or skip-worktree flag;
  * `git status --porcelain --ignored` is empty;
  * the three required submodules are checked out at their gitlinks.
"""
import hashlib
import json
import os
import pathlib
import subprocess
import sys

CLONE = pathlib.Path(os.environ.get("CLONE", ".")).resolve()
EXPECT_HEAD = "50c0d00ac3e7b7aa319ba4eab995d7e12b89149e"
EXPECT_TREE = "4819081971902d71acba2948e659e9658b3fb977"
REQUIRED_SUBMODULES = ("third_party/verilog-axis", "protocol-processor", "gptp-processor")
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(*args, cwd=CLONE, text=True):
    return subprocess.run(["git", *args], cwd=cwd, env=ENV, capture_output=True,
                          text=text, check=True).stdout


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "check"
    head, tree = git("rev-parse", "HEAD", "HEAD^{tree}").split()
    problems = []
    if head != EXPECT_HEAD or tree != EXPECT_TREE:
        problems.append(f"identity {head} {tree}")
    entries = git("ls-tree", "-r", "-z", "--full-tree", "HEAD", text=False).split(b"\0")
    blobs = gitlinks = 0
    for raw in filter(None, entries):
        meta, path = raw.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        p = CLONE / os.fsdecode(path)
        if kind == "commit":
            gitlinks += 1
            continue
        blobs += 1
        if mode == "120000":
            if not p.is_symlink() or blob_id(os.fsencode(os.readlink(p))) != oid:
                problems.append(f"symlink {path!r}")
            continue
        if p.is_symlink() or not p.is_file():
            problems.append(f"not a regular file {path!r}")
            continue
        actual_mode = "100755" if os.stat(p).st_mode & 0o111 else "100644"
        if actual_mode != mode:
            problems.append(f"mode {path!r} {actual_mode} != {mode}")
        if blob_id(p.read_bytes()) != oid:
            problems.append(f"bytes {path!r}")
    if git("diff", "--cached", "--name-only", "HEAD").strip():
        problems.append("index differs from HEAD")
    flags = [l for l in git("ls-files", "-v").splitlines() if l[:1] not in ("H",)]
    if flags:
        problems.append(f"index flags {flags[:5]}")
    if git("ls-files", "-u").strip():
        problems.append("unmerged index stages")
    status = git("status", "--porcelain", "--ignored")
    if status.strip():
        problems.append(f"status not clean: {status.splitlines()[:10]}")
    subs = {}
    for sub in REQUIRED_SUBMODULES:
        link = git("ls-tree", "HEAD", sub).split()[2]
        actual = git("rev-parse", "HEAD", cwd=CLONE / sub).strip()
        dirty = git("status", "--porcelain", cwd=CLONE / sub).strip()
        subs[sub] = {"gitlink": link, "checkout": actual, "clean": not dirty}
        if link != actual or dirty:
            problems.append(f"submodule {sub} {actual} vs {link} dirty={bool(dirty)}")
    report = {"label": label, "head": head, "tree": tree, "blobs_checked": blobs,
              "gitlinks_in_tree": gitlinks, "submodules": subs,
              "problems": problems, "verdict": "PASS" if not problems else "FAIL"}
    print(json.dumps(report, indent=1))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
