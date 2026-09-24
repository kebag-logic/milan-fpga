#!/usr/bin/env python3
"""Reviewer-owned check that hdl/ changes between two commits are comment-only.

Usage: hdl_comment_only_check.py <repo> <base> <head>
1. Every added/removed line in `git diff -U0 base head -- hdl/` must be a
   whole-line // comment (or blank).
2. Each changed hdl file, tokenised with a SystemVerilog-aware stripper that
   removes // and /* */ comments outside string literals and then drops all
   whitespace, must be identical at both commits.
Exits 0 only if both hold.
"""
import hashlib, re, subprocess, sys

def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True).stdout

def strip(src: str) -> str:
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == '\\' else 1
            out.append(src[i:j + 1]); i = j + 1
        elif src.startswith('//', i):
            j = src.find('\n', i); i = n if j < 0 else j
        elif src.startswith('/*', i):
            j = src.find('*/', i + 2); i = n if j < 0 else j + 2
        else:
            out.append(c); i += 1
    return re.sub(r'\s+', '', ''.join(out))

repo, base, head = sys.argv[1:4]
ok = True
diff = git(repo, "diff", "-U0", "--no-color", base, head, "--", "hdl/").decode()
changed, bad = 0, []
for ln in diff.splitlines():
    if ln.startswith(('+++', '---')):
        continue
    if ln[:1] in '+-':
        changed += 1
        body = ln[1:].strip()
        if body and not body.startswith('//'):
            bad.append(ln)
print(f"changed hdl diff lines: {changed}; non-comment lines: {len(bad)}")
for b in bad:
    print("  NONCOMMENT:", b); ok = False
files = git(repo, "diff", "--name-only", base, head, "--", "hdl/").decode().split()
for f in files:
    a = strip(git(repo, "show", f"{base}:{f}").decode())
    b = strip(git(repo, "show", f"{head}:{f}").decode())
    ha, hb = hashlib.sha256(a.encode()).hexdigest(), hashlib.sha256(b.encode()).hexdigest()
    same = a == b
    ok &= same
    print(f"{f}: stripped sha256 base={ha} head={hb} identical={same}")
print("RESULT:", "PASS comment-only" if ok else "FAIL")
sys.exit(0 if ok else 1)
