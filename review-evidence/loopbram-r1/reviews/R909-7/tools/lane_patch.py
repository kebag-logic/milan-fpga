#!/usr/bin/env python3
"""The lane's net change per file, before and after the merge: equal line sets mean the merge altered none of it.

usage: lane_patch.py REPO BASE OLD DEV HEAD
"""
import subprocess, sys
repo, base, old, dev, head = sys.argv[1:]
def g(*a): return subprocess.check_output(["/usr/bin/git", "-C", repo, *a], text=True, errors="replace")
def net(x, y, f): return [l for l in g("diff", "-U0", x, y, "--", f).splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))]
files = sorted(set(g("diff", "--name-only", base, old).split()) | set(g("diff", "--name-only", dev, head).split()))
same = []
for f in files:
    a, b = net(base, old, f), net(dev, head, f)
    if a == b: same.append(f)
    else: print(f"CHANGED {f}: lane net lines {len(a)} -> {len(b)}; only-old {len([l for l in a if l not in b])}, only-new {len([l for l in b if l not in a])}")
print("same:", len(same)); print("\n".join("  " + f for f in same))
