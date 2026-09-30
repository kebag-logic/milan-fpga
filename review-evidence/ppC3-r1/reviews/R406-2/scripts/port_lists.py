#!/usr/bin/env python3
"""Compare comment-stripped module headers (parameters and ports, up to the first ');')
of named modules between two revisions of a git repository.
usage: port_lists.py <repo> <rev-a> <rev-b> <path:module>..."""
import re, subprocess, sys
repo, ra, rb = sys.argv[1:4]
def header(rev, path, mod):
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    src = re.sub(r"//[^\n]*", " ", src)
    m = re.search(r"\bmodule\s+" + re.escape(mod) + r"\b(.*?)\);", src, flags=re.S)
    return m.group(1).split() if m else None
for spec in sys.argv[4:]:
    path, mod = spec.split(":")
    a, b = header(ra, path, mod), header(rb, path, mod)
    if a == b:
        print(f"IDENTICAL {mod} ({len(a)} tokens)")
    else:
        sa, sb = " ".join(a).split(","), " ".join(b).split(",")
        print(f"DIFFERS {mod}: only in {rb}: {[x.strip() for x in sb if x not in sa]}; only in {ra}: {[x.strip() for x in sa if x not in sb]}")
