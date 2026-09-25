#!/usr/bin/env python3
"""Compare two versions of a Python file ignoring function docstrings.
Usage: docstring-ast.py <old.py> <new.py>"""
import ast, sys
def strip(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.body \
           and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant) \
           and isinstance(node.body[0].value.value, str):
            node.body = node.body[1:]
    return ast.dump(tree)
print("AST identical excluding function docstrings:", strip(sys.argv[1]) == strip(sys.argv[2]))
