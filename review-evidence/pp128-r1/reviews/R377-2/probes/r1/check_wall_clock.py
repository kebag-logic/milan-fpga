#!/usr/bin/env python3
"""Apply the parent's uses_wall_clock() classifier (scripts/measure_test_evidence.py,
fetched read-only) to processor tb/*.py files. Usage: check_wall_clock.py PARENT_SCRIPT FILE..."""
import importlib.util, sys, types
# the classifier needs no repository scan; stub the parent helper module it imports
for _n in ("code_quality_scope", "suite_tally"):
    _m = types.ModuleType(_n); _m.tracked = lambda *a, **k: []; sys.modules.setdefault(_n, _m)
spec = importlib.util.spec_from_file_location("mte", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for p in sys.argv[2:]:
    print(f"{mod.uses_wall_clock(open(p, errors='replace').read(), '.py')} {p}")
