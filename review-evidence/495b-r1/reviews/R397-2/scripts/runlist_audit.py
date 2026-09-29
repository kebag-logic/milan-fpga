#!/usr/bin/env python3
"""Audit test_builder.py's __main__ run list at a tree: duplicates, undefined names,
duplicate top-level defs, and which names each side (predecessor/PR) added.
Usage: runlist_audit.py <path-to-test_builder.py> [<label>]"""
import ast, sys, collections
src = open(sys.argv[1]).read()
tree = ast.parse(src)
defs = collections.Counter(n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
dupdefs = {k: v for k, v in defs.items() if v > 1}
loops = [n for n in ast.walk(tree) if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == "fn"]
assert len(loops) == 1, len(loops)
runs = [e.id for e in loops[0].iter.elts] if isinstance(loops[0].iter, ast.Tuple) else None
imported = set()
main = [n for n in tree.body if isinstance(n, ast.If)][-1]
for n in ast.walk(main):
    if isinstance(n, ast.ImportFrom):
        for a in n.names: imported.add(a.asname or a.name)
c = collections.Counter(runs)
print(f"[{sys.argv[2] if len(sys.argv)>2 else ''}] run-list entries: {len(runs)} unique: {len(c)}")
print("duplicate run-list entries:", {k: v for k, v in c.items() if v > 1} or "none")
print("duplicate top-level defs:", dupdefs or "none")
undefined = [r for r in runs if r not in defs and r not in imported]
print("run-list names neither defined nor imported in __main__:", undefined or "none")
unrun = sorted(k for k in defs if k.startswith("test_") and k not in c)
print("top-level test_* defs not in run list:", len(unrun))
for u in unrun: print("   ", u)
open(sys.argv[1] + ".runlist" if False else "/dev/null", "w")
print("RUNLIST", " ".join(runs))
