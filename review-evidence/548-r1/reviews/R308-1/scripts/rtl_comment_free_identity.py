#!/usr/bin/env python3
"""Compare comment-free RTL bytes of two commits for the given paths.

Usage: rtl_comment_free_identity.py REPO BASE HEAD PATH...
Strips // and /* */ comments outside string literals, then trailing
whitespace and blank lines, and prints sha256 per side plus a verdict.
"""
import hashlib, subprocess, sys

def strip(src: str) -> str:
    out, i, n, state = [], 0, len(src), "code"
    while i < n:
        c = src[i]
        if state == "code":
            if src.startswith("//", i):
                j = src.find("\n", i)
                i = n if j < 0 else j
                continue
            if src.startswith("/*", i):
                j = src.find("*/", i + 2)
                seg = src[i:(n if j < 0 else j + 2)]
                out.append("\n" * seg.count("\n"))
                i = n if j < 0 else j + 2
                continue
            if c == '"':
                state = "str"
            out.append(c)
        else:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(src[i + 1]); i += 2; continue
            if c == '"':
                state = "code"
        i += 1
    lines = [l.rstrip() for l in "".join(out).splitlines()]
    return "\n".join(l for l in lines if l) + "\n"

def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout

repo, base, head, *paths = sys.argv[1:]
ok = True
for p in paths:
    a, b = strip(show(repo, base, p)), strip(show(repo, head, p))
    ha, hb = (hashlib.sha256(x.encode()).hexdigest() for x in (a, b))
    same = a == b
    ok &= same
    print(f"{p}\n  base {base[:12]} {ha}\n  head {head[:12]} {hb}\n  comment-free identical: {same}")
print("VERDICT", "IDENTICAL" if ok else "DIFFERENT")
sys.exit(0 if ok else 1)
