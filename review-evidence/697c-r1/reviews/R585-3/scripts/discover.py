#!/usr/bin/env python3
"""Print what ctrl_configs derives at a checkout: modes, computed values, builders, C++ sources, and every
tracked C++ source under sw/ and tb/ that no builder names. Usage: discover.py <checkout>"""
import subprocess, sys
from pathlib import Path
co = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(co / "sw/firmware/ctrl/test")); sys.path.insert(0, str(co / "sw/firmware/gtest"))
import ctrl_configs as c
modes, computed = c.derive()
print("MODES", len(modes)); [print("  ", k, v) for k, v in modes.items()]
print("COMPUTED", computed)
print("BUILDERS"); [print("  ", c.rel(p)) for p in c.builder_texts()]
cx = sorted(c.rel(p) for p in c.cxx_sources())
print("CXX_SOURCES", len(cx)); [print("  ", p) for p in cx]
allcpp = subprocess.run(["git", "-C", str(co), "ls-files", "--", "sw/firmware/*.cpp", "tb/verilator/mbx/*.cpp"],
                        capture_output=True, text=True).stdout.split()
print("TRACKED .cpp under sw/firmware and tb/verilator/mbx NOT named by a builder:")
[print("  ", p) for p in allcpp if p not in cx]
