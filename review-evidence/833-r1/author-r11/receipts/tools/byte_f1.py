"""The F1 mutant's edit in MUTANTS is R763-10's natural10.py edit, byte for byte.

usage: python3 -I byte_f1.py <tree> <natural10.py>
"""
import ast, sys
from pathlib import Path
tree, nat = Path(sys.argv[1]), Path(sys.argv[2])
src = nat.read_text(); mod = ast.parse(src)
env = {}
for node in mod.body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") in ("PARENT", "MUTANTS"):
        exec(compile(ast.Module([node], []), "natural10", "exec"), env)
theirs = env["MUTANTS"]["first-census-parent-unspared-beside-shell"]
sup = (tree / "scripts/process_test_support.py").read_text()
d = next(n for n in ast.parse(sup).body if isinstance(n, ast.AnnAssign) and n.target.id == "MUTANTS").value
mine = ast.literal_eval(ast.unparse(d))["first-census-parent-unspared-beside-shell"]
print("control:", mine[0], "| words:", repr(mine[1]))
same = list(mine[2:]) == [tuple(edit) for edit in theirs]
print("edit byte for byte as natural10.py:", "SAME" if same else "DIFFERENT")
sys.exit(0 if same else 1)
