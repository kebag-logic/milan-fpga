#!/usr/bin/env python3
"""Classify files changed between the previously reviewed head and the
reviewed head by origin: dev import, network import, or own change."""
import subprocess, sys
REPO, PREV, HEAD, BASE, DEV, NET = sys.argv[1:7]
def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True,
                          text=True, check=True).stdout
def blob(rev, path):
    r = subprocess.run(["git", "-C", REPO, "rev-parse", "-q", "--verify",
                        f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout.strip() or None
files = git("diff", "--name-only", "--no-renames", PREV, HEAD).split()
for f in files:
    h, p, b, d, n = (blob(x, f) for x in (HEAD, PREV, BASE, DEV, NET))
    if h == n and n != b:
        cls = "NET-IMPORT"
    elif h == d and d != b and p == b:
        cls = "DEV-IMPORT"
    elif h == d and h == n:
        cls = "SHARED-IMPORT"
    else:
        cls = "OWN"
        if n != b and n is not None:
            cls += "+NETTOUCHED"
        if d != b:
            cls += "+DEVTOUCHED"
    print(f"{cls}\t{f}")
