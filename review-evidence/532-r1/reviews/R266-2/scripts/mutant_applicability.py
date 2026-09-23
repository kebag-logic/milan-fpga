#!/usr/bin/env python3
"""Static check (no execution of the runner): every published mutant's 'before'
fragment occurs exactly once in the reviewed file. Reads the MUTANTS list with
ast.literal_eval so the published harness is never imported or run.

Usage: mutant_applicability.py HARNESS.py TARGET_FILE
"""
import ast
import hashlib
import pathlib
import sys

harness, target = map(pathlib.Path, sys.argv[1:3])
tree = ast.parse(harness.read_text(encoding="utf-8"))
mutants = None
for node in tree.body:
    if isinstance(node, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == "MUTANTS" for t in node.targets
    ):
        mutants = ast.literal_eval(node.value)
if mutants is None:
    sys.exit("no MUTANTS list")
text = target.read_text(encoding="utf-8")
print(f"target {target.name} sha256={hashlib.sha256(target.read_bytes()).hexdigest()}")
bad = 0
for entry in mutants:
    name, before = entry[0], entry[1]
    count = text.count(before)
    ok = count == 1
    bad += 0 if ok else 1
    print(f"{'ok  ' if ok else 'BAD '} occurrences={count} {name}")
print(f"mutants={len(mutants)} not-exactly-once={bad}")
sys.exit(1 if bad else 0)
