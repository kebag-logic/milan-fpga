#!/usr/bin/env python3
"""Show that two versions of a Python file differ only in function docstrings,
and list public functions lacking docstrings or annotations in the second.
Usage: ast_docstring_only.py <old.py> <new.py>"""
import ast
import sys


def strip(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.body \
                and isinstance(node.body[0], ast.Expr) \
                and isinstance(getattr(node.body[0], "value", None), ast.Constant) \
                and isinstance(node.body[0].value.value, str):
            node.body = node.body[1:]
    return ast.dump(tree)


old, new = (ast.parse(open(p, encoding="utf-8").read()) for p in sys.argv[1:3])
same = strip(old) == strip(ast.parse(open(sys.argv[2], encoding="utf-8").read()))
print("ast identical excluding function docstrings:", same)
for n in ast.walk(new):
    if isinstance(n, ast.FunctionDef) and not n.name.startswith("_"):
        print(f"  {n.name}: docstring={ast.get_docstring(n) is not None} "
              f"returns_annotated={n.returns is not None} "
              f"args_annotated={all(a.annotation is not None for a in n.args.args)}")
sys.exit(0 if same else 1)
