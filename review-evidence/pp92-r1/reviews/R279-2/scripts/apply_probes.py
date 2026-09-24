#!/usr/bin/env python3
"""Splice the reviewer probes into a scratch copy of tb/acmp_nvm/sim_main.cpp.

usage: apply_probes.py <scratch tree root> <probe cases .cpp>
Adds a Harness::check_r279() declaration and definition and, when the
environment variable R279_ONLY is set at run time, runs only the probes.
Operates only on the given scratch tree; never on the review clone.
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
cases = pathlib.Path(sys.argv[2]).read_text()
f = root / "tb/acmp_nvm/sim_main.cpp"
s = f.read_text()
decl = "  void check_n9_an_unwired_device_face();\n"
assert s.count(decl) == 1
s = s.replace(decl, decl + "  void check_r279();\n")
anchor = "int Harness::report() {"
assert s.count(anchor) == 1
s = s.replace(anchor, cases + "\n" + anchor)
run = "int Harness::run_suite() {\n"
assert s.count(run) == 1
s = s.replace(run, run + "  if (getenv(\"R279_ONLY\")) { check_r279(); return report(); }\n")
if "#include <cstdlib>" not in s:
    s = s.replace("#include <cstdint>", "#include <cstdint>\n#include <cstdlib>", 1)
f.write_text(s)
print("spliced", f)
