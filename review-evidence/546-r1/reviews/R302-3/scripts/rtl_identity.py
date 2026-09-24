#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R302-3: comment-free identity of every tracked HDL file between two commits.

Usage: rtl_identity.py <clone> <old-commit> <new-commit>
Strips // and /* */ comments (string-literal aware) and folds whitespace, then
compares sha256 per path. Also reports raw byte identity. Exit 0 iff every
tracked hdl/ path present at either commit is comment-free identical.
"""
import hashlib, re, subprocess, sys

def git(c, *a):
    return subprocess.run(["git", "-C", c, *a], check=True, capture_output=True).stdout

def strip(src: str) -> str:
    out, i, n = [], 0, len(src)
    while i < n:
        ch = src[i]
        if ch == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            out.append(src[i:j + 1]); i = j + 1
        elif src.startswith("//", i):
            j = src.find("\n", i); i = n if j < 0 else j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2); i = n if j < 0 else j + 2; out.append(" ")
        else:
            out.append(ch); i += 1
    return re.sub(r"\s+", " ", "".join(out)).strip()

def files(c, rev):
    lines = git(c, "ls-tree", "-r", rev, "--", "hdl").decode().splitlines()
    return {l.split("\t", 1)[1]: l.split()[2] for l in lines
            if l.split()[0] != "160000" and re.search(r"\.(sv|v|svh|vh)$", l)}

def main():
    c, old, new = sys.argv[1:4]
    a, b = files(c, old), files(c, new)
    bad = 0
    raw_changed = []
    for p in sorted(set(a) | set(b)):
        if p not in a or p not in b:
            print(f"MISSING {p} old={p in a} new={p in b}"); bad += 1; continue
        if a[p] != b[p]:
            raw_changed.append(p)
        ha = hashlib.sha256(strip(git(c, "cat-file", "blob", a[p]).decode()).encode()).hexdigest()
        hb = hashlib.sha256(strip(git(c, "cat-file", "blob", b[p]).decode()).encode()).hexdigest()
        if ha != hb:
            print(f"DIFF {p} {ha} {hb}"); bad += 1
        elif a[p] != b[p]:
            print(f"COMMENT-ONLY {p} old-blob={a[p]} new-blob={b[p]} normalized={ha}")
    print(f"old={old} new={new}")
    print(f"hdl files compared: {len(set(a) | set(b))}; raw-byte changed: {len(raw_changed)}; comment-free mismatches: {bad}")
    print("overall:", "PASS" if bad == 0 else "FAIL")
    return 1 if bad else 0

if __name__ == "__main__":
    raise SystemExit(main())
