#!/usr/bin/env python3
"""Run the builder's gate 20a (test_csr_defaults_header_consumed) alone.

It is the one builder gate whose inputs include a file the predecessor lane
changed (syn/yosys/run.sh, the INCDIRS row). Run from a disposable copy of the
candidate with the three required submodules initialised; with argument
`drop-incdir` it first removes the csr include dir from run.sh's INCDIRS to
show the row can fail in the composed tree.
"""
import pathlib
import re
import runpy
import sys

mode = sys.argv[1] if len(sys.argv) > 1 else "pristine"
if mode == "drop-incdir":
    p = pathlib.Path("syn/yosys/run.sh")
    text = p.read_text()
    new, n = re.subn(r'\s*"\$R/hdl/common/csr"', "", text, count=1)
    assert n == 1, "mutation anchor not found exactly once"
    p.write_text(new)
sys.argv = ["test_builder.py"]
sys.path.insert(0, "sw/builder")
g = runpy.run_path("sw/builder/test_builder.py", run_name="probe")
try:
    g["test_csr_defaults_header_consumed"]()
except AssertionError as exc:
    print(f"GATE20A {mode}: REFUSED: {exc}")
    sys.exit(1)
print(f"GATE20A {mode}: PASS")
