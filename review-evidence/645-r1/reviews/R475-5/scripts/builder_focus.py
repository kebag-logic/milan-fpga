"""Run named sw/builder/test_builder.py functions alone, from the tree root.

Usage: python3 builder_focus.py <tree> <test-name> [<test-name> ...]
Prints one PASS/FAIL line per test; exit 0 only when every named test passed.
"""
import os
import sys
import traceback

tree = os.path.abspath(sys.argv[1])
os.chdir(tree)
sys.path.insert(0, os.path.join(tree, "sw", "builder"))
import test_builder  # noqa: E402

failed = 0
for name in sys.argv[2:]:
    try:
        getattr(test_builder, name)()
        print(f"PASS {name}", flush=True)
    except BaseException:  # report every failure, including SystemExit
        failed += 1
        traceback.print_exc()
        print(f"FAIL {name}", flush=True)
sys.exit(1 if failed else 0)
