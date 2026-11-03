"""Item 1's TSC change is layout only, apart from the new listing and the named stubborn-parent events.

usage: python3 -I layout_check.py REPO BASE [NEW]   (BASE's scripts/test_suite_cancellation.py against NEW's, or the worktree's)
Every kept(...) call at BASE is found at the worktree with an identical AST, except "a stubborn parent", whose
stated list is now the name `stubborn`, assigned the identical literal. Every other top-level statement of the
module and every other statement in owner_stated_seconds and stated_liveness is AST-identical. Prints what is new.
"""
import ast, subprocess, sys
from pathlib import Path
repo, base, *rest = sys.argv[1:]
path = "scripts/test_suite_cancellation.py"
old_src = subprocess.run(["git", "-C", repo, "show", f"{base}:{path}"], capture_output=True, text=True, check=True).stdout
new_src = (subprocess.run(["git", "-C", repo, "show", f"{rest[0]}:{path}"], capture_output=True, text=True,
                          check=True).stdout if rest else (Path(repo) / path).read_text())
old, new = ast.parse(old_src), ast.parse(new_src)
def stmts(tree):
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.stmt):
            out.append(node)
    return out
def kept_calls(tree):
    return {ast.unparse(n.value.args[0]): n.value for n in stmts(tree)
            if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and getattr(n.value.func, "id", "") == "kept"}
ok = True
ko, kn = kept_calls(old), kept_calls(new)
stub = next(n for n in stmts(new) if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "stubborn")
for words, call in ko.items():
    other = kn.get(words)
    if other is None:
        print("MISSING", words); ok = False; continue
    if ast.dump(call) == ast.dump(other):
        continue
    if words == "'a stubborn parent'":
        same = (ast.dump(call.args[0]) == ast.dump(other.args[0]) and ast.dump(call.args[1]) == ast.dump(other.args[1])
                and getattr(other.args[2], "id", "") == "stubborn" and ast.dump(call.args[2]) == ast.dump(stub.value)
                and len(call.args) == len(other.args) == 3 and not call.keywords and not other.keywords)
        print("a stubborn parent: stated list moved into `stubborn`, identical literal:", same); ok &= same
        continue
    print("CHANGED", words); ok = False
print("new kept calls:", [w for w in kn if w not in ko])
# Everything else: the module with the new loop and the stubborn assignment removed, and the stubborn name inlined,
# must dump identically to the base.
class Undo(ast.NodeTransformer):
    def visit_For(self, node):
        self.generic_visit(node)
        if "stubborn parent {at}" in ast.unparse(node):
            return None
        return node
    def visit_Assign(self, node):
        return None if getattr(node.targets[0], "id", "") == "stubborn" else node
    def visit_Name(self, node):
        return stub.value if node.id == "stubborn" else node
undone = Undo().visit(ast.parse(new_src))
same_rest = ast.dump(undone) == ast.dump(old)
print("rest of the module AST-identical to the base:", same_rest); ok &= same_rest
print("layout check:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
