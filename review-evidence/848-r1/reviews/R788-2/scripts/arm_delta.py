#!/usr/bin/env python3
"""Compare the planted control arms of two versions of docs_inventory.py, arm by arm.

Usage: python3 -I arm_delta.py OLD.py NEW.py

An arm is a tuple whose first element is a string literal inside selftest() or copy_controls().
Arms are compared on their source form, normalised by the AST, so a rejoined arm compares equal.
"""
import ast
import sys
from pathlib import Path


def arms(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    found = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ("selftest", "copy_controls"):
            for item in ast.walk(node):
                if isinstance(item, ast.Tuple) and len(item.elts) >= 3 and isinstance(item.elts[0], ast.Constant) \
                        and isinstance(item.elts[0].value, str) and isinstance(item.elts[2], ast.Constant) \
                        and isinstance(item.elts[2].value, int):
                    found[item.elts[0].value] = ast.unparse(item)
    return found


def main():
    old, new = arms(sys.argv[1]), arms(sys.argv[2])
    print(f"arms: old {len(old)}, new {len(new)}")
    print("removed:")
    for name in sorted(old.keys() - new.keys()):
        print("  -", name)
    print("added:")
    for name in sorted(new.keys() - old.keys()):
        print("  +", name)
    print("changed:")
    for name in sorted(old.keys() & new.keys()):
        if old[name] != new[name]:
            print("  ~", name)
            print("    old:", old[name][:260])
            print("    new:", new[name][:260])


if __name__ == "__main__":
    main()
