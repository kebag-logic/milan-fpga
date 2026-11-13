#!/usr/bin/env python3
"""Print an engine arm's MUTATIONS list, one repr per line, in list order.

usage: dump_mutations.py <tree>/tb/verilator/engine/mutants.py
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("arm", sys.argv[1])
arm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arm)
for i, m in enumerate(arm.MUTATIONS):
    print(i, repr(m))
print("TOTAL", len(arm.MUTATIONS))
