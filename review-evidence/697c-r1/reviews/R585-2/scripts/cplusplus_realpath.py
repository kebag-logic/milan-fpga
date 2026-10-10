#!/usr/bin/env python3
"""Real-path companion to probe n1: plant `#include "acmp_fake.hpp"` in the C++-only region of a copy of
sw/firmware/ctrl/adp/adp_mbx.h, then preprocess the firmware's own test test_adp.cpp exactly with the arms'
test include path (ctrl_build.includes + the stack's tests/, as ctrl_build.compile_tests gives it) and show
the header chain reaching the stack's tests/ through the firmware header; then the same header as C (the
only language the boundary gate preprocesses it in) reaches nothing of the stack outside include/.
Usage: cplusplus_realpath.py <checkout> <work>"""
import shutil, subprocess, sys
from pathlib import Path
checkout, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import ctrl_build as cb, fw_gtest  # noqa: E402
ctrl = work / "ctrl"
if ctrl.exists():
    shutil.rmtree(ctrl)
shutil.copytree(cb.CTRL, ctrl, ignore=shutil.ignore_patterns("__pycache__"))
h = ctrl / "adp/adp_mbx.h"
anchor = '#ifdef __cplusplus\nextern "C" {\n'
t = h.read_text()
assert t.count(anchor) == 1
h.write_text(t.replace(anchor, '#ifdef __cplusplus\n#include "acmp_fake.hpp"\nextern "C" {\n'))
tree = cb.Tree(ctrl, work / "out", work / "reuse")
inc = [*cb.includes(tree), f"-I{cb.STACK_TESTS}"]
cxx = ["g++", *fw_gtest.CXX_FLAGS, *inc, "-E", "-H", "-o", "/dev/null", str(cb.HERE / "test_adp.cpp")]
r = subprocess.run(cxx, capture_output=True, text=True)
chain = [ln for ln in r.stderr.splitlines() if "adp_mbx.h" in ln or "acmp_fake.hpp" in ln]
print("C++ (the arm's test compile of test_adp.cpp), rc", r.returncode)
print("\n".join(chain))
c = ["gcc", *cb.C_FLAGS, *inc, "-x", "c", "-E", "-H", "-o", "/dev/null", str(h)]
r2 = subprocess.run(c, capture_output=True, text=True)
print("C (the gate's language for the header), rc", r2.returncode, "reaches acmp_fake.hpp:", "acmp_fake.hpp" in r2.stderr)
print("RESULT:", "C++-ONLY ESCAPE DEMONSTRATED" if any("acmp_fake.hpp" in ln for ln in chain) and "acmp_fake.hpp" not in r2.stderr else "NOT DEMONSTRATED")
