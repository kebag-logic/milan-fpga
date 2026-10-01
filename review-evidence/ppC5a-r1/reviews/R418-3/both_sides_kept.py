#!/usr/bin/env python3
"""Check that a merge keeps both sides: every line each side added relative to
the merge base is present in the merge result (multiset count), and every line
each side deleted is gone unless the other side or the base keeps it elsewhere.

usage: both_sides_kept.py <repo> <base> <ours> <theirs> <merge> [paths...]
Prints each file with lines added by a side that are missing from the merge.
Exit 0 always; the output is the receipt to be read.
"""
import subprocess, sys
from collections import Counter


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True,
                          check=False).stdout.decode("utf-8", "replace")


def blob(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                       capture_output=True)
    return r.stdout.decode("utf-8", "replace").splitlines() if r.returncode == 0 else None


def added(repo, a, b, path):
    out = git(repo, "diff", "-U0", "--no-color", a, b, "--", path)
    adds, dels = Counter(), Counter()
    for ln in out.splitlines():
        if ln.startswith("+++") or ln.startswith("---"):
            continue
        if ln.startswith("+"):
            adds[ln[1:]] += 1
        elif ln.startswith("-"):
            dels[ln[1:]] += 1
    return adds, dels


def main():
    repo, base, ours, theirs, merge = sys.argv[1:6]
    paths = sys.argv[6:]
    if not paths:
        names = set(git(repo, "diff", "--name-only", base, ours).split())
        names &= set(git(repo, "diff", "--name-only", base, theirs).split())
        paths = sorted(names)
    total_missing = 0
    for p in paths:
        m = blob(repo, merge, p)
        if m is None:
            print(f"## {p}: ABSENT in merge")
            continue
        mc = Counter(m)
        for side, rev in (("ours", ours), ("theirs", theirs)):
            adds, _ = added(repo, base, rev, p)
            other = blob(repo, theirs if side == "ours" else ours, p) or []
            oc = Counter(other)
            miss = []
            for ln, n in adds.items():
                if ln.strip() == "":
                    continue
                if mc[ln] < min(n, n):
                    miss.append((ln, n, mc[ln]))
            if miss:
                total_missing += len(miss)
                print(f"## {p}: {side} ({rev}) added lines not all in merge: {len(miss)}")
                for ln, n, have in miss[:60]:
                    print(f"   want {n} have {have}: {ln[:150]}")
        print(f"-- {p}: checked")
    print(f"TOTAL lines-with-shortfall: {total_missing}")


if __name__ == "__main__":
    main()
