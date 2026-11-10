#!/usr/bin/env python3
"""Compare the engine arm's MUTATIONS (and its imported lists) and its
verdict helpers between two extracted trees. usage: <base-tree> <head-tree>"""
import importlib.util, inspect, sys
from pathlib import Path
sys.dont_write_bytecode = True
def load(tree, tag):
    eng = Path(tree) / "tb/verilator/engine"
    sys.path[:0] = [str(eng), str(Path(tree) / "tb")]
    for k in ("mutation_verdict", "receipt_mutants", "port_mutants", "p100_mutants"):
        sys.modules.pop(k, None)
    spec = importlib.util.spec_from_file_location(f"m_{tag}", eng / "mutants.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    del sys.path[:2]
    return m
b, h = load(sys.argv[1], "base"), load(sys.argv[2], "head")
same = lambda x: "SAME" if x else "DIFFERENT"
print("MUTATIONS", len(b.MUTATIONS), len(h.MUTATIONS), same(b.MUTATIONS == h.MUTATIONS))
for n in ("RTL_SOURCES", "GENARGS", "P1_GENARGS", "P1_PLUSARG", "P1_PREFIX", "VFLAGS", "PARSER_EDITS", "GENERATOR"):
    print(n, same(getattr(b, n) == getattr(h, n)))
for f in ("edits_of", "stage", "generate_image", "build", "run_harness", "_named_failure", "verdict"):
    print(f, same(inspect.getsource(getattr(b, f)) == inspect.getsource(getattr(h, f))))
