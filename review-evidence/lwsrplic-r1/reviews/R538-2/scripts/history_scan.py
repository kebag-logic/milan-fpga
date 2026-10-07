#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Scan every object reachable from every ref of a git repository for terms.

Usage: TERMS_FILE=<file with one case-insensitive regex per line> \
       history_scan.py <git-dir-or-worktree> [ref-glob ...]

The term list is supplied privately so that this script and its output stay
free of the scanned names.  Matches are reported with the term replaced by
[TERM<n>] and the matched text never printed.  Scope: commit headers and
messages (author, committer, subject, body, trailers), annotated tags, every
tree entry name (paths), and every blob, for all objects reachable from the
selected refs (default: --all).
"""
import os
import re
import subprocess
import sys


def git(repo, *args, data=None):
    return subprocess.run(["git", "-C", repo, *args], input=data,
                          capture_output=True, check=True).stdout


def redact(text, pats):
    for n, p in enumerate(pats):
        text = p.sub(f"[TERM{n}]".encode(), text.encode()).decode()
    return text


def main():
    repo = sys.argv[1]
    refs = sys.argv[2:] or ["--all"]
    terms = [line.strip() for line in open(os.environ["TERMS_FILE"])
             if line.strip() and not line.startswith("#")]
    pats = [re.compile(t.encode(), re.I) for t in terms]
    revs = git(repo, "rev-list", "--objects", *refs).decode().splitlines()
    objs = {}
    for line in revs:
        oid, _, path = line.partition(" ")
        objs.setdefault(oid, set()).add(path)
    batch = git(repo, "cat-file", "--batch", data="\n".join(objs).encode() + b"\n")
    pos = 0
    counts = {"commit": 0, "tree": 0, "blob": 0, "tag": 0}
    hits = 0
    while pos < len(batch):
        nl = batch.index(b"\n", pos)
        oid, typ, size = batch[pos:nl].decode().split()
        size = int(size)
        body = batch[nl + 1:nl + 1 + size]
        pos = nl + 1 + size + 1
        counts[typ] += 1
        if typ == "tree":
            # Tree entries: "<mode> <name>\0<20-byte oid>"; scan names only.
            names = []
            i = 0
            while i < len(body):
                z = body.index(b"\0", i)
                names.append(body[i:z].split(b" ", 1)[1])
                i = z + 21
            text = b"\n".join(names)
        else:
            text = body
        for n, p in enumerate(pats):
            for lineno, ln in enumerate(text.split(b"\n"), 1):
                if p.search(ln):
                    hits += 1
                    where = redact(sorted(objs[oid])[0] or "-", pats)
                    print(f"HIT {typ} {oid} path={where} line={lineno} [TERM{n}]")
    for path in sorted({p for s in objs.values() for p in s if p}):
        for n, p in enumerate(pats):
            if p.search(path.encode()):
                hits += 1
                print(f"HIT path [TERM{n}] (reachable path name)")
    print(f"refs={' '.join(refs)} objects={len(objs)} commits={counts['commit']} "
          f"trees={counts['tree']} blobs={counts['blob']} tags={counts['tag']} "
          f"terms={len(pats)} hits={hits}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
