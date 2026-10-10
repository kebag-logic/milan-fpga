#!/usr/bin/env python3
"""R584-3: the firmware units the gate judges as C++ too. Run from <checkout>/sw/firmware/ctrl/test."""
import sys, tempfile
from pathlib import Path
sys.path.insert(0, "../../gtest")
import ctrl_boundary as b
u, f = b.cxx_units(b.Trees(b.CTRL, b.STACK), Path(tempfile.mkdtemp()))
allu = b.firmware_units(b.Trees(b.CTRL, b.STACK))
print("CXX", len(u), "of", len(allu)); [print("  C++", p.relative_to(b.CTRL)) for p in u]
print("NOT-C++:"); [print("  ", p.relative_to(b.CTRL)) for p in allu if p not in u]
print("unfollowed", f)
