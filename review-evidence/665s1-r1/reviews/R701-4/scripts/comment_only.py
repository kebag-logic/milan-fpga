#!/usr/bin/env python3
"""Show that a delta's Python files differ only in comments and docstrings.
Usage: script REPO BASE HEAD PATH...  (reads blobs with git show; writes nothing)."""
import ast, subprocess, sys
repo, base, head, *paths = sys.argv[1:]
def tree(rev, path):
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, check=True, text=True).stdout
    t = ast.parse(src)
    for n in ast.walk(t):
        body = getattr(n, "body", None)
        if isinstance(body, list) and body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) and isinstance(body[0].value.value, str):
            body[0] = ast.Pass()
    return ast.dump(t)
bad = 0
for p in paths:
    same = tree(base, p) == tree(head, p)
    bad += not same
    print(("SAME-AST " if same else "CODE-DIFF ") + p)
sys.exit(1 if bad else 0)
