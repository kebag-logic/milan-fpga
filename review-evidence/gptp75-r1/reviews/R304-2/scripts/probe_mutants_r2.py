#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R304-2 extra probes: reuse the unchanged round-1 driver (scripts/round1/
probe_mutants.py) with a round-2 reviewer list aimed at the inactive direction
of the lifecycle contract beyond the two round-1 gaps.

usage: probe_mutants_r2.py TREE WORKDIR OUTDIR [--jobs N] [--only I,J]
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "probe_mutants", HERE / "round1" / "probe_mutants.py")
pm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pm)

RTL, GEN = pm.RTL, pm.GEN
HOOK = ("                if (phc_slew_active_o &&\n"
        "                    (!st_wdata_w[2] || !st_wdata_w[3]))\n")
pm.REVIEWER = [
    ("X01 asCapable loss arms while inactive", RTL, HOOK,
     "                if ((phc_slew_active_o && !st_wdata_w[3]) ||\n"
     "                    !st_wdata_w[2])\n",
     "an inactive asCapable lapse cannot turn tracking into a slew"),
    ("X02 sync-ok lapse arms while inactive only", RTL, HOOK,
     "                if ((phc_slew_active_o && !st_wdata_w[2]) ||\n"
     "                    !st_wdata_w[3])\n",
     "an inactive Sync lapse / GM change cannot arm qualification"),
    ("X03 idle lapse arms one pair", RTL,
     HOOK + "                  phc_slew_left_r <= 2'd2;\n",
     "                if (!st_wdata_w[2] || !st_wdata_w[3])\n"
     "                  phc_slew_left_r <= phc_slew_active_o ? 2'd2 : 2'd1;\n",
     "an idle lapse cannot arm even a single-pair qualification"),
    ("X04 step arms qualification", RTL,
     "                //! Keep an existing level until the step's rate tail.\n"
     "                phc_slew_left_r <= 2'd0;\n",
     "                //! Keep an existing level until the step's rate tail.\n"
     "                phc_slew_left_r <= 2'd2;\n",
     "a step never asserts the level"),
    ("X05 mastership arms qualification", RTL,
     "                phc_slew_left_r   <= 2'd0;\n"
     "                phc_slew_active_o <= 1'b0;\n",
     "                phc_slew_left_r   <= 2'd2;\n"
     "                phc_slew_active_o <= 1'b0;\n",
     "return to slave duty starts a fresh decision"),
]

if __name__ == "__main__":
    argv = sys.argv[1:4] + ["reviewer"] + sys.argv[4:]
    sys.argv = [sys.argv[0]] + argv
    sys.exit(pm.main())
