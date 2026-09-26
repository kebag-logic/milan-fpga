#!/usr/bin/env python3
"""Show that a Python file's executable content is unchanged between trees.

Usage: ast_delta.py OLD_TREE NEW_TREE PATH [PATH ...]

Each file is parsed and normalised: docstrings, parameter/return annotations
and `from typing import ...` are removed, and so is any `timeout=` keyword on a
call. The script then prints, per path:
- whether the raw ASTs are equal;
- whether the normalised ASTs are equal (only those four kinds of edit);
- whether a `timeout=` keyword is present in each version.
Exit 0 when every path's normalised AST is equal.
"""
import ast
import sys
from pathlib import Path


class Strip(ast.NodeTransformer):
    def _undoc(self, node):
        body = node.body
        if body and isinstance(body[0], ast.Expr) and isinstance(
                getattr(body[0], "value", None), ast.Constant) and isinstance(
                body[0].value.value, str):
            node.body = body[1:] or [ast.Pass()]
        return node

    def visit_Module(self, node):
        self.generic_visit(node)
        node.body = [n for n in node.body if not (
            isinstance(n, ast.ImportFrom) and n.module == "typing")]
        return self._undoc(node)

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        return self._undoc(node)

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        node.returns = None
        for a in node.args.args + node.args.kwonlyargs + node.args.posonlyargs:
            a.annotation = None
        return self._undoc(node)

    def visit_Call(self, node):
        self.generic_visit(node)
        node.keywords = [k for k in node.keywords if k.arg != "timeout"]
        return node


def has_timeout(tree):
    return any(isinstance(n, ast.keyword) and n.arg == "timeout"
               for n in ast.walk(tree))


old, new = Path(sys.argv[1]), Path(sys.argv[2])
rc = 0
for rel in sys.argv[3:]:
    a = ast.parse((old / rel).read_text())
    b = ast.parse((new / rel).read_text())
    raw = ast.dump(a) == ast.dump(b)
    ta, tb = has_timeout(a), has_timeout(b)
    norm = ast.dump(Strip().visit(a)) == ast.dump(Strip().visit(b))
    print(f"{rel}: raw AST {'equal' if raw else 'differs'}; normalised AST "
          f"{'EQUAL' if norm else 'DIFFERS'}; timeout= old={ta} new={tb}")
    rc |= not norm
sys.exit(rc)
