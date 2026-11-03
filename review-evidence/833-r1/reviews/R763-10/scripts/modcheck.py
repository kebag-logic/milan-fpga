"""Module moves of round 10: BLOCKING and every prior MUTANTS entry unchanged in value.

Usage: python3 -I modcheck.py <prev-tree> <head-tree>
"""
import ast, sys
def load(tree, path, names):
    mod = ast.parse(open(f"{tree}/{path}").read())
    out = {}
    for node in mod.body:
        target = node.target if isinstance(node, ast.AnnAssign) else node.targets[0] if isinstance(node, ast.Assign) else None
        if isinstance(target, ast.Name) and target.id in names:
            out[target.id] = ast.literal_eval(node.value)
    return out
prev = load(sys.argv[1], "scripts/process_test_support.py", {"MUTANTS"}) | load(sys.argv[1], "scripts/test_suite_cancellation.py", {"BLOCKING"})
head = load(sys.argv[2], "scripts/process_test_support.py", {"MUTANTS", "BLOCKING"})
tsc = load(sys.argv[2], "scripts/test_suite_cancellation.py", {"BLOCKING"})
print("BLOCKING moved byte-identical:", prev["BLOCKING"] == head["BLOCKING"], "| still defined in test_suite_cancellation:", bool(tsc))
pm, hm = prev["MUTANTS"], head["MUTANTS"]
print("prior entries:", len(pm), "head entries:", len(hm))
print("prior entries changed in value:", [k for k in pm if pm[k] != hm.get(k)])
print("prior keys order kept:", list(hm)[:len(pm)] == list(pm))
print("new entries:", [k for k in hm if k not in pm])
