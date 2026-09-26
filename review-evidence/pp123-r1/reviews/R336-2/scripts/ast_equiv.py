#!/usr/bin/env python3
"""Prove the round-2 delta is behaviour-free at the syntax-tree level.

Usage: ast_equiv.py <round1-tree> <head-tree>

gen_desc_image.py: the two module ASTs must be equal once the module docstring
is set aside (the only round-2 edit there is one sketch line in it).
test_gen_desc_image.py: the two ASTs must be equal once, on both sides,
function annotations and function docstrings are removed, the `typing` import is
removed, and the `timeout` keyword is removed from calls. What that leaves out is
printed, so the residual difference is exactly F1 (annotations, docstrings) and
F2 (the deadline). Exit 0 only if both comparisons are equal.
"""
import ast
import sys
from pathlib import Path


def drop_docstring(body: list) -> list:
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        return body[1:]
    return body


class Strip(ast.NodeTransformer):
    def __init__(self) -> None:
        self.removed: list[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        self.generic_visit(node)
        if node.returns is not None:
            self.removed.append(f"{node.name}: return annotation")
            node.returns = None
        for arg in node.args.args + node.args.kwonlyargs:
            if arg.annotation is not None:
                self.removed.append(f"{node.name}: annotation on {arg.arg}")
                arg.annotation = None
        new = drop_docstring(node.body)
        if new is not node.body:
            self.removed.append(f"{node.name}: docstring")
            node.body = new
        return node

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.AST | None:
        if node.module == "typing":
            self.removed.append("from typing import ...")
            return None
        return node

    def visit_Call(self, node: ast.Call) -> ast.AST:
        self.generic_visit(node)
        kept = [k for k in node.keywords if k.arg != "timeout"]
        if len(kept) != len(node.keywords):
            self.removed.append(f"line {node.lineno}: timeout= keyword")
            node.keywords = kept
        return node


def module(path: Path) -> ast.Module:
    return ast.parse(path.read_text(), str(path))


R1, HEAD = (Path(a).resolve() for a in sys.argv[1:3])
ok = True

gen = "hdl/aecp/desc/gen_desc_image.py"
a, b = module(R1 / gen), module(HEAD / gen)
same_doc = ast.get_docstring(a) == ast.get_docstring(b)
a.body, b.body = drop_docstring(a.body), drop_docstring(b.body)
eq = ast.dump(a) == ast.dump(b)
ok &= eq
print(f"{gen}: module docstring {'same' if same_doc else 'differs'}; "
      f"code AST without docstring {'EQUAL' if eq else 'DIFFERENT'}")

test = "tb/desc_store/test_gen_desc_image.py"
sa, sb = Strip(), Strip()
a, b = sa.visit(module(R1 / test)), sb.visit(module(HEAD / test))
eq = ast.dump(a) == ast.dump(b)
ok &= eq
print(f"{test}: normalised AST {'EQUAL' if eq else 'DIFFERENT'}")
print(f"  removed from round 1 ({len(sa.removed)}): {sa.removed}")
print(f"  removed from head ({len(sb.removed)}):")
for item in sb.removed:
    print(f"    {item}")
sys.exit(0 if ok else 1)
