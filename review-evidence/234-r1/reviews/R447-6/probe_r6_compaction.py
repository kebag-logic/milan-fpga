#!/usr/bin/env python3
"""Is the compaction commit c7cde331 behaviour-preserving against round 5's ec7eb2d8? Compares the self-test's
docstring word sequence and each top-level function's AST and each top-level constant's evaluated repr.
Usage: probe_r6_compaction.py <repo checkout> [<ec7eb2d8 export> <c7cde331 export>]  (reads git objects and the exports only)
"""
import ast, subprocess, sys
repo = sys.argv[1]
def src(rev):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:syn/ooc/pp_resource_gate_selftest.py"],
                          capture_output=True, text=True, check=True).stdout
a, b = ast.parse(src("ec7eb2d8")), ast.parse(src("c7cde331"))
print("docstring words equal:", " ".join(ast.get_docstring(a).split()) == " ".join(ast.get_docstring(b).split()))
fa = {n.name: ast.dump(n) for n in a.body if isinstance(n, ast.FunctionDef)}
fb = {n.name: ast.dump(n) for n in b.body if isinstance(n, ast.FunctionDef)}
print("functions:", len(fa), "->", len(fb), "; AST differs:", sorted(k for k in fa if fa[k] != fb.get(k)),
      "; added:", sorted(set(fb) - set(fa)))
def consts(tree):
    out = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and all(isinstance(t, ast.Name) for t in n.targets):
            out[n.targets[0].id] = n
    return out
ca, cb = consts(a), consts(b)
print("top-level assignments:", len(ca), "->", len(cb), "; added:", sorted(set(cb) - set(ca)),
      "; removed:", sorted(set(ca) - set(cb)))
print("assignments whose source AST differs:", sorted(k for k in ca if k in cb and ast.dump(ca[k]) != ast.dump(cb[k])))
# Evaluated equality of the arm tables whose source changed: import each commit's self-test from a git-archive export.
if len(sys.argv) > 2:
    import importlib.util, os
    def load(root, tag):
        sys.path.insert(0, f"{root}/syn/ooc")
        spec = importlib.util.spec_from_file_location(f"st_{tag}", f"{root}/syn/ooc/pp_resource_gate_selftest.py")
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        sys.path.pop(0)
        return mod
    ma, mb = load(sys.argv[2], "a"), load(sys.argv[3], "b")
    for name in ("ROUTE_ARMS", "OOC_ARMS"):
        print(f"{name} evaluated equal:", repr(getattr(ma, name)) == repr(getattr(mb, name)), len(getattr(mb, name)))
