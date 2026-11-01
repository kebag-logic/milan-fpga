#!/usr/bin/env python3
"""Compare the parsed program of one Python file between two commits.

Usage: soc_ast_same.py <repo> <old> <new> <path>. Exit 0 when the ASTs are equal.
"""
import ast
import subprocess
import sys

repo, old, new, path = sys.argv[1:5]


def tree(rev):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout
    return ast.dump(ast.parse(text), include_attributes=False)


same = tree(old) == tree(new)
print(f"{path} {old[:8]} -> {new[:8]}: parsed program {'IDENTICAL' if same else 'DIFFERS'}")
sys.exit(0 if same else 1)
