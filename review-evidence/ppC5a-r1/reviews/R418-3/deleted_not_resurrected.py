#!/usr/bin/env python3
"""For a merge, flag lines a side deleted (vs base) that the merge still carries
more often than the side and the other side would allow.
usage: deleted_not_resurrected.py <repo> <base> <ours> <theirs> <merge> paths..."""
import subprocess, sys
from collections import Counter
def blob(repo, rev, p):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{p}"], capture_output=True)
    return Counter(r.stdout.decode("utf-8", "replace").splitlines()) if r.returncode == 0 else Counter()
repo, base, ours, theirs, merge = sys.argv[1:6]
n = 0
for p in sys.argv[6:]:
    b, o, t, m = (blob(repo, r, p) for r in (base, ours, theirs, merge))
    for ln in set(b) | set(o) | set(t):
        if not ln.strip():
            continue
        # three-way expected count: base + (ours-base) + (theirs-base)
        want = b[ln] + (o[ln] - b[ln]) + (t[ln] - b[ln])
        if m[ln] > max(want, 0) and (o[ln] < b[ln] or t[ln] < b[ln]):
            n += 1
            print(f"{p}: base {b[ln]} ours {o[ln]} theirs {t[ln]} merge {m[ln]}: {ln[:140]}")
print(f"TOTAL resurrected-candidates: {n}")
