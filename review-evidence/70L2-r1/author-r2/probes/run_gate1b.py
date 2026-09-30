#!/usr/bin/env python3
"""Run ONLY builder gate 1b (test_baremetal_profile_contract) from a tree copy.

usage: run_gate1b.py <tree>
Runs with --require-rv32 from the tree's own sw/builder/test_builder.py (the
tree's firmware may carry a plant). Prints GATE1B ACCEPTED or the refusal text;
exit 0 on acceptance, 1 on refusal. Combine with instrument_gate1b.py's
A455_STOP to stop early.
"""
import os
import sys
import time
import traceback

tree = os.path.abspath(sys.argv[1])
os.chdir(tree)
sys.argv = [os.path.join(tree, "sw/builder/test_builder.py"), "--require-rv32"]
sys.path.insert(0, os.path.join(tree, "sw/builder"))
import test_builder as tb  # noqa: E402

start = time.time()
try:
    tb.test_baremetal_profile_contract()
except AssertionError as exc:
    print("GATE1B REFUSED:", str(exc)[:4000])
    traceback.print_exc(limit=2)
    print(f"elapsed {time.time() - start:.1f}s")
    sys.exit(1)
print("GATE1B ACCEPTED")
print(f"elapsed {time.time() - start:.1f}s")
