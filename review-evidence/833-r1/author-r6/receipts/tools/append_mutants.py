#!/usr/bin/env python3
"""Append candidate mutants to MUTANTS in a disposable tree, keeping their named controls.

usage: python3 -I -B append_mutants.py <tree> <candidates.py>   (never the lane)
"""
import runpy
import sys
from pathlib import Path

tree = Path(sys.argv[1])
assert "$VALIDATION_STORAGE/" in str(tree.resolve()), tree
new = runpy.run_path(sys.argv[2])["NEW"]
support = tree / "scripts/process_test_support.py"
text = support.read_text()
anchor = "\n}\n\n\ndef mutant_tree("
assert text.count(anchor) == 1
entries = "".join(f"    {name!r}: {entry!r},\n" for name, entry in new.items())
support.write_text(text.replace(anchor, "\n" + entries + "}\n\n\ndef mutant_tree(", 1))
print("\n".join(new))
