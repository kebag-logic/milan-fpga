#!/usr/bin/env python3
"""Resolve every relative Markdown link with a fragment that the delta adds.
Usage: check_delta_anchors.py <clone> <old> <new>"""
import re, subprocess, sys, posixpath
clone, old, new = sys.argv[1:4]
diff = subprocess.run(["git", "-C", clone, "diff", "-U0", old, new, "--", "*.md"], capture_output=True, text=True).stdout
def slug(h):
    h = h.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")
cache = {}
def anchors(path):
    if path not in cache:
        t = subprocess.run(["git", "-C", clone, "show", f"{new}:{path}"], capture_output=True, text=True).stdout
        cache[path] = {slug(m.group(1)) for m in re.finditer(r"^#+ (.*)$", t, re.M)}
    return cache[path]
cur = None; n = 0; bad = 0
for line in diff.splitlines():
    if line.startswith("+++ b/"):
        cur = line[6:]; continue
    if not line.startswith("+") or line.startswith("+++"):
        continue
    for tgt in re.findall(r"\]\(([^)\s]+)\)", line):
        if tgt.startswith("http"):
            continue
        p, _, frag = tgt.partition("#")
        path = posixpath.normpath(posixpath.join(posixpath.dirname(cur), p)) if p else cur
        ok = subprocess.run(["git", "-C", clone, "cat-file", "-e", f"{new}:{path}"]).returncode == 0
        if ok and frag:
            ok = frag in anchors(path)
        n += 1
        if not ok:
            bad += 1
        print(("OK  " if ok else "BAD ") + f"{cur}: {tgt}")
print(f"links {n} bad {bad}")
sys.exit(1 if bad else 0)
