#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R228-4: prove the 97aa1ec9..4876423d delta changes no production code.

Usage: r228_4_ast_scope.py <clone> <prev> <head>

Parses sw/builder/test_builder.py at both commits and compares the AST
dump (no line numbers) of every top-level statement. Only
test_baremetal_profile_contract may differ; inside it, the differing
top-level statements of its body are listed by the names they assign.
"""

import ast
import subprocess
import sys

clone, prev, head = sys.argv[1:4]
PATH = "sw/builder/test_builder.py"


def load(rev):
    src = subprocess.run(["git", "-C", clone, "show", f"{rev}:{PATH}"],
                         check=True, capture_output=True, text=True).stdout
    return ast.parse(src)


def key(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
        return node.name
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        return "=" + ",".join(ast.unparse(t) for t in targets)
    return ast.unparse(node)[:60]


def table(tree):
    out = {}
    for node in tree.body:
        k = key(node)
        while k in out:
            k += "'"
        out[k] = ast.dump(node, include_attributes=False)
    return out


a, b = table(load(prev)), table(load(head))
changed = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
print(f"top-level statements: prev {len(a)} head {len(b)}; changed: {changed}")
ok = changed == ["test_baremetal_profile_contract"]
fa = next(n for n in load(prev).body if getattr(n, "name", "") == changed[0])
fb = next(n for n in load(head).body if getattr(n, "name", "") == changed[0])
ia = [ast.dump(n, include_attributes=False) for n in fa.body]
ib = [ast.dump(n, include_attributes=False) for n in fb.body]
print(f"{changed[0]}: body statements prev {len(ia)} head {len(ib)}")
diff = [(i, key(fb.body[i])) for i in range(max(len(ia), len(ib)))
        if i >= len(ia) or i >= len(ib) or ia[i] != ib[i]]
print(f"differing body statements (index, target): {diff}")
ok = ok and len(ia) == len(ib) and [d[1] for d in diff] == \
    ["=stale_probes", "=kept_probes", "=store_classes_note"]
print("AST SCOPE " + ("PASS: only stale_probes, kept_probes and the printed note changed"
                      if ok else "FAIL"))
sys.exit(0 if ok else 1)
