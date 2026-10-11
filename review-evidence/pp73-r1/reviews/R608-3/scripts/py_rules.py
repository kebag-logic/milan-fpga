#!/usr/bin/env python3
"""Approximate the parent's Rule 12 budgets over the gate package (read-only).

Usage: py_rules.py FILE...
Reports module lines > 1000, functions > 100 lines, > 6 parameters, and public
(no leading underscore, module-level or method) functions lacking a docstring
or full annotations. This is a reviewer approximation, not the parent's tool.
"""
import ast
import sys
from pathlib import Path


def main() -> int:
    bad = 0
    for name in sys.argv[1:]:
        src = Path(name).read_text(encoding="utf-8")
        lines = src.count("\n") + 1
        if lines > 1000:
            print(f"{name}: module {lines} lines > 1000"); bad += 1
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            n = node.end_lineno - node.lineno + 1
            a = node.args
            params = a.posonlyargs + a.args + a.kwonlyargs
            if n > 100:
                print(f"{name}:{node.lineno} {node.name}: {n} lines > 100"); bad += 1
            if len(params) > 6:
                print(f"{name}:{node.lineno} {node.name}: {len(params)} params > 6"); bad += 1
            if node.name.startswith("_"):
                continue
            if ast.get_docstring(node) is None:
                print(f"{name}:{node.lineno} {node.name}: public, undocumented"); bad += 1
            unann = [p.arg for p in params if p.annotation is None and p.arg not in ("self", "cls")]
            if unann or node.returns is None:
                print(f"{name}:{node.lineno} {node.name}: public, unannotated {unann}"
                      f"{' (no return)' if node.returns is None else ''}"); bad += 1
    print(f"py_rules: {len(sys.argv) - 1} files, {bad} budget hits")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
