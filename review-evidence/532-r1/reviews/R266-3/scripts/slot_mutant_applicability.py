#!/usr/bin/env python3
"""Static check: how many times each published slot mutant's `before` text occurs in a runner file.

Usage: slot_mutant_applicability.py RUNNER A213_SLOT_MUTANTS_PY A220_SLOT_MUTANTS_PY
Reads the MUTANTS / A220_MUTANTS lists with ast.literal_eval; executes neither
the mutant scripts nor the runner.
"""
import ast
import pathlib
import sys


def literal_list(path: str, name: str) -> list:
    tree = ast.parse(pathlib.Path(path).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise SystemExit(f"{name} not found in {path}")


runner = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
mutants = literal_list(sys.argv[2], "MUTANTS") + literal_list(sys.argv[3], "A220_MUTANTS")
bad = 0
for label, before, after in mutants:
    count = runner.count(before)
    changes = runner.replace(before, after, 1) != runner
    ok = count == 1 and changes
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'} occurs={count} changes={changes} {label}")
print(f"total={len(mutants)} applying-exactly-once={len(mutants) - bad}")
