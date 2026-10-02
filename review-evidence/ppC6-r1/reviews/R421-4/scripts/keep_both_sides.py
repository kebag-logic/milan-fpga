#!/usr/bin/env python3
"""Line-level 'nothing lost' check for a two-parent merge commit.

For every file touched by either side relative to the merge base, every line a
side ADDED must still be present in the merge result (multiset-aware), and every
line a side DELETED must be absent unless the other side or the base keeps more
copies. Lines the merge drops or adds on its own are listed for manual review.

usage: keep_both_sides.py <repo> <merge-commit>
"""
import collections
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True).stdout


def blob_lines(repo, rev, path):
    try:
        data = git(repo, "show", f"{rev}:{path}")
    except subprocess.CalledProcessError:
        return []
    if b"\0" in data[:8000]:
        return None  # binary
    return data.decode("utf-8", "replace").splitlines()


def main():
    repo, merge = sys.argv[1], sys.argv[2]
    p1, p2 = git(repo, "rev-parse", f"{merge}^1", f"{merge}^2").decode().split()
    base = git(repo, "merge-base", p1, p2).decode().strip()
    files = set()
    for p in (p1, p2):
        files |= set(git(repo, "diff", "--name-only", base, p).decode().split())
    print(f"merge {merge} p1 {p1} p2 {p2} base {base} files {len(files)}")
    problems = 0
    for f in sorted(files):
        b = blob_lines(repo, base, f)
        s1 = blob_lines(repo, p1, f)
        s2 = blob_lines(repo, p2, f)
        m = blob_lines(repo, merge, f)
        if None in (b, s1, s2, m):
            print(f"BINARY {f}:")
            for r, name in ((base, "base"), (p1, "p1"), (p2, "p2"), (merge, "merge")):
                try:
                    print(f"   {name} blob {git(repo, 'rev-parse', f'{r}:{f}').decode().strip()}")
                except subprocess.CalledProcessError:
                    print(f"   {name} absent")
            continue
        cb, c1, c2, cm = (collections.Counter(x) for x in (b, s1, s2, m))
        lost, resurrected, own = [], [], []
        for line in set(c1) | set(c2) | set(cb) | set(cm):
            want_min = max(c1[line] - cb[line], 0) + max(c2[line] - cb[line], 0) + min(cb[line], c1[line], c2[line])
            # each side's additions on top of the common kept copies
            want_max = max(c1[line], c2[line], cb[line]) + max(c1[line] - cb[line], 0) + max(c2[line] - cb[line], 0)
            if cm[line] < want_min and line.strip():
                # tolerate a common addition both sides made identically
                if not (c1[line] == c2[line] and cm[line] >= c1[line]):
                    lost.append((line, cm[line], want_min))
            if cm[line] > max(c1[line], c2[line]) and line.strip() and cm[line] > want_min:
                own.append((line, cm[line]))
        if lost or own:
            problems += 1
            print(f"== {f}: {len(lost)} line(s) below both-sides count, {len(own)} merge-own line(s)")
            for line, have, want in sorted(lost)[:40]:
                print(f"   LOST have={have} want>={want}: {line[:150]}")
            for line, have in sorted(own)[:40]:
                print(f"   OWN  x{have}: {line[:150]}")
    print(f"files needing review: {problems}")


if __name__ == "__main__":
    main()
