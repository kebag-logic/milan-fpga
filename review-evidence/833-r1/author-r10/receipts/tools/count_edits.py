#!/usr/bin/env python3
"""Count how often each candidate mutant's old text occurs in a product file.

usage: python3 -I -B count_edits.py <owned_process.py> <candidates.py>
candidates.py defines NEW = {name: (control, words, (old, new), ...)}.
"""
import runpy
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text()
candidates = runpy.run_path(sys.argv[2])["NEW"]
bad = 0
for name, (_control, _words, *edits) in candidates.items():
    mutated = text
    for old, new in edits:
        count = mutated.count(old)
        print(f"{name}: {count} x {old[:70]!r}")
        bad |= count != 1
        mutated = mutated.replace(old, new)
    try:
        compile(mutated, name, "exec")
    except SyntaxError as exc:
        print(f"{name}: SYNTAX {exc}")
        bad = 1
sys.exit(bad)
