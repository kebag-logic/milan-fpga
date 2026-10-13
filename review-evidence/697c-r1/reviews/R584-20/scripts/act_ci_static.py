#!/usr/bin/env python3
"""act_ci_static.py <tree>: a static (non-executing) check of the composed scripts/act_ci.py.
It parses the file with ast and never imports or runs it (the runner's self-test is not run on a
host). Checks: the PR's stack-manifest self-test is defined once and called from the
submodule-manifest self-test, every name it uses is defined, no self-test is defined twice,
and TRUSTED_SUBMODULES lists the six approved entries."""
import ast, builtins, pathlib, sys

src = (pathlib.Path(sys.argv[1]) / "scripts/act_ci.py").read_text()
tree = ast.parse(src)
top = {}
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        top.setdefault(node.name, []).append(node.lineno)
    elif isinstance(node, (ast.Assign, ast.AnnAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        for t in targets:
            if isinstance(t, ast.Name):
                top.setdefault(t.id, []).append(node.lineno)
for name in ("selftest_stack_manifest", "selftest_lwsrp_manifest", "selftest_submodule_manifest",
             "validate_submodule_manifest", "GitFixture", "SelftestTally", "TRUSTED_SUBMODULES",
             "REQUIRED_SUBMODULES", "job_container_width", "replay_container_concurrency"):
    print(f"{name}: defined at {top.get(name)}")
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "selftest_submodule_manifest")
calls = [c.func.id for c in ast.walk(fn) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)]
print("selftest_submodule_manifest calls selftest_stack_manifest:", "selftest_stack_manifest" in calls)
stack = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "selftest_stack_manifest")
local = {a.arg for a in stack.args.args} | {n.id for n in ast.walk(stack) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
local |= {a.arg for n in ast.walk(stack) if isinstance(n, ast.Lambda) for a in n.args.args}
used = {n.id for n in ast.walk(stack) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
missing = sorted(u for u in used if u not in local and u not in top and not hasattr(builtins, u))
print("names selftest_stack_manifest uses that nothing defines:", missing)
ts = next(n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "TRUSTED_SUBMODULES" for t in n.targets))
print("TRUSTED_SUBMODULES entries:", [e.elts[1].value for e in ts.value.elts])
dups = sorted(k for k, v in top.items() if k.startswith("selftest_") and len(v) > 1)
print("self-tests defined more than once:", dups)
ok = not missing and len(ts.value.elts) == 6 and "selftest_stack_manifest" in calls and not dups
print("static check:", "OK" if ok else "FAILED")
sys.exit(0 if ok else 1)
