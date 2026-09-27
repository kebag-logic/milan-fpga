#!/usr/bin/env python3
"""List self-test methods present at <base> whose source differs at <head> (or vanished).
Usage (from the review clone): tests_changed.py <base> <head>"""
import ast, subprocess, sys

def methods(rev):
    src = subprocess.run(["git", "show", f"{rev}:tb/tools/torture_campaign.py"], capture_output=True,
                         text=True, check=True).stdout
    out = {}
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                    out[f"{node.name}.{item.name}"] = ast.get_source_segment(src, item)
    return out

base, head = methods(sys.argv[1]), methods(sys.argv[2])
print(f"base tests={len(base)} head tests={len(head)}")
for name in sorted(base):
    if name not in head:
        print("REMOVED", name)
    elif base[name] != head[name]:
        print("CHANGED", name)
for name in sorted(set(head) - set(base)):
    print("ADDED", name)
