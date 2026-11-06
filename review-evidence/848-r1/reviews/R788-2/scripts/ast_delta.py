#!/usr/bin/env python3
"""Compare two versions of a module def by def, on the AST with docstrings removed.

Usage: python3 -I ast_delta.py OLD.py NEW.py

A rejoined statement or reflowed docstring leaves the AST of its definition unchanged, so any definition
named here changed in meaning; every other definition changed, at most, in layout or docstring wording.
"""
import ast
import sys
from pathlib import Path


def strip(node):
    for item in ast.walk(node):
        if isinstance(item, (ast.FunctionDef, ast.ClassDef, ast.Module)) and item.body:
            first = item.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) \
                    and isinstance(first.value.value, str):
                item.body = item.body[1:] or [ast.Pass()]
    return node


def table(path):
    tree = strip(ast.parse(Path(path).read_text(encoding="utf-8")))
    out = {}
    for index, node in enumerate(tree.body):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out[node.name] = ast.dump(node)
        else:
            names = [t.id for s in [node] for t in getattr(s, "targets", []) if isinstance(t, ast.Name)]
            out[names[0] if names else f"stmt:{type(node).__name__}:{ast.dump(node)[:60]}"] = ast.dump(node)
    return out


def main():
    old, new = table(sys.argv[1]), table(sys.argv[2])
    changed = sorted(k for k in old.keys() & new.keys() if old[k] != new[k])
    print("definitions compared:", len(old.keys() & new.keys()))
    print("only in old:", sorted(old.keys() - new.keys()))
    print("only in new:", sorted(new.keys() - old.keys()))
    print("AST changed:", changed)


if __name__ == "__main__":
    main()
