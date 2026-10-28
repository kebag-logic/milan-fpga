#!/usr/bin/env python3
"""ast_compare.py <a.py> <b.py>: equal when the two files differ only in comments and docstrings."""
import ast, sys

def norm(path):
    t = ast.parse(open(path, encoding="utf-8").read())
    for n in ast.walk(t):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            b = n.body
            if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], "value", None), ast.Constant) and isinstance(b[0].value.value, str):
                n.body = b[1:] or [ast.Pass()]
    return ast.dump(t, include_attributes=False)

a, b = norm(sys.argv[1]), norm(sys.argv[2])
print("AST-EQUAL (comments/docstrings only)" if a == b else "AST-DIFFERENT")
sys.exit(0 if a == b else 1)
