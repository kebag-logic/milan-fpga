#!/usr/bin/env python3
"""Verify local Markdown link fragments resolve to GitHub-style heading slugs.

usage: anchor_check.py DONOR_REPO [FILE ...]   (default: every tracked *.md)
"""
import re, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1])
files = sys.argv[2:] or subprocess.run(["git", "-C", str(root), "ls-files", "*.md"],
                                       capture_output=True, text=True).stdout.split()
LINK = re.compile(r"!?\[[^\]]*]\(([^)\s]+)\)")

def slugs(path):
    out, seen, fenced = set(), {}, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if fenced or not re.match(r"^#{1,6} ", line):
            continue
        t = re.sub(r"^#{1,6} ", "", line).strip().lower()
        t = re.sub(r"\[([^\]]*)]\([^)]*\)", r"\1", t)
        t = re.sub(r"[^\w\- ]", "", t).replace(" ", "-")
        n = seen.get(t, 0); seen[t] = n + 1
        out.add(t if n == 0 else f"{t}-{n}")
    return out

bad = checked = 0
for f in files:
    p = root / f
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        for raw in LINK.findall(line):
            if "://" in raw or "#" not in raw:
                continue
            target, frag = raw.split("#", 1)
            tp = (p.parent / target).resolve() if target else p
            if not tp.is_file() or tp.suffix != ".md":
                continue
            checked += 1
            ok = frag.lower() in slugs(tp)
            if not ok:
                bad += 1
            print(f"{'OK ' if ok else 'BAD'} {f}:{n} -> {target or '(self)'}#{frag}")
print(f"checked {checked} bad {bad}")
sys.exit(1 if bad else 0)
