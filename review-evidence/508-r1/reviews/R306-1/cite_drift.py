#!/usr/bin/env python3
"""List processor source line citations in the tracked tree (outside docs/history)
whose cited line text differs between two processor revisions.
Usage: cite_drift.py <superproject root> <old rev> <new rev>"""
import re, subprocess, sys
root, old, new = sys.argv[1:4]
pp = f"{root}/protocol-processor"
files = subprocess.run(["git", "-C", root, "ls-files"], capture_output=True, text=True).stdout.split()
pat = re.compile(r"((?:hdl|tb)/[\w/]+\.(?:sv|svh|cpp|hpp|py)):(\d+)(?:-(\d+))?((?:,\s*\d+(?:-\d+)?)*)")
cache = {}
def lines(rev, path):
    k = (rev, path)
    if k not in cache:
        r = subprocess.run(["git", "-C", pp, "show", f"{rev}:{path}"], capture_output=True, text=True)
        cache[k] = r.stdout.splitlines() if r.returncode == 0 else None
    return cache[k]
for f in files:
    if f.startswith("docs/history") or f.startswith("protocol-processor"):
        continue
    try:
        txt = open(f"{root}/{f}", encoding="utf-8", errors="replace").read()
    except (IsADirectoryError, FileNotFoundError):
        continue
    for ln, line in enumerate(txt.splitlines(), 1):
        for m in pat.finditer(line):
            path = m.group(1)
            if lines(new, path) is None:
                continue
            spans = [m.group(2) + (f"-{m.group(3)}" if m.group(3) else "")]
            spans += [s.strip() for s in m.group(4).split(",") if s.strip()]
            for sp in spans:
                a, _, b = sp.partition("-")
                lo, hi = int(a), int(b or a)
                o, n = lines(old, path), lines(new, path)
                if o is None:
                    continue
                if o[lo-1:hi] != n[lo-1:hi]:
                    print(f"{f}:{ln}: {path}:{sp} differs between {old[:8]} and {new[:8]}")
