#!/usr/bin/env python3
"""Check that a merge tree is the clean union of both sides' changes.

Usage: merge_union.py <repo> <base> <ours> <theirs> <merge>
Every path (blobs and gitlinks, with modes) in the merge must equal the side
that changed it relative to the merge base. A path changed by both sides is
reported as a conflict path for separate hunk review.
"""
import subprocess
import sys


def tree(repo: str, rev: str) -> dict:
    out = subprocess.check_output(['git', '-C', repo, 'ls-tree', '-r', '--full-tree', rev],
                                  stderr=subprocess.DEVNULL)
    entries = {}
    for line in out.decode().splitlines():
        meta, path = line.split('\t', 1)
        mode, _kind, sha = meta.split()
        entries[path] = (mode, sha)
    return entries


def main() -> int:
    repo, base, ours, theirs, merge = sys.argv[1:6]
    b, o, t, m = (tree(repo, r) for r in (base, ours, theirs, merge))
    bad, both = [], []
    for path in sorted(set(b) | set(o) | set(t) | set(m)):
        vo, vt, vb, vm = o.get(path), t.get(path), b.get(path), m.get(path)
        if vo != vb and vt != vb and vo != vt:
            both.append(path)
            continue
        want = vo if vo != vb else vt
        if vm != want:
            bad.append((path, want, vm))
    print(f'paths: {len(set(m))}; changed by ours: {sum(o.get(p) != b.get(p) for p in set(b)|set(o))}; '
          f'changed by theirs: {sum(t.get(p) != b.get(p) for p in set(b)|set(t))}')
    print('changed differently by both sides:', both)
    for item in bad:
        print('NOT A CLEAN UNION:', item)
    print('RESULT:', 'PASS' if not bad else 'FAIL')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
