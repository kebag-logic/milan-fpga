#!/usr/bin/env python3
"""Print the slot firewall text the reviewed runner's self-test pins, re-targeted.

Static only: the pinned expected string is read out of scripts/act_ci.py with
ast (the runner is never imported or executed). Only two substrings change:
the cgroup path (to a level-1 cgroup the probing process really sits under)
and the uplink set (to the probe's own uplink interface).

Usage: pinned_firewall_text.py ACT_CI_PY CGROUP_LEVEL1 UPLINK [--rule1-only]
"""
import ast
import pathlib
import sys

source = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
cgroup, uplink = sys.argv[2], sys.argv[3]
rule1_only = "--rule1-only" in sys.argv[4:]
pinned = None
for node in ast.walk(ast.parse(source)):
    if (
        isinstance(node, ast.Compare)
        and isinstance(node.left, ast.Call)
        and getattr(node.left.func, "id", "") == "slot_firewall_rules"
        and len(node.comparators) == 1
    ):
        pinned = ast.literal_eval(node.comparators[0])
if pinned is None:
    sys.exit("pinned firewall text not found")
assert pinned.count('"milan_act_slot_2.slice"') == 2, pinned
assert pinned.count('{ "eth0", "wg0" }') == 1, pinned
text = pinned.replace('"milan_act_slot_2.slice"', f'"{cgroup}"').replace(
    '{ "eth0", "wg0" }', f'{{ "{uplink}" }}'
)
if rule1_only:
    text = "".join(line + "\n" for line in text.splitlines() if "oifname" not in line)
sys.stdout.write(text)
