#!/usr/bin/env python3
"""Compare top-level definitions of a Python file between two git revisions.

Usage: entrypoint_identity.py <repo> <rev-a> <rev-b> <path> [name ...]
Prints, for every top-level def/class (and each method of class MilanSoC),
whether its source text is identical at both revisions; names given on the
command line are marked as required and make the exit status 1 if they differ.
Also confirms every name imported from clock_constraints exists at rev-b.
"""
import ast
import subprocess
import sys


def source(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def units(text):
    tree = ast.parse(text)
    lines = text.splitlines()
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out[node.name] = "\n".join(lines[node.lineno - 1:node.end_lineno])
            if isinstance(node, ast.ClassDef) and node.name == "MilanSoC":
                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef):
                        out[f"MilanSoC.{sub.name}"] = "\n".join(lines[sub.lineno - 1:sub.end_lineno])
    return tree, out


def main():
    repo, rev_a, rev_b, path, *required = sys.argv[1:]
    _, a = units(source(repo, rev_a, path))
    tree_b, b = units(source(repo, rev_b, path))
    changed = sorted(n for n in set(a) | set(b) if a.get(n) != b.get(n))
    print(f"{len(set(a) | set(b))} units compared, {len(changed)} differ: {changed}")
    bad = 0
    for name in required:
        same = name in a and a.get(name) == b.get(name)
        print(f"required {name}: {'identical' if same else 'DIFFERS'}")
        bad |= not same
    cc_tree = ast.parse(source(repo, rev_b, "sw/litex/clock_constraints.py"))
    defined = {n.name for n in cc_tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    for node in ast.walk(tree_b):
        if isinstance(node, ast.ImportFrom) and node.module == "clock_constraints":
            for alias in node.names:
                ok = alias.name in defined
                print(f"clock_constraints.{alias.name} at {rev_b[:8]}: {'defined' if ok else 'MISSING'}")
                bad |= not ok
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
