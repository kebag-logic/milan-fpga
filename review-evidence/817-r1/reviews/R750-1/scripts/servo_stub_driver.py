"""Run sw/builder/test_clock_constraints.py::test_servo_reset_sync from a given tree.

usage: python3 -I servo_stub_driver.py <tree-root>
LiteX is not installed on the review host; clock_constraints.py imports one
LiteX class at module scope, so an import-only stand-in is placed first on
sys.path. The test under examination uses only tclsh and the tree's Tcl.
"""
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(here / "litex_stub"))
sys.path.insert(0, str(root / "sw/builder"))
import test_clock_constraints as t  # noqa: E402

assert Path(t.__file__).resolve().is_relative_to(root), t.__file__
t.test_servo_reset_sync()
print("DRIVER: test_servo_reset_sync returned")
