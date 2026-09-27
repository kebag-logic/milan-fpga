#!/usr/bin/env python3
"""Report whether Python files differ between two commits only in comments
and docstrings. Run from the repository root.

Usage: ast_equal.py <base-rev> <head-rev> <path>...
"""
import ast
import subprocess
import sys


def stripped(src: str) -> str:
    tree = ast.parse(src)
    for node in ast.walk(tree):
        body = getattr(node, 'body', None)
        if (isinstance(body, list) and body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)):
            body[0] = ast.Pass()
    return ast.dump(tree, include_attributes=False)


def main() -> int:
    base, head, *paths = sys.argv[1:]
    rc = 0
    for path in paths:
        srcs = [subprocess.run(['git', 'show', f'{rev}:{path}'], check=True,
                               capture_output=True, text=True).stdout
                for rev in (base, head)]
        same = stripped(srcs[0]) == stripped(srcs[1])
        print(f'{path}: executable AST {"IDENTICAL" if same else "DIFFERS"}'
              f' (raw text {"identical" if srcs[0] == srcs[1] else "differs"})')
        rc |= 0 if same else 1
    return rc


if __name__ == '__main__':
    sys.exit(main())
