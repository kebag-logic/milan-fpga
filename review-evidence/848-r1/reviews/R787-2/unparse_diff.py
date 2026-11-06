#!/usr/bin/env python3
"""Print a unified diff of the named functions after normalising layout through ast.unparse.

Usage: unparse_diff.py OLD.py NEW.py NAME... A statement that was only rejoined produces no diff line.
"""
import ast
import difflib
import sys


def function(path, name):
    tree = ast.parse(open(path, encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            text = ast.unparse(node)
            # One arm or element per line, so the diff is read per statement.
            return text.replace("), (", "),\n(").split("\n")
    return []


for name in sys.argv[3:]:
    print(f"#### {name}")
    for line in difflib.unified_diff(function(sys.argv[1], name), function(sys.argv[2], name), lineterm="", n=0):
        if not line.startswith(("---", "+++", "@@")):
            print(line[:330])
