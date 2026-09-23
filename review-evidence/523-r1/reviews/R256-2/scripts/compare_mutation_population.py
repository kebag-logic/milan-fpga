#!/usr/bin/env python3
"""Reviewer receipt: structural comparison of the gPTP shadow mutation driver
population and verdict helpers between two commits.

Usage: compare_mutation_population.py REPO BASE HEAD
"""
import ast, hashlib, json, subprocess, sys

repo, base, head = sys.argv[1:4]
PATH = "tb/verilator/gptp_shadow/mutants.py"

def module(rev):
    return ast.parse(subprocess.check_output(["git", "-C", repo, "show", f"{rev}:{PATH}"]))

def assigned(tree, name):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.dump(node.value)
    return None

def function(tree, name):
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.dump(node)
    return None

b, h = module(base), module(head)
report = {}
for name in ("MUTATIONS", "NOT_SEPARATELY_OBSERVABLE", "TALLY_RE", "PLANE", "RET", "OBS", "TIC"):
    vb, vh = assigned(b, name), assigned(h, name)
    report[name] = dict(present=vb is not None, identical=vb == vh,
                        sha256=hashlib.sha256((vh or "").encode()).hexdigest()[:16])
for name in ("suite_failed", "apply_control"):
    report[name] = dict(identical=function(b, name) == function(h, name))
def count(tree, name):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return len(node.value.elts)
report["counts"] = dict(mutations=count(h, "MUTATIONS"), not_separately_observable=count(h, "NOT_SEPARATELY_OBSERVABLE"))
# The per-control verdict branch (named / alternate-failed-check / survivor).
def verdict_branch(tree, fname):
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == fname)
    for node in ast.walk(fn):
        if isinstance(node, ast.If) and isinstance(node.test, ast.BoolOp) and \
           {getattr(v, "id", None) for v in node.test.values} == {"caught", "named"}:
            return node
branch_b, branch_h = verdict_branch(b, "main"), verdict_branch(h, "campaign")
# Compare the named and alternate arms exactly; the survivor arm is reported.
report["named_arm_identical"] = ast.dump(ast.Module(body=branch_b.body, type_ignores=[])) == ast.dump(ast.Module(body=branch_h.body, type_ignores=[]))
alt_b, alt_h = branch_b.orelse[0], branch_h.orelse[0]
report["alternate_failed_check_arm_identical"] = ast.dump(alt_b.test) == ast.dump(alt_h.test) and \
    ast.dump(ast.Module(body=alt_b.body, type_ignores=[])) == ast.dump(ast.Module(body=alt_h.body, type_ignores=[]))
report["survivor_arm_base"] = ast.unparse(ast.Module(body=alt_b.orelse, type_ignores=[]))
report["survivor_arm_head"] = ast.unparse(ast.Module(body=alt_h.orelse, type_ignores=[]))
print(json.dumps(report, indent=2))
ok = all(v.get("identical", True) for v in report.values() if isinstance(v, dict)) and \
     report["named_arm_identical"] and report["alternate_failed_check_arm_identical"] and \
     report["counts"] == dict(mutations=9, not_separately_observable=6)
print("POPULATION " + ("UNCHANGED" if ok else "CHANGED"))
sys.exit(0 if ok else 1)
