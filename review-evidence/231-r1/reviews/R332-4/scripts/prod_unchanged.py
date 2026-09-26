#!/usr/bin/env python3
"""Reviewer probe: compare every non-self-test top-level definition of
syn/ooc/pp_baseline.py between two commits by AST dump.
usage (from a clone): prod_unchanged.py <old-rev> <new-rev>"""
import ast, subprocess, sys
TEST = {"expect_refusal", "selftest", "export_inventory_selftest", "export_endpoint_selftest", "export_selftest"}
def defs(rev):
    text = subprocess.run(["git", "show", f"{rev}:syn/ooc/pp_baseline.py"], capture_output=True, text=True, check=True).stdout
    out = {}
    for node in ast.parse(text).body:
        name = getattr(node, "name", None) or ast.unparse(node).split("=")[0].strip()[:60]
        if name not in TEST:
            out[name] = ast.dump(node)
    return out
old, new = defs(sys.argv[1]), defs(sys.argv[2])
for name in sorted(set(old) | set(new)):
    print(f"{name}\t{'same' if old.get(name) == new.get(name) else 'DIFFERENT'}")
