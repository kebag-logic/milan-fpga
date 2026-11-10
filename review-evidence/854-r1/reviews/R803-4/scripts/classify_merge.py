#!/usr/bin/env python3
"""Classify every path of a merge commit's tree against its two sides.

Usage: python3 -I classify_merge.py <head> <pr-side> <dev-side> <merge-base>
Run from inside the repository. Prints one line per path that is not
identical on all four trees and not a plain dev-side change, then counts.

Classes:
  dev-only  head equals dev, and the PR side never changed the path
  pr-only   head equals the PR side, and dev never changed the path
  HAND      head equals neither side (a hand resolution or regeneration)
  HEAD=DEV-BUT-PR-CHANGED / HEAD=PR-BUT-DEV-CHANGED  a side's change lost
Mode and object id are both compared, so gitlinks and modes are covered.
"""
import subprocess
import sys


def tree(rev):
    out = subprocess.run(["git", "ls-tree", "-r", "--full-tree", rev],
                         capture_output=True, text=True, check=True).stdout
    m = {}
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        mode, _typ, oid = meta.split()
        m[path] = (mode, oid)
    return m


def main():
    head, pr, dev, base = (tree(r) for r in sys.argv[1:5])
    counts = {}
    for p in sorted(set(head) | set(pr) | set(dev) | set(base)):
        hv, dv, av, bv = head.get(p), dev.get(p), pr.get(p), base.get(p)
        dev_changed, pr_changed = dv != bv, av != bv
        if hv == dv and hv == av:
            cls = "same-all"
        elif hv == dv and not pr_changed:
            cls = "dev-only"
        elif hv == av and not dev_changed:
            cls = "pr-only"
        elif hv == dv:
            cls = "HEAD=DEV-BUT-PR-CHANGED"
        elif hv == av:
            cls = "HEAD=PR-BUT-DEV-CHANGED"
        else:
            cls = "HAND"
        counts[cls] = counts.get(cls, 0) + 1
        if cls not in ("same-all", "dev-only"):
            print(cls, p)
    print("counts", counts)


if __name__ == "__main__":
    main()
