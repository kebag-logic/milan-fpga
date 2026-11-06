#!/usr/bin/env python3
"""Run the sim-pool backpressure test with the two sidmove legs added to the shared list in memory.

No file is changed. Usage: backpressure_patched.py <tree-root>
"""
import runpy
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
here = root / "tb/verilator/milan_dp"
sys.path.insert(0, str(here))
import test_sim_pool as sp  # noqa: E402

legs = list(sp.LEGACY_LEGS)
at = [k for k, leg in enumerate(legs) if leg[1].endswith("Vmilan_dp_tspec8")][0] + 1
legs[at:at] = [
    ("---- processor #202: the Stream ID move after a MAAP conflict on the wire, the shipping shape, "
     "TIMED on the crflic grid ----", "./obj_sidmove/Vmilan_dp_sidmove"),
    ("---- processor #202: the Stream ID move on the wire, two AAF talkers of the 8x8 shape, "
     "a TCTX uid named ----", "./obj_sidmove8/Vmilan_dp_sidmove8"),
]
sp.LEGACY_LEGS = tuple(legs)
sys.argv = [str(here / "test_sim_pool_backpressure.py")]
runpy.run_path(sys.argv[0], run_name="__main__")
