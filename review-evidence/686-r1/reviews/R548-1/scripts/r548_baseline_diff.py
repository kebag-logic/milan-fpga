#!/usr/bin/env python3
"""List every JSON leaf that differs between two pp_resource_baseline.json files.

usage: r548_baseline_diff.py <base.json> <head.json>
Prints changed leaf paths grouped by top-level category and fails (rc 1) if any
changed leaf lies outside record.figures, record.scopes, record.inputs_sha256
or measured, i.e. if a tolerance, floor, ceiling, identity or policy moved.
"""
import json
import sys


def leaves(node, path=()):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from leaves(value, path + (key,))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from leaves(value, path + (str(index),))
    else:
        yield path, node


base = dict(leaves(json.load(open(sys.argv[1]))))
head = dict(leaves(json.load(open(sys.argv[2]))))
changed = sorted(set(base) | set(head), key=str)
changed = [p for p in changed if base.get(p, "<absent>") != head.get(p, "<absent>")]
allowed = ("figures", "scopes", "inputs_sha256", "measured")
bad = [p for p in changed if not any(part in allowed for part in p)]
for p in changed:
    if "figures" in p or "measured" in p or "inputs_sha256" in p:
        print("/".join(p), ":", base.get(p, "<absent>"), "->", head.get(p, "<absent>"))
print(f"changed leaves: {len(changed)}; scope leaves: {sum('scopes' in p for p in changed)}")
print(f"changed outside figures/scopes/inputs/measured: {len(bad)}")
for p in bad:
    print("  OUTSIDE:", "/".join(p), base.get(p), "->", head.get(p))
sys.exit(1 if bad else 0)
