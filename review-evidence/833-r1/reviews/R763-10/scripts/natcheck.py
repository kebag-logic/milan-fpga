"""Compare round 9 natural mutants (natural.py) with MUTANTS at a tree: python3 -I natcheck.py <tree> <natural.py>"""
import ast, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
from process_test_support import MUTANTS
mod = ast.parse(open(sys.argv[2]).read())
env = {}
for node in mod.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ("TERM", "PARENT", "LIMIT", "MUTANTS"):
        exec(compile(ast.Module([node], []), "natural", "exec"), env)
for name, edits in env["MUTANTS"].items():
    repo = MUTANTS.get(name)
    if repo is None:
        print(f"{name}: NOT IN MUTANTS"); continue
    same = [tuple(e) for e in edits] == [tuple(e) for e in repo[2:]]
    print(f"{name}: {'SAME' if same else 'DIFFERENT'} control={repo[0]} words={repo[1]!r}")
