#!/usr/bin/env python3
"""Round-3 reviewer mutants, run through the unchanged round-1 probe_mutants.py.

Loads probe_mutants.py as a module, replaces its REVIEWER list with the
round-3 set below, and calls its main() with the same arguments.

  R31: an asCapable RISE (recovery) arms the completion qualifier while the
       level is low; the loss itself does not.  Only a check that consumes
       in-band pairs after an inactive recovery can see it.
  R32: an inactive asCapable loss raises the level directly on the flags
       write (no pair consumed).  The incapable-interval checks must see it.
  R33: an inactive asCapable loss loads ONE remaining pair (predicted
       equivalent: an in-band pair decrements it to zero and publishes 0, an
       outside-band pair reloads anyway, and steps/mastership clear it; only
       the slew leg reads the qualifier).  Expected to survive.

Usage: PATH=<verilator dir>:$PATH python3 probe_r3.py --tree <tree> \
           --work <scratch> --set reviewer [--jobs N]
"""
import importlib.util
import sys
from pathlib import Path

HOOK = ("                if (phc_slew_active_o &&\n"
        "                    (!st_wdata_w[2] || !st_wdata_w[3]))\n"
        "                  phc_slew_left_r <= 2'd2;\n")

ROUND3 = [
    ("R31 inactive asCapable recovery arms qualification",
     "top/KL_gptp_engine.sv", HOOK,
     "                if ((phc_slew_active_o &&\n"
     "                    (!st_wdata_w[2] || !st_wdata_w[3])) ||\n"
     "                    (st_wdata_w[2] && !pub_flags_r[2]))\n"
     "                  phc_slew_left_r <= 2'd2;\n",
     "an inactive asCapable recovery must not arm a later in-band pair"),
    ("R32 inactive asCapable loss raises the level",
     "top/KL_gptp_engine.sv", HOOK,
     HOOK +
     "                else if (!st_wdata_w[2])\n"
     "                  phc_slew_active_o <= 1'b1;\n",
     "an inactive asCapable loss leaves the level low"),
    ("R33 inactive asCapable loss loads one pair",
     "top/KL_gptp_engine.sv", HOOK,
     HOOK +
     "                else if (!st_wdata_w[2])\n"
     "                  phc_slew_left_r <= 2'd1;\n",
     "predicted equivalent; expected to survive"),
]

spec = importlib.util.spec_from_file_location(
    "probe_mutants", Path(__file__).with_name("probe_mutants.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.REVIEWER = ROUND3
sys.exit(mod.main())
