#!/usr/bin/env python3
"""Check that a merge commit keeps both sides.

For every file both parents changed against the merge base, list each line a
side ADDED (relative to the base) that the merge does not carry, and each line
a side REMOVED that the merge still carries more often than the base allowed.
Multiset comparison, so reordering is not a loss; edits show as a missing line
plus its replacement, which the reviewer then reads by hand.

usage: both_sides.py REPO MERGE_COMMIT
"""
import collections
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True).stdout


def lines(repo, rev, path):
    try:
        return git(repo, "show", f"{rev}:{path}").decode("utf-8", "replace").splitlines()
    except subprocess.CalledProcessError:
        return []


def changed(repo, a, b):
    return set(git(repo, "diff", "--name-only", a, b).decode().split())


def main():
    repo, merge = sys.argv[1], sys.argv[2]
    p1, p2 = git(repo, "rev-parse", f"{merge}^1", f"{merge}^2").decode().split()
    base = git(repo, "merge-base", p1, p2).decode().strip()
    print(f"merge {merge}\n  ours   {p1}\n  theirs {p2}\n  base   {base}")
    both = sorted(changed(repo, base, p1) & changed(repo, base, p2))
    print(f"files changed by both sides: {len(both)}")
    total = 0
    for path in both:
        b = collections.Counter(lines(repo, base, path))
        m = collections.Counter(lines(repo, merge, path))
        for side, rev in (("ours", p1), ("theirs", p2)):
            s = collections.Counter(lines(repo, rev, path))
            added = s - b
            lost = {ln: n - m[ln] for ln, n in added.items() if m[ln] < n}
            for ln, n in sorted(lost.items()):
                total += 1
                print(f"  LOST-ADD {path} [{side}] x{n}: {ln[:200]}")
            removed = b - s
            kept = {ln: m[ln] - (b[ln] - n) for ln, n in removed.items()
                    if m[ln] > b[ln] - n}
            for ln, n in sorted(kept.items()):
                total += 1
                print(f"  KEPT-DEL {path} [{side}] x{n}: {ln[:200]}")
    print(f"discrepancies: {total}")


if __name__ == "__main__":
    main()
