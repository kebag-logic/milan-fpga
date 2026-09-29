#!/usr/bin/env python3
"""Line-exact check of the docs/findings/README.md merge resolution.
Usage: run from the repository root. Prints the rows unique to each side and
asserts the merged file equals the three-way expectation."""
import subprocess, sys
def show(rev):
    return subprocess.run(["git", "show", f"{rev}:docs/findings/README.md"],
                          check=True, capture_output=True).stdout.decode().splitlines(keepends=True)
base, dev, src, mrg, cand = (show(r) for r in
    ("13eda870", "79c36963", "5c579274", "d62b1e1a", "61752396"))
ok = True
added_dev = [l for l in dev if l not in base]
removed_dev = [l for l in base if l not in dev]
added_src = [l for l in src if l not in base]
removed_src = [l for l in base if l not in src]
print("dev added:", len(added_dev), "dev removed:", len(removed_dev))
print("src added:", len(added_src), "src removed:", len(removed_src))
for l in added_dev + added_src:
    if l not in mrg: print("MISSING in merge:", l[:90]); ok = False
for l in removed_dev + removed_src:
    if l in mrg: print("RESURRECTED in merge:", l[:90]); ok = False
extra = [l for l in mrg if l not in base and l not in added_dev and l not in added_src]
print("merge-only lines:", len(extra)); ok &= not extra
# expected order: base with dev's 451 row inserted above the rewritten #75 row
exp = []
for l in base:
    if l in removed_src:
        exp.extend(added_dev)  # the 451 row sits directly above the #75 row on dev
        exp.extend(added_src)
    else:
        exp.append(l)
print("merge == expected order:", mrg == exp); ok &= (mrg == exp)
print("candidate == merge:", cand == mrg); ok &= (cand == mrg)
print("line count base/dev/src/merge:", len(base), len(dev), len(src), len(mrg))
print("RESULT", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
