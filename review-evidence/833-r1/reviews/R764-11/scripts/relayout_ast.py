#!/usr/bin/env python3
"""Show the round's test-file edit is the two added listings plus behaviour-neutral re-layout.

Usage: python3 -I relayout_ast.py <old test_suite_cancellation.py> <new test_suite_cancellation.py>
Normalises the new file by inlining the `stubborn` list into its single pre-existing use and
dropping the added `for at, entry in ...` loop; strips docstrings from both; compares ast.dump.
"""
import ast
import copy
import sys


def strip_docstrings(tree: ast.AST) -> None:
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body and isinstance(body[0], ast.Expr) \
                and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            body.pop(0)


old = ast.parse(open(sys.argv[1]).read())
new = ast.parse(open(sys.argv[2]).read())
for tree in (old, new):
    strip_docstrings(tree)

stubborn_value, added_loops = None, 0
for node in ast.walk(new):
    body = getattr(node, "body", None)
    if not isinstance(body, list):
        continue
    keep = []
    for stmt in body:
        if isinstance(stmt, ast.Assign) and [getattr(t, "id", None) for t in stmt.targets] == ["stubborn"]:
            stubborn_value = stmt.value
            continue
        if isinstance(stmt, ast.For) and isinstance(stmt.target, ast.Tuple) \
                and [getattr(e, "id", None) for e in stmt.target.elts] == ["at", "entry"]:
            added_loops += 1
            continue
        keep.append(stmt)
    node.body[:] = keep
assert stubborn_value is not None and added_loops == 1, (stubborn_value, added_loops)


class Inline(ast.NodeTransformer):
    uses = 0

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if node.id == "stubborn":
            Inline.uses += 1
            return copy.deepcopy(stubborn_value)
        return node


new = Inline().visit(new)
assert Inline.uses == 1, Inline.uses
same = ast.dump(old) == ast.dump(new)
print(f"relayout-ast: stubborn inlined at {Inline.uses} use, added loops removed {added_loops}, "
      f"docstrings ignored: {'IDENTICAL' if same else 'DIFFERENT'}")
sys.exit(0 if same else 1)
