#!/usr/bin/env python3
"""Count mentions of superseded archive commit ids (read from a private
file, one full SHA per line) in (a) every blob and message of a git range and
(b) the PR commits. Prints labels L1..Ln, never the ids.
usage: superseded_mentions.py <private-sha-file> <git-dir> <A..B> [<git-dir> <A..B> ...]"""
import re
import subprocess
import sys

shas = [l.strip() for l in open(sys.argv[1]) if l.strip()]
pats = [(f"L{i + 1}", re.compile(s[:7].encode())) for i, s in enumerate(shas)]


def git(gd, *a):
    return subprocess.run(["git", "--git-dir", gd, *a], capture_output=True, check=True).stdout


args = sys.argv[2:]
for gd, rng in zip(args[::2], args[1::2]):
    a, b = rng.split("..")
    total = {}
    files = {}
    for c in git(gd, "rev-list", f"{a}..{b}").decode().split():
        objs = [("message", git(gd, "log", "-1", "--format=%B", c))]
        out = git(gd, "diff-tree", "-r", "-z", "--no-renames", c).split(b"\0")
        for i in range(len(out) - 1):
            if out[i].startswith(b":"):
                sha = out[i][1:].split()[3].decode()
                if set(sha) != {"0"}:
                    objs.append((out[i + 1].decode("utf-8", "surrogateescape"), git(gd, "cat-file", "blob", sha)))
        for name, data in objs:
            for lab, p in pats:
                n = len(p.findall(data))
                if n:
                    total[lab] = total.get(lab, 0) + n
                    files.setdefault(f"{c[:12]}:{name}", set()).add(lab)
    print(f"range {rng}: mentions by label {dict(sorted(total.items()))}; objects {len(files)}")
    for k in sorted(files):
        print(f"   {k}: {sorted(files[k])}")
