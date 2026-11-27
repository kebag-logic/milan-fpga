#!/usr/bin/env python3
"""Compare named top-level function definitions between two revisions of
(possibly different) Python files by their AST dump."""
import ast, subprocess, sys
REPO, REV_A, PATH_A, REV_B, PATH_B, *NAMES = sys.argv[1:]
def defs(rev, path):
    t = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                       capture_output=True, text=True, check=True).stdout
    return {n.name: ast.dump(n) for n in ast.parse(t).body if isinstance(n, ast.FunctionDef)}
a, b = defs(REV_A, PATH_A), defs(REV_B, PATH_B)
for n in NAMES:
    print(n, "IDENTICAL" if n in a and a.get(n) == b.get(n) else "DIFFERENT")
