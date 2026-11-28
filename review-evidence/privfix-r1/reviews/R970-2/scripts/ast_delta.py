#!/usr/bin/env python3
"""Reviewer probe: for each touched Python file, compare the base and head ASTs.
Prints whether the trees are structurally identical once string constants are masked,
and lists every string constant whose value differs, classified as docstring or other.
usage: ast_delta.py <repo> <base-rev> <head-rev> <path>...   (run with python3 -I)"""
import ast, subprocess, sys
repo, base, head, *paths = sys.argv[1:]
def src(rev, p):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{p}"], check=True, capture_output=True).stdout.decode()
def docstring_nodes(tree):
    ids = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and n.body:
            f = n.body[0]
            if isinstance(f, ast.Expr) and isinstance(f.value, ast.Constant) and isinstance(f.value.value, str):
                ids.add(id(f.value))
    return ids
def consts(tree):
    doc = docstring_nodes(tree)
    return [(n, id(n) in doc) for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
class Mask(ast.NodeTransformer):
    def visit_Constant(self, n):
        return ast.Constant(value="S") if isinstance(n.value, str) else n
rc = 0
for p in paths:
    tb, th = ast.parse(src(base, p)), ast.parse(src(head, p))
    cb, ch = consts(tb), consts(th)
    same_shape = ast.dump(Mask().visit(ast.parse(src(base, p)))) == ast.dump(Mask().visit(ast.parse(src(head, p))))
    diffs = [(a, b, da) for (a, da), (b, db) in zip(cb, ch) if a.value != b.value]
    print(f"{p}\tstructure_identical_with_strings_masked={same_shape}\tstring_constants={len(cb)}/{len(ch)}\tdiffering={len(diffs)}")
    if not same_shape or len(cb) != len(ch): rc = 1
    for a, b, is_doc in diffs:
        la, lb = a.value.splitlines(), b.value.splitlines()
        changed = [(x, y) for x, y in zip(la, lb) if x != y]
        print(f"  line {b.lineno}\t{'DOCSTRING' if is_doc else 'NON-DOCSTRING STRING'}\tlines_in_string={len(la)}/{len(lb)}\tchanged_lines={len(changed)}")
        for x, y in changed:
            print(f"    - {x.strip()[:150]}\n    + {y.strip()[:150]}")
sys.exit(rc)
