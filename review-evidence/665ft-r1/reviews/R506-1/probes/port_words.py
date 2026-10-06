#!/usr/bin/env python3
"""Probe (R506-1): every hand-rolled check's words at the base, found at the head.
Usage: port_words.py <repo> <base> <head>
For each base C test, the first string literal of each check()/check_eq()/bound()
call site; then the count of head test files carrying that literal."""
import re, subprocess, sys
repo, base, head = sys.argv[1:4]
def show(rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True).stdout
pairs = {"sw/firmware/ctrl/test/test_adp.c": "sw/firmware/ctrl/test/test_adp.cpp",
         "sw/firmware/ctrl/test/test_port_loop.c": "sw/firmware/ctrl/test/test_port_loop.cpp"}
call = re.compile(r'\b(check|check_eq|bound)\(\s*"((?:[^"\\]|\\.)*)"', re.S)
total = missing = 0
for old, new in pairs.items():
    src = show(base, old); dst = show(head, new)
    words = [m.group(2) for m in call.finditer(src)]
    lost = [w for w in words if f'"{w}"' not in dst]
    total += len(words); missing += len(lost)
    print(f"{old}: {len(words)} literal call sites, {len(words) - len(lost)} found verbatim in {new}")
    for w in lost:
        print(f"   NOT FOUND: {w}")
print(f"total {total}, not found {missing}")
