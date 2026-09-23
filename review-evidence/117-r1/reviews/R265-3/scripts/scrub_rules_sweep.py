#!/usr/bin/env python3
"""Apply the repository's own SCRUB_RULES (identity + local-info) to git blobs and commit messages.

Usage: scrub_rules_sweep.py <repo-with-docs_check> <git-dir> <label> <rev-range>...
Prints rule class, object path and count; never the matched text.
"""
import collections
import importlib.util
import subprocess
import sys

repo, gd, label = sys.argv[1:4]
ranges = sys.argv[4:]
spec = importlib.util.spec_from_file_location("docs_check", f"{repo}/scripts/docs_check.py")
dc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dc)


def git(*a):
    return subprocess.run(["git", f"--git-dir={gd}", *a], capture_output=True, check=True).stdout


seen = set()
hits = collections.Counter()
nobj = 0
for r in ranges:
    for c in git("rev-list", r).decode().split():
        msg = git("cat-file", "commit", c).decode("latin-1")
        nobj += 1
        for rx, cls, _ in dc.SCRUB_RULES:
            n = len(rx.findall(msg))
            if n:
                hits[(cls, "commit message " + c[:12])] += n
    for line in git("rev-list", "--objects", r).decode().splitlines():
        parts = line.split(" ", 1)
        if len(parts) != 2 or parts[0] in seen:
            continue
        seen.add(parts[0])
        if git("cat-file", "-t", parts[0]).strip() != b"blob":
            continue
        nobj += 1
        text = git("cat-file", "blob", parts[0]).decode("latin-1")
        for rx, cls, _ in dc.SCRUB_RULES:
            n = len(rx.findall(text))
            if n:
                hits[(cls, parts[1])] += n
print(f"[{label}] objects scanned {nobj}; rules {len(dc.SCRUB_RULES)}; hits {sum(hits.values())}")
for (cls, where), n in sorted(hits.items()):
    print(f"   {cls:28s} {where} x{n}")
