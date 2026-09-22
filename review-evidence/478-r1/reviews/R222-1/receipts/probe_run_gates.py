#!/usr/bin/env python3
"""[R222] Run selected test_builder gate functions from a scratch checkout.

Usage: probe_run_gates.py <scratch-root> <fn> [<fn> ...]
Imports <root>/sw/builder/test_builder.py as a module (its __main__ block does
not run), calls each named function in order and reports PASS or the first
exception per function. Exit status is the number of failing functions.
"""
import importlib.util
import sys
import traceback
from pathlib import Path

root = Path(sys.argv[1]).resolve()
names = sys.argv[2:]
spec = importlib.util.spec_from_file_location(
    "test_builder", root / "sw/builder/test_builder.py")
tb = importlib.util.module_from_spec(spec)
sys.modules["test_builder"] = tb
spec.loader.exec_module(tb)
assert Path(tb.eb.__file__).resolve() == root / "sw/builder/endstation_builder.py", tb.eb.__file__
print(f"root={root} builder={tb.eb.__file__}")
failed = 0
for name in names:
    fn = getattr(tb, name)
    print(f"--- {name}")
    try:
        fn()
    except BaseException as exc:  # report and continue: each gate stands alone
        failed += 1
        print(f"RESULT {name}: FAIL {type(exc).__name__}: {exc}")
        traceback.print_exc(limit=3, file=sys.stdout)
    else:
        print(f"RESULT {name}: PASS")
print(f"SKIPPED={tb.SKIPPED}")
sys.exit(failed)
