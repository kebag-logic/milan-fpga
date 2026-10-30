#!/usr/bin/env python3
"""Count mutants added and edits changed between two copies of pp_resource_gate_mutants.py.
usage: mutant_delta.py <old.py> <new.py>"""
import ast, sys
def tables(path):
    tree = ast.parse(open(path).read()); out = {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(node.value, ast.Dict):
            name = (node.targets[0] if isinstance(node, ast.Assign) else node.target).id
            if name.endswith("MUTANTS"):
                out.update({f"{name}:{ast.unparse(k)}": ast.unparse(v) for k, v in zip(node.value.keys, node.value.values)})
    return out
old, new = tables(sys.argv[1]), tables(sys.argv[2])
added = sorted(set(new) - set(old)); removed = sorted(set(old) - set(new))
changed = sorted(k for k in set(old) & set(new) if old[k] != new[k])
print(f"old {len(old)}, new {len(new)}; added {len(added)}, removed {len(removed)}, edit changed {len(changed)}")
for k in added: print("  added", k)
for k in removed: print("  removed", k)
for k in changed: print("  changed", k)
