#!/usr/bin/env python3
"""Print lines this lane itself added: lines added by its own commits that
are present in neither merge input (audio side before the network merge,
network head), so restored inherited content is excluded."""
import re, subprocess, sys
REPO, OURS, THEIRS, *COMMITS = sys.argv[1:]
PAT = re.compile(sys.stdin.read().strip())
def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True).stdout
cache = {}
def lines_of(rev, path):
    k = (rev, path)
    if k not in cache:
        cache[k] = set(git("show", f"{rev}:{path}").splitlines())
    return cache[k]
for c in COMMITS:
    path = None
    post_merge = c.startswith("POST:")
    c = c.removeprefix("POST:")
    for line in git("show", "--format=", "-U0", "--first-parent", c).splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else None
            continue
        if not line.startswith("+") or path is None:
            continue
        text = line[1:]
        if post_merge and (text in lines_of(OURS, path) or text in lines_of(THEIRS, path)):
            continue
        if PAT.search(text):
            print(f"{c[:10]} {path}: {text.strip()[:220]}")
