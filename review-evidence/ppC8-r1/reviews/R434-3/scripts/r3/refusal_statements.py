#!/usr/bin/env python3
"""Reviewer re-derivation of the "each refusal statement replaced by pass"
claim: find, by AST, every `ctx.bad(...)` call statement in model_rules.py and
every `raise ValueError(...)` and every `.append(...)`/`ctx.bad` statement that
records a refusal, stale or problem line in model_lint.py; replace each
statement alone by `pass` in a disposable copy; run the desc_store gate.
Usage: refusal_statements.py <head-tree> <work-dir> --list | <index>"""
import ast
import pathlib
import shutil
import subprocess
import sys

head, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
D = "hdl/aecp/desc/"
TARGETS = []
for name in ("model_rules.py", "model_lint.py"):
    text = (head / D / name).read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(text)):
        hit = False
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            f = node.value.func
            if isinstance(f, ast.Attribute) and f.attr == "bad":
                hit = True
            if isinstance(f, ast.Attribute) and f.attr == "append" and isinstance(f.value, ast.Name) \
                    and f.value.id in ("refusals", "stale", "problems"):
                hit = True
        if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) \
                and getattr(node.exc.func, "id", "") == "ValueError":
            hit = True
        if hit:
            TARGETS.append((name, node.lineno, node.end_lineno, node.col_offset))
TARGETS.sort()
if sys.argv[3] == "--list":
    for i, t in enumerate(TARGETS):
        print(i, *t)
    sys.exit(0)
i = int(sys.argv[3]); name, first, last, col = TARGETS[i]
tree = work / f"s{i:03d}"
if tree.exists():
    shutil.rmtree(tree)
shutil.copytree(head / D, tree / D)
shutil.copytree(head / "tb/desc_store", tree / "tb/desc_store", ignore=shutil.ignore_patterns("obj_dir"))
f = tree / D / name
lines = f.read_text(encoding="utf-8").splitlines(keepends=True)
lines[first - 1:last] = [" " * col + "pass\n"]
f.write_text("".join(lines), encoding="utf-8")
r = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"], cwd=tree / "tb/desc_store",
                   capture_output=True, text=True, timeout=600)
fails = [l for l in r.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
print(f"{i} {name}:{first}-{last} {'KILLED' if r.returncode else 'SURVIVED'} {fails[:2]}")
