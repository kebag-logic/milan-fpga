#!/usr/bin/env python3
"""Reviewer probe: compare every argparse option of milan_soc.py, base vs head.

Usage: 37_cli_defaults.py <base-tree> <head-tree>
For each ap.add_argument call, records the option strings and every keyword
except `help` (default, type, action, choices, ...). Prints differences and,
separately, the options whose help text changed. rc 1 if any non-help keyword
differs, so a default change cannot hide inside a help edit.
"""
import ast
import sys
from pathlib import Path

REL = "sw/litex/milan_soc.py"


def options(tree_root):
    tree = ast.parse((Path(tree_root) / REL).read_text())
    out = {}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_argument"):
            names = tuple(a.value for a in node.args if isinstance(a, ast.Constant))
            kws = {k.arg: ast.unparse(k.value) for k in node.keywords if k.arg != "help"}
            helps = [ast.unparse(k.value) for k in node.keywords if k.arg == "help"]
            assert names not in out, names
            out[names] = (kws, helps[0] if helps else None)
    return out


base, head = options(sys.argv[1]), options(sys.argv[2])
print(f"options: base {len(base)}, head {len(head)}")
bad = 0
for key in sorted(set(base) | set(head)):
    if key not in base or key not in head:
        print(f"OPTION SET DIFFERS {key}: base={key in base} head={key in head}")
        bad += 1
        continue
    if base[key][0] != head[key][0]:
        print(f"NON-HELP KEYWORDS DIFFER {key}: {base[key][0]} -> {head[key][0]}")
        bad += 1
for key in sorted(set(base) & set(head)):
    if base[key][1] != head[key][1]:
        print(f"help changed only: {key} (non-help keywords identical: {base[key][0]})")
for key in (("--sys-clk-freq",), ("--milan-clk-freq",), ("--entity-gen-dir",)):
    print(f"head {key[0]}: {head[key][0]}")
print(f"non-help differences: {bad}")
sys.exit(1 if bad else 0)
