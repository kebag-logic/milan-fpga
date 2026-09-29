#!/usr/bin/env python3
"""Compare every hdl/ file changed between two commits with comments and
whitespace stripped. Exit 0 only if every change is comment/whitespace-only.
Usage: rtl_comment_only.py <repo> <base> <head>"""
import re, subprocess, sys

def strip(src: str) -> str:
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    src = re.sub(r"//[^\n]*", " ", src)
    return " ".join(src.split())

repo, base, head = sys.argv[1:4]
git = lambda *a: subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True).stdout
files = [f for f in git("diff", "--name-only", f"{base}..{head}", "--", "hdl/").split() if f]
bad = 0
for f in files:
    a, b = strip(git("show", f"{base}:{f}")), strip(git("show", f"{head}:{f}"))
    same = a == b
    bad += not same
    print(f"{'COMMENT-ONLY' if same else 'LOGIC-CHANGED'} {f} (stripped sha-eq={same}, len {len(a)} vs {len(b)})")
print(f"{len(files)} hdl files changed, {bad} with non-comment change")
sys.exit(1 if bad else 0)
