#!/usr/bin/env python3
"""Check the round 10 module moves change no behaviour: BLOCKING's bytes, and every prior MUTANTS entry's value.

usage: module_moves.py PREV_TREE HEAD_TREE
"""
import ast, sys
from pathlib import Path

prev, head = Path(sys.argv[1]), Path(sys.argv[2])

def const(path, name):
    tree = ast.parse(path.read_text())
    for node in tree.body:
        targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else []
        if any(isinstance(t, ast.Name) and t.id == name for t in targets):
            return ast.literal_eval(node.value)
    return None

old_blocking = const(prev / "scripts/test_suite_cancellation.py", "BLOCKING")
new_blocking = const(head / "scripts/process_test_support.py", "BLOCKING")
print("BLOCKING moved byte-identical:", old_blocking == new_blocking and old_blocking is not None,
      "| still defined in test file at head:", const(head / "scripts/test_suite_cancellation.py", "BLOCKING") is not None,
      "| defined in support at prev:", const(prev / "scripts/process_test_support.py", "BLOCKING") is not None)
old = const(prev / "scripts/process_test_support.py", "MUTANTS")
new = const(head / "scripts/process_test_support.py", "MUTANTS")
same = [k for k in old if new.get(k) == old[k]]
diff = [k for k in old if k in new and new[k] != old[k]]
gone = [k for k in old if k not in new]
added = [k for k in new if k not in old]
print(f"MUTANTS prev {len(old)} head {len(new)}: unchanged values {len(same)}, changed {diff}, removed {gone}")
print("added:", added)
print("order of prior keys kept:", [k for k in new if k in old] == list(old))
