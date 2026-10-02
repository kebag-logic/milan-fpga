#!/usr/bin/env python3
"""List which functions of the eight drivers are AST-identical, changed, removed or added between two commits."""
import ast
import subprocess
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from ast_tables import DRIVERS, show  # noqa: E402


def functions(src: str) -> dict[str, str]:
    return {n.name: ast.dump(n) for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)}


base, head = sys.argv[1], sys.argv[2]
for path in DRIVERS:
    a, b = functions(show(base, path)), functions(show(head, path))
    print(path)
    print("  identical:", sorted(k for k in a if k in b and a[k] == b[k]))
    print("  changed:  ", sorted(k for k in a if k in b and a[k] != b[k]))
    print("  removed:  ", sorted(set(a) - set(b)))
    print("  added:    ", sorted(set(b) - set(a)))
