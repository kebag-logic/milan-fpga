#!/usr/bin/env python3
"""Run ONLY builder gate 1b (test_baremetal_profile_contract) on a tree copy.

usage: run_gate1b.py <tree>   (the tree is a disposable copy of the head)
Prints PASS or the AssertionError text; exit 0 on PASS, 1 on refusal.
"""
import os
import sys
import traceback

tree = os.path.abspath(sys.argv[1])
os.chdir(tree)
sys.argv = [os.path.join(tree, "sw/builder/test_builder.py"), "--require-rv32"]
sys.path.insert(0, os.path.join(tree, "sw/builder"))
import test_builder as tb  # noqa: E402

try:
    tb.test_baremetal_profile_contract()
except AssertionError as exc:
    print("GATE1B REFUSED:", str(exc)[:4000])
    traceback.print_exc(limit=3)
    sys.exit(1)
print("GATE1B PASS")
