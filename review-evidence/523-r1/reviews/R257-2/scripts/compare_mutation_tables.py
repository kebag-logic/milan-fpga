#!/usr/bin/env python3
"""Compare the mutation population and verdict helpers of mutants.py at two
revisions by AST (docstrings/comments ignored). Usage: CLONE BASE HEAD"""
import ast, json, os, subprocess, sys
clone, base, head = sys.argv[1:4]
NAMES = ("MUTATIONS", "NOT_SEPARATELY_OBSERVABLE", "TALLY_RE", "PLANE", "RET", "OBS", "TIC")
FUNCS = ("suite_failed", "apply_control")
def source(rev):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", clone, "show", f"{rev}:tb/verilator/gptp_shadow/mutants.py"],
                          env=env, capture_output=True, text=True, check=True).stdout
def pick(text):
    tree = ast.parse(text)
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in NAMES:
            out[node.targets[0].id] = ast.dump(node.value)
        if isinstance(node, ast.FunctionDef) and node.name in FUNCS:
            body = node.body[1:] if (node.body and isinstance(node.body[0], ast.Expr)
                                     and isinstance(getattr(node.body[0], "value", None), ast.Constant)) else node.body
            out[node.name] = ast.dump(ast.Module(body=body, type_ignores=[]))
    return out
b, h = pick(source(base)), pick(source(head))
ns = {}
exec(compile(ast.Module(body=[n for n in ast.parse(source(head)).body if isinstance(n, ast.Assign)
     and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("MUTATIONS", "NOT_SEPARATELY_OBSERVABLE")],
     type_ignores=[]), "m", "exec"), {"RET": "RET", "OBS": "OBS", "TIC": "TIC"}, ns)
print(json.dumps({"compared": sorted(b), "identical": {k: b.get(k) == h.get(k) for k in sorted(set(b) | set(h))},
                  "head_mutations": len(ns["MUTATIONS"]), "head_unobservable": len(ns["NOT_SEPARATELY_OBSERVABLE"])},
                 indent=1))
