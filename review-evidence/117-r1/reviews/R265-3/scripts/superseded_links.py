#!/usr/bin/env python3
"""Find any link to a superseded evidence-archive object in the PR's commits.

Usage: superseded_links.py <pr-git-dir> <evidence-git-dir> <base> <head> <current-tip> <superseded-tip>...

Collects every hex token of 7..40 characters from the PR commit messages and
every blob the PR adds, then reports which resolve (as a prefix) to a commit or
tree on a superseded chain but not on the current evidence chain.
"""
import re
import subprocess
import sys


def git(gd, *a):
    return subprocess.run(["git", f"--git-dir={gd}", *a], capture_output=True, check=True).stdout.decode(errors="replace")


pr, ev, base, head, cur = sys.argv[1:6]
sup_tips = sys.argv[6:]
objs_cur = set()
for c in git(ev, "rev-list", f"{base}..{cur}").split():
    objs_cur.add(c)
    objs_cur.add(git(ev, "rev-parse", c + "^{tree}").strip())
objs_sup = set()
for tip in sup_tips:
    for c in git(ev, "rev-list", f"{base}..{tip}").split():
        objs_sup.add(c)
        objs_sup.add(git(ev, "rev-parse", c + "^{tree}").strip())
        # subtrees under review-evidence as well
        for line in git(ev, "ls-tree", "-r", "-t", c, "review-evidence").splitlines():
            meta, _ = line.split("\t", 1)
            objs_sup.add(meta.split()[2])
only_sup = objs_sup - objs_cur
print("superseded-only commits/trees:", len(only_sup), "; current-chain commits/trees:", len(objs_cur))
texts = []
for c in git(pr, "rev-list", f"{base}..{head}").split():
    texts.append(("message " + c[:12], git(pr, "cat-file", "commit", c)))
for line in git(pr, "rev-list", "--objects", f"{base}..{head}").splitlines():
    parts = line.split(" ", 1)
    if len(parts) == 2 and git(pr, "cat-file", "-t", parts[0]).strip() == "blob":
        texts.append((f"blob {parts[0][:12]} {parts[1]}", git(pr, "cat-file", "blob", parts[0])))
tokens = {}
for where, t in texts:
    for m in re.finditer(r"(?<![0-9a-fA-F])[0-9a-f]{7,40}(?![0-9a-fA-F])", t):
        tokens.setdefault(m.group(0), set()).add(where)
print("distinct hex tokens (7..40) in PR messages and blobs:", len(tokens))
hits = {tok: w for tok, w in tokens.items() if any(o.startswith(tok) for o in only_sup)}
print("tokens resolving to superseded-only archive objects:", len(hits))
for tok, w in sorted(hits.items()):
    print("  ", tok, sorted(w))
curhits = {tok: w for tok, w in tokens.items() if any(o.startswith(tok) for o in objs_cur)}
print("tokens resolving to current evidence-chain commits/trees:", sorted(curhits))
