"""Prove the diff stays inside the settled closing-condition scope."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
base = "b17580b91deb11f3441dfc5d7f9fafe539d929b8"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
paths = subprocess.check_output(["git", "diff", "--name-only", base, head], text=True).splitlines()
expected = ["docs/DOC_GENERATION.md", "scripts/check_em_dash.py", "scripts/gen_toc.py",
            "scripts/gen_toc_cases.py", "scripts/gen_toc_closer_cases.py", "scripts/gen_toc_guards.py"]
assert paths == expected, paths

def nodes(source):
    result = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef):
            node = copy.deepcopy(node)
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                node.body.pop(0)
            result[node.name] = ast.dump(node)
    return result

changed = {}
for script, permitted in [("gen_toc.py", {"_type_1_end", "_still_open", "_opens", "selftest"}),
                           ("check_em_dash.py", {"selftest"}), ("gen_toc_guards.py", set())]:
    before = subprocess.check_output(["git", "show", base+":scripts/"+script], text=True)
    after = (Path("scripts")/script).read_text()
    old, new = nodes(before), nodes(after)
    differences = {name for name in old.keys() | new.keys() if old.get(name) != new.get(name)}
    assert differences == permitted, (script,differences)
    changed[script] = sorted(differences)
    if script == "gen_toc.py":
        assignments = lambda source: [ast.dump(n) for n in ast.parse(source).body
            if isinstance(n, ast.Assign) and all(not isinstance(t,ast.Name) or t.id not in
                                                {"ARM_FAMILIES","MIN_ARMS"} for t in n.targets)]
        assert assignments(before) == assignments(after)
oldcases = subprocess.check_output(["git", "show", base+":scripts/gen_toc_cases.py"],text=True)
newcases = Path("scripts/gen_toc_cases.py").read_text()
assert nodes(oldcases)["_round10_walk_arms"] == nodes(newcases)["_round10_walk_arms"]
report = dict(base=base, head=head, paths=paths, changed_function_bodies=changed,
              class_refusal_fold_and_all_non_tally_constants="identical",
              existing_unicode_fold_controls="identical",
              changed_budgets=[], changed_gitlinks=[])
(root/"scope-guard.json").write_text(json.dumps(report,indent=2)+"\n")
perpages = {}
for label in ("pages-base-base","pages-head-base","pages-base-head","pages-head-head"):
    rows = json.loads((root/(label+".json")).read_text())
    perpages[label] = {path:hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()
                       for path,row in rows.items()}
(root/"perpage-record-hashes.json").write_text(json.dumps(perpages,indent=2)+"\n")
print(json.dumps(report,indent=2))
