#!/usr/bin/env python3
"""Stage the zero-context hunks of one file whose changed lines match a regex (or --all).

Usage: stage_hunks.py <file> <regex> [--invert]   (run from the repository root)
Prints each hunk it stages; applies them to the index with git apply --cached --unidiff-zero.
"""
import re
import subprocess
import sys

path, rx = sys.argv[1], re.compile(sys.argv[2])
invert = "--invert" in sys.argv
diff = subprocess.run(["git", "diff", "-U0", "--", path], capture_output=True, text=True, check=True).stdout
lines = diff.splitlines(keepends=True)
head, hunks, cur = [], [], None
for ln in lines:
    if ln.startswith("@@"):
        cur = [ln]
        hunks.append(cur)
    elif cur is None:
        head.append(ln)
    else:
        cur.append(ln)
keep = []
for h in hunks:
    body = "".join(x[1:] for x in h[1:] if x[:1] in "+-")
    hit = bool(rx.search(body))
    if hit != invert:
        keep.append(h)
if not keep:
    print(f"{path}: no hunk matches")
    sys.exit(1)
patch = "".join(head) + "".join("".join(h) for h in keep)
subprocess.run(["git", "apply", "--cached", "--unidiff-zero", "-"], input=patch, text=True, check=True)
print(f"{path}: staged {len(keep)} of {len(hunks)} hunks")
