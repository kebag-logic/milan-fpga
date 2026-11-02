#!/usr/bin/env python3
"""Build mutant trees with the tree's own mutant_tree(), for whole-test runs.

Usage: python3 -I make_trees.py <tree with MUTANTS> <output dir> NAME...
"""
import sys
from pathlib import Path

tree, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(tree / "scripts"))
import process_test_support as support  # noqa: E402

for name in sys.argv[3:]:
    print(support.mutant_tree(out, name))
