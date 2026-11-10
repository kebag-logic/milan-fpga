#!/usr/bin/env python3
"""Compare the mutation arm's data (mutant list, sources, flags) between the
base commit's driver and the head driver. usage: compare_arm_constants.py <engine_dir>
(engine_dir holds mutants.py = head and mutants_base.py = base)."""
import importlib.util, sys
from pathlib import Path
eng = Path(sys.argv[1]).resolve()
def load(name):
    s = importlib.util.spec_from_file_location(name, eng / f"{name}.py")
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
head, base = load("mutants"), load("mutants_base")
bad = 0
for k in ("MUTATIONS", "RTL_SOURCES", "GENARGS", "P1_GENARGS", "P1_PLUSARG",
          "P1_PREFIX", "VFLAGS", "PARSER_EDITS", "GENERATOR"):
    same = getattr(head, k) == getattr(base, k)
    bad += not same
    n = len(getattr(head, k)) if hasattr(getattr(head, k), "__len__") else ""
    print(f"{'SAME' if same else 'DIFF'} {k} {n}")
print("verdict function identical:", head.verdict is base.verdict or
      head.verdict.__code__.co_code == base.verdict.__code__.co_code)
sys.exit(1 if bad else 0)
