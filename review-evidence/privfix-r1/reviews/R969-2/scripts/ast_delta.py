#!/usr/bin/env python3
"""Compare base and head Python files by AST, docstrings and string constants masked.

Reports per file whether the masked trees are identical and how many string
constants changed. Removed (base) strings are printed only as sha256 prefixes,
so the receipt never re-publishes a removed literal; head strings are printed.
Usage: ast_delta.py <repo> <base> <head> <path>...
"""
import ast
import hashlib
import subprocess
import sys


def blob(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True).stdout.decode()


def mask(tree):
    consts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            consts.append(node.value)
            node.value = "<str>"
    return ast.dump(tree), consts


repo, base, head, *paths = sys.argv[1:]
for p in paths:
    b, bc = mask(ast.parse(blob(repo, base, p)))
    h, hc = mask(ast.parse(blob(repo, head, p)))
    changed = [(x, y) for x, y in zip(bc, hc) if x != y]
    print(f"{p}: {'STRUCTURE-IDENTICAL' if b == h else 'STRUCTURE-DIFFERS'}; "
          f"string constants base {len(bc)} head {len(hc)}, changed {len(changed)}")
    for x, y in changed:
        kind = "docstring/comment-like" if "\n" in x and len(x) > 80 else "literal"
        print(f"    - base sha256:{hashlib.sha256(x.encode()).hexdigest()[:16]} ({kind})")
        print(f"    + head {y[:120]!r}")
