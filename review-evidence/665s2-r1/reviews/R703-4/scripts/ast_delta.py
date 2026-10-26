#!/usr/bin/env python3
"""ast_delta.py OLD NEW: is NEW's code (docstrings and comments removed) identical to OLD's?"""
import ast, sys
def strip(src):
    t = ast.parse(src)
    for n in ast.walk(t):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) and n.body \
           and isinstance(n.body[0], ast.Expr) and isinstance(getattr(n.body[0], 'value', None), ast.Constant) \
           and isinstance(n.body[0].value.value, str):
            n.body = n.body[1:] or [ast.Pass()]
    return ast.dump(t)
a, b = (open(p).read() for p in sys.argv[1:3])
print('code-identical' if strip(a) == strip(b) else 'CODE DIFFERS')
