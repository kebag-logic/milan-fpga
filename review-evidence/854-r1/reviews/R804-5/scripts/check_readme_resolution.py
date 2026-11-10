#!/usr/bin/env python3
"""Check that docs/findings/README.md at HEAD is base with the 234 row from
the PR side and the 649 row from the dev side, nothing else changed.
Usage: check_readme_resolution.py <repo> <base> <pr_side> <dev_side> <head>"""
import subprocess, sys
repo, base, ours, theirs, head = sys.argv[1:6]
P = "docs/findings/README.md"
def lines(rev):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{P}"], check=True,
                          capture_output=True, text=True).stdout.splitlines(True)
B, O, T, H = (lines(r) for r in (base, ours, theirs, head))
def changed(a, b):
    assert len(a) == len(b), (len(a), len(b))
    return [i for i in range(len(a)) if a[i] != b[i]]
co, ct, ch = changed(B, O), changed(B, T), changed(B, H)
print("line counts base/pr/dev/head:", len(B), len(O), len(T), len(H))
print("lines changed by PR side (0-based):", co)
print("lines changed by dev side:", ct)
print("lines changed at head vs base:", ch)
ok = True
for i in range(len(H)):
    if i in co:
        want = O[i]; src = "pr"
    elif i in ct:
        want = T[i]; src = "dev"
    else:
        want = B[i]; src = "base"
    if H[i] != want:
        ok = False; print(f"MISMATCH line {i+1} (expected {src})")
    elif i in co or i in ct:
        print(f"line {i+1}: head == {src} side; starts {H[i][:60]!r}")
print("overlap:", sorted(set(co) & set(ct)))
print("RESULT:", "PASS" if ok and not (set(co) & set(ct)) else "FAIL")
sys.exit(0 if ok else 1)
