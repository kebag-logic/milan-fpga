#!/usr/bin/env python3
"""Run named test_builder gate functions from one exported tree.
Usage: run_focused.py <tree> <function> [<function> ...]
Prints each gate's own output, then the skipped arms; exit 0 only when every
named function returned without raising."""
import sys
import traceback
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw" / "builder"))
sys.argv = [sys.argv[0]] + sys.argv[2:]
import test_builder as tb  # noqa: E402

rc = 0
for name in sys.argv[1:]:
    print(f"{name}:", flush=True)
    try:
        getattr(tb, name)()
        print(f"RESULT {name} PASS", flush=True)
    except BaseException:  # report every failure, keep going
        traceback.print_exc()
        print(f"RESULT {name} FAIL", flush=True)
        rc = 1
for gate, why, _kind in tb.SKIPPED:
    print(f"SKIPPED [{gate}] {why}")
sys.exit(rc)
