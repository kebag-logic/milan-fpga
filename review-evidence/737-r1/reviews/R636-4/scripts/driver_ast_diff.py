#!/usr/bin/env python3
"""Compare sw/builder/test_builder.py between two revisions at the AST level.

Usage: python3 -I driver_ast_diff.py <repo> <old-rev> <new-rev>

Reports every changed top-level statement other than the module docstring and
the `if __name__ == "__main__":` block, then compares the ordered run list (the
Names inside the one `for fn in ...` loop's iterable, minus helper names).
Exit 0 only when no top-level definition changed and the run lists are equal.
"""
from __future__ import annotations

import ast
import subprocess
import sys

PATH = "sw/builder/test_builder.py"
HELPERS = {"_gate_run_list", "bank"}


def load(repo: str, rev: str) -> ast.Module:
    text = subprocess.check_output(["git", "-C", repo, "show", f"{rev}:{PATH}"], text=True)
    return ast.parse(text)


def key(node: ast.stmt) -> str:
    if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
        return node.name
    if isinstance(node, ast.Assign):
        return "=" + ",".join(ast.unparse(t) for t in node.targets)
    if isinstance(node, ast.AnnAssign):
        return "=" + ast.unparse(node.target)
    return type(node).__name__ + ":" + ast.unparse(node)[:80]


def is_main(node: ast.stmt) -> bool:
    return isinstance(node, ast.If) and "__main__" in ast.unparse(node.test)


def body(tree: ast.Module) -> list[tuple[str, str]]:
    out = []
    for index, node in enumerate(tree.body):
        if index == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue  # module docstring
        if is_main(node):
            continue
        out.append((key(node), ast.dump(node)))
    return out


def run_list(tree: ast.Module) -> list[str]:
    main = [node for node in tree.body if is_main(node)][0]
    loops = [n for n in ast.walk(main) if isinstance(n, ast.For)
             and isinstance(n.target, ast.Name) and n.target.id == "fn"]
    assert len(loops) == 1, len(loops)
    return [n.id for n in ast.walk(loops[0].iter) if isinstance(n, ast.Name) and n.id not in HELPERS]


def main() -> int:
    repo, old_rev, new_rev = sys.argv[1:4]
    old, new = load(repo, old_rev), load(repo, new_rev)
    a, b = body(old), body(new)
    changed = 0
    if [k for k, _ in a] != [k for k, _ in b]:
        print("top-level statement order or membership differs")
        changed += 1
    for (ka, da), (kb, db) in zip(a, b):
        if ka == kb and da != db:
            print("changed:", ka)
            changed += 1
    gates = sum(1 for k, _ in a if k.startswith("test_"))
    print(f"top-level statements compared: {len(a)} old, {len(b)} new; test_* functions: {gates}; changed: {changed}")
    ra, rb = run_list(old), run_list(new)
    print(f"run list: {len(ra)} old, {len(rb)} new, equal={ra == rb}")
    return 0 if changed == 0 and ra == rb else 1


if __name__ == "__main__":
    raise SystemExit(main())
