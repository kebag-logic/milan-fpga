#!/usr/bin/env python3
"""Run the Makefile arm of the sim-pool test with the two sidmove legs added to its list in memory.

No file is changed. Usage: sim_pool_arm_patched.py <tree-root>
"""
import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("sp", root / "tb/verilator/milan_dp/test_sim_pool.py")
sp = importlib.util.module_from_spec(spec)
sys.modules["sp"] = sp
spec.loader.exec_module(sp)
arm = sp.arm_the_makefile_hands_the_runner_the_recipes_ordinary_legs
try:
    arm()
    print("as committed: PASS")
except AssertionError as finding:
    print("as committed: FAIL", str(finding)[:90])
legs = list(sp.LEGACY_LEGS)
at = [k for k, leg in enumerate(legs) if leg[1].endswith("Vmilan_dp_tspec8")][0] + 1
legs[at:at] = [
    ("---- processor #202: the Stream ID move after a MAAP conflict on the wire, the shipping shape, "
     "TIMED on the crflic grid ----", "./obj_sidmove/Vmilan_dp_sidmove"),
    ("---- processor #202: the Stream ID move on the wire, two AAF talkers of the 8x8 shape, "
     "a TCTX uid named ----", "./obj_sidmove8/Vmilan_dp_sidmove8"),
]
sp.LEGACY_LEGS = tuple(legs)
try:
    arm()
    print("with the two sidmove rows: PASS")
except AssertionError as finding:
    print("with the two sidmove rows: FAIL", str(finding)[:300])
