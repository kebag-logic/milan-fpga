#!/usr/bin/env python3
"""Show that a commit changes only the module docstring of a Python file.
Usage: ast_probe.py <repo> <old-rev> <new-rev> <path>"""
import ast, subprocess, sys
repo, old, new, path = sys.argv[1:5]
def load(rev):
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                         check=True, capture_output=True, text=True).stdout
    tree = ast.parse(src)
    doc = ast.get_docstring(tree, clean=False)
    body = tree.body[1:] if doc is not None else tree.body
    return doc, ast.dump(ast.Module(body=body, type_ignores=[]))
(d0, b0), (d1, b1) = load(old), load(new)
print("docstring_changed", d0 != d1)
print("code_after_docstring_identical", b0 == b1)
sys.exit(0 if (d0 != d1 and b0 == b1) else 1)
