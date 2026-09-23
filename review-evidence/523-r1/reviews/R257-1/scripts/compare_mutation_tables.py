#!/usr/bin/env python3
"""Compare the MUTATIONS / NOT_SEPARATELY_OBSERVABLE tables (AST dumps) and the
suite_failed/apply_control/TALLY_RE definitions between two mutants.py blobs.
Usage: compare_mutation_tables.py <base.py> <head.py>"""
import ast, hashlib, sys
def pick(path):
    tree = ast.parse(open(path).read()); out = {}
    for node in tree.body:
        names = [t.id for t in getattr(node, 'targets', []) if isinstance(t, ast.Name)]
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name): names = [node.target.id]
        for n in names:
            if n in ('MUTATIONS', 'NOT_SEPARATELY_OBSERVABLE', 'TALLY_RE', 'PLANE', 'RET', 'OBS', 'SHADOW', 'LAUNCH'):
                out[n] = ast.dump(node.value)
        if isinstance(node, ast.FunctionDef) and node.name in ('suite_failed', 'apply_control'):
            out['def ' + node.name] = ast.dump(node)
    return out
b, h = pick(sys.argv[1]), pick(sys.argv[2])
ok = True
for k in sorted(set(b) | set(h)):
    same = b.get(k) == h.get(k); ok &= same
    print(f"{k:34s} {'SAME' if same else 'DIFFERENT'} {hashlib.sha256((h.get(k) or '').encode()).hexdigest()[:16]}")
ns = {}
src = open(sys.argv[2]).read()
tree = ast.parse(src)
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ('MUTATIONS', 'NOT_SEPARATELY_OBSERVABLE') for t in node.targets):
        print(node.targets[0].id, 'entries:', len(node.value.elts))
print('TABLES', 'UNCHANGED' if ok else 'CHANGED'); sys.exit(0 if ok else 1)
