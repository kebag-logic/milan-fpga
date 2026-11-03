#!/usr/bin/env python3
"""Show the round's test_suite_cancellation.py edit is the stubborn name, the docstring and two added listings only.

Usage: python3 -I ast_relayout.py <old file> <new file>
The new file's `stubborn` assignment is inlined at its use in "a stubborn parent", the two added listings
(the for loop over beside/under) are removed, and kept's docstring is set to the old one; then the module ASTs
must be equal.
"""
import ast, copy, sys

old = ast.parse(open(sys.argv[1]).read())
new = ast.parse(open(sys.argv[2]).read())

def fn(tree, name):
    return next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)

with_new = next(n for n in fn(new, "owner_stated_seconds").body if isinstance(n, ast.With))
assign = [s for s in with_new.body if isinstance(s, ast.Assign) and getattr(s.targets[0], "id", "") == "stubborn"]
loops = [s for s in with_new.body if isinstance(s, ast.For) and "stubborn" in ast.unparse(s)]
assert len(assign) == 1 and len(loops) == 1, (assign, loops)
value = assign[0].value
with_new.body = [s for s in with_new.body if s is not assign[0] and s is not loops[0]]

class Inline(ast.NodeTransformer):
    def visit_Name(self, node):
        return copy.deepcopy(value) if node.id == "stubborn" else node
Inline().visit(with_new)
fn(fn(new, "owner_stated_seconds"), "kept").body[0] = fn(fn(old, "owner_stated_seconds"), "kept").body[0]
print("loops removed:", ast.unparse(loops[0]).replace("\n", " | "))
same = ast.dump(old) == ast.dump(new)
print("module AST equal after the stated edits:", same)
sys.exit(0 if same else 1)
