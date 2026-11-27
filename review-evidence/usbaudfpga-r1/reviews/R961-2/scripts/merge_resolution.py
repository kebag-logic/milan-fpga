#!/usr/bin/env python3
"""For every path changed on both sides of the network merge, redo the
three-way merge and compare the clean result (if any) with the reviewed
head, so conflict resolutions and post-merge corrections are isolated."""
import subprocess, sys, tempfile, os
REPO, BASE, OURS, THEIRS, HEAD = sys.argv[1:6]
def git(*a, check=True):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True,
                          check=check).stdout
def names(a, b):
    return set(git("diff", "--name-only", "--no-renames", a, b).decode().split())
def show(rev, p):
    r = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{p}"],
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None
both = sorted(names(BASE, OURS) & names(BASE, THEIRS))
with tempfile.TemporaryDirectory() as td:
    for p in both:
        b, o, t, h = (show(x, p) for x in (BASE, OURS, THEIRS, HEAD))
        if o == t:
            print(f"SAME-BOTH-SIDES\t{'=HEAD' if h == o else '!=HEAD'}\t{p}")
            continue
        fs = []
        for nm, data in (("o", o), ("b", b), ("t", t)):
            fn = os.path.join(td, nm)
            open(fn, "wb").write(data or b"")
            fs.append(fn)
        r = subprocess.run(["git", "merge-file", "-p", *fs], capture_output=True)
        if r.returncode == 0:
            st = "CLEAN=HEAD" if r.stdout == h else "CLEAN!=HEAD"
        else:
            st = f"CONFLICT({r.returncode})"
        print(f"{st}\t\t{p}")
