#!/usr/bin/env python3
"""Both sides of a merge kept, per file: the merge's diff from one parent carries exactly the other side's own changes
(the -U0 hunks' +/- lines, line numbers stripped, compared as sorted multisets). usage: merge_sides.py REPO BASE OURS THEIRS MERGED
MERGED may be 'WORKTREE' (the index and worktree before the commit)."""
import subprocess, sys
repo, base, ours, theirs, merged = sys.argv[1:6]
def git(*a):
    return subprocess.run(['git', '-C', repo, *a], check=True, capture_output=True, text=True).stdout
def files(a, b):
    args = ['diff', '--name-only', a] + ([] if b == 'WORKTREE' else [b])
    return set(git(*args).split())
def body(a, b, f):
    args = ['diff', '-U0', '--no-color', a] + ([] if b == 'WORKTREE' else [b]) + ['--', f]
    out = git(*args)
    return sorted(l for l in out.splitlines() if l[:1] in '+-' and not l.startswith(('+++', '---')))
bad = 0
for side, other, label in ((ours, theirs, 'this branch'), (theirs, ours, 'the merged-in side')):
    own = files(base, side)
    through = files(other, merged)
    for f in sorted(own):
        same = body(base, side, f) == body(other, merged, f)
        print(f"{label}: {f}: {'SAME' if same else 'DIFFERS'}")
        bad += not same
    extra = sorted(through - own)
    for f in extra:
        print(f"{label}: {f}: in the merge's diff from the other parent but not this side's own change")
        bad += 1
print(f"{bad} file(s) differ")
sys.exit(1 if bad else 0)
