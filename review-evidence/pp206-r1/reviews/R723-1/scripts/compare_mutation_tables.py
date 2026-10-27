#!/usr/bin/env python3
"""Reviewer check: the mutation tables of two gsi_mutants.py copies are equal.

Usage: compare_mutation_tables.py <tb/common dir> <old.py> <new.py>
"""
import importlib.util
import sys

sys.path.insert(0, sys.argv[1])


def table(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.mutations()


old, new = table(sys.argv[2], "old"), table(sys.argv[3], "new")
print(f"old {len(old)} arms, new {len(new)} arms, identical and ordered: {old == new}")
sys.exit(0 if old == new else 1)
