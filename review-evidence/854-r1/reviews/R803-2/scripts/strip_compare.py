#!/usr/bin/env python3
"""strip_compare.py <repo> <rev-a> <rev-b> <path>...: compare SystemVerilog files at two revisions after removing
// and /* */ comments and collapsing whitespace; prints SAME or DIFFERENT per path, exit 1 if any differ."""
import re, subprocess, sys
repo, a, b, paths = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
def strip(text):
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"//[^\n]*", " ", text)
    return " ".join(text.split())
bad = 0
for p in paths:
    x = [strip(subprocess.run(["git", "-C", repo, "show", f"{r}:{p}"], capture_output=True, text=True, check=True).stdout) for r in (a, b)]
    same = x[0] == x[1]; bad |= not same
    print(("SAME" if same else "DIFFERENT"), a, b, p)
sys.exit(bad)
