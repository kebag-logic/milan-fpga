"""Evaluate the three round 8 edits built from module constants and compare with MUTANTS at the head."""
import ast, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
from process_test_support import MUTANTS
def consts(path):
    tree = ast.parse(open(path).read()); env = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                env[node.targets[0].id] = eval(compile(ast.Expression(node.value), path, "eval"), {}, dict(env))
            except Exception:
                pass
    return env
r8 = consts(sys.argv[2]); live = consts(sys.argv[3])
m8 = r8["MINE"]; ml = live[[k for k in live if isinstance(live[k], dict) and "sigterm-to-live-new" in live[k]][0]]
for theirs, mine in ((m8["r8-resume-beside-new-live"], "resume-beside-new-live"),
                     (m8["r8-sigterm-trap-command-after-late-grace-resume"], "sigterm-trap-command-after-resume-from-1.5s"),
                     (ml["sigterm-to-live-new"][0], "sigterm-to-live-new")):
    print(mine, "SAME" if tuple(theirs) == tuple(MUTANTS[mine][2]) and len(MUTANTS[mine]) == 3 else f"DIFF {theirs!r} vs {MUTANTS[mine][2:]!r}")
