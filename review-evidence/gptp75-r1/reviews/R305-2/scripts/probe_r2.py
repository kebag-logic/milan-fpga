#!/usr/bin/env python3
"""Round-2 reviewer mutants, run through the unchanged round-1 probe_mutants.py.

Loads probe_mutants.py as a module, replaces its REVIEWER list with the
round-2 set below, and calls its main() with the same arguments. The
round-1 script bytes are not edited.

  R21: the lapse hook's asCapable term fires even while inactive; the sync-ok
       term keeps its phc_slew_active_o guard.
  R22: the lapse hook's sync-ok term fires even while inactive; the asCapable
       term keeps its guard (the mirror image of R21, a control that the
       round-2 idle Sync-timeout arm must catch).

Usage: PATH=<verilator dir>:$PATH python3 probe_r2.py --tree <tree> \
           --work <scratch> --set reviewer [--jobs N]
"""
import importlib.util
import sys
from pathlib import Path

GUARD = ("                if (phc_slew_active_o &&\n"
         "                    (!st_wdata_w[2] || !st_wdata_w[3]))")

ROUND2 = [
    ("R21 asCapable lapse arms qualification while inactive",
     "top/KL_gptp_engine.sv", GUARD,
     "                if ((phc_slew_active_o && !st_wdata_w[3]) ||\n"
     "                    !st_wdata_w[2])",
     "an inactive asCapable loss must not arm a later in-band pair"),
    ("R22 sync-ok lapse arms qualification while inactive",
     "top/KL_gptp_engine.sv", GUARD,
     "                if ((phc_slew_active_o && !st_wdata_w[2]) ||\n"
     "                    !st_wdata_w[3])",
     "an inactive Sync lapse must not arm a later in-band pair"),
]

spec = importlib.util.spec_from_file_location(
    "probe_mutants", Path(__file__).with_name("probe_mutants.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.REVIEWER = ROUND2
sys.exit(mod.main())
