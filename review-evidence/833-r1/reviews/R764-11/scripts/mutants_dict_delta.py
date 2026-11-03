#!/usr/bin/env python3
"""Compare MUTANTS between two copies of process_test_support.py; check the rest of the module is AST-identical.

Usage: python3 -I mutants_dict_delta.py <old process_test_support.py> <new process_test_support.py>
"""
import ast
import sys


def mutants(path):
    tree = ast.parse(open(path).read())
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", None) == "MUTANTS":
            return ast.literal_eval(node.value), tree, node


old, old_tree, old_node = mutants(sys.argv[1])
new, new_tree, new_node = mutants(sys.argv[2])
print("added", sorted(set(new) - set(old)), "removed", sorted(set(old) - set(new)),
      "changed", sorted(k for k in old if k in new and old[k] != new[k]))
print("order of old entries kept:", [k for k in new if k in old] == list(old))
new_node.value = old_node.value
print("rest of process_test_support identical:", ast.dump(old_tree) == ast.dump(new_tree))
