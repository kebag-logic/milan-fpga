#!/usr/bin/env python3
"""Stage chosen zero-context hunks of the worktree's diff into the index, leaving the worktree as it is. Lane
helper, not part of the tree.

usage: stage_hunks.py FILE INDEX...    (INDEX: the hunk's position in `git diff -U0 -- FILE` against the index)
       stage_hunks.py FILE all
"""
import subprocess
import sys

path, picks = sys.argv[1], sys.argv[2:]
diff = subprocess.run(["git", "diff", "-U0", "--", path], capture_output=True, text=True, check=True).stdout
lines = diff.splitlines(keepends=True)
head = []
hunks = []
for line in lines:
    if line.startswith("@@"):
        hunks.append([line])
    elif hunks:
        hunks[-1].append(line)
    else:
        head.append(line)
chosen = range(len(hunks)) if picks == ["all"] else [int(p) for p in picks]
patch = "".join(head) + "".join("".join(hunks[k]) for k in chosen)
subprocess.run(["git", "apply", "--cached", "--unidiff-zero", "-"], input=patch, text=True, check=True)
print(f"{path}: staged hunks {list(chosen)} of {len(hunks)}")
