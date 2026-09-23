#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Disposable counterfactual: rescript the parent gptp_shadow closed-loop
phase (parent dev 574c29fa, check_sync_offset_and_closed_loop_lock) so its
phase jump is one the recorded FPGA-gPTP #68 policy steps. Instead of a 1 ms
master jump against a SYNCHRONIZED servo (which #68 slews), the phase first
lets the 375 ms Sync receipt timeout clear sync-ok, then presents a master
1.5 s ahead: a first synchronization over one second. Nothing else in the
suite changes. If both failing checks pass under this rescript, they encoded
the retired step policy and are not donor defects.
Usage: counterfactual_first_sync_loop.py <sim_main.cpp> (in place, scratch copy only)."""

import pathlib
import sys

OLD = ("      uint64_t mst_base = phc() + 1000000ull - cyc * 8ull - cyc / 1250ull;\n")
NEW = ("      // COUNTERFACTUAL: let sync-ok fall (375 ms receipt timeout), then\n"
       "      // present a first synchronization 1.5 s off, which #68 steps\n"
       "      for (int w = 0; w < 4000 && (dut->pub_flags_o & FL_SYNCOK); w++)\n"
       "        run_svc(1000);\n"
       "      expect(\"counterfactual: sync-ok fell before the loop\",\n"
       "             dut->pub_flags_o & FL_SYNCOK, 0);\n"
       "      uint64_t mst_base = phc() + 1500000000ull - cyc * 8ull - cyc / 1250ull;\n")


def main() -> None:
    """Apply the rescript to the file named on the command line."""
    path = pathlib.Path(sys.argv[1])
    src = path.read_text()
    if src.count(OLD) != 1:
        raise SystemExit("counterfactual anchor not unique/absent")
    path.write_text(src.replace(OLD, NEW))


if __name__ == "__main__":
    main()
