#!/usr/bin/env python3
"""Compare two Python sources as programs with every docstring removed.

usage: ast_equiv.py OLD NEW
Prints IDENTICAL, or a unified diff of the unparsed docstring-free programs.
"""
import ast, difflib, sys

def strip(src: str) -> str:
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)

old, new = (strip(open(p).read()) for p in sys.argv[1:3])
if old == new:
    print("IDENTICAL")
else:
    sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), new.splitlines(True), sys.argv[1], sys.argv[2]))
