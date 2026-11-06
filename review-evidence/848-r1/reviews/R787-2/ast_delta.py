#!/usr/bin/env python3
"""Compare two versions of a Python module statement by statement, docstrings removed.

Usage: ast_delta.py OLD.py NEW.py. Prints every top-level name whose code differs, so a
reformatting (a rejoined statement, a rewrapped docstring) shows up as no difference.
"""
import ast
import sys


def strip(node):
    for sub in ast.walk(node):
        if isinstance(sub, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
            body = sub.body
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                    and isinstance(body[0].value.value, str):
                sub.body = body[1:] or [ast.Pass()]
    return node


def table(path):
    tree = strip(ast.parse(open(path, encoding="utf-8").read()))
    out = {}
    for index, node in enumerate(tree.body):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            key = node.name
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            target = node.targets[0] if isinstance(node, ast.Assign) else node.target
            key = ast.unparse(target)
        else:
            key = f"stmt:{ast.unparse(node)[:50]}"
        out[key] = ast.dump(node)
    return out


old, new = table(sys.argv[1]), table(sys.argv[2])
same = [k for k in old if k in new and old[k] == new[k]]
print(f"identical top-level names: {len(same)}")
for key in sorted(set(old) | set(new)):
    if key not in old:
        print("ADDED  ", key)
    elif key not in new:
        print("REMOVED", key)
    elif old[key] != new[key]:
        print("CHANGED", key)
