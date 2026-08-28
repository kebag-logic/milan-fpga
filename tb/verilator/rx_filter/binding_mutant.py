#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove the rx_filter harness rejects a tied-off production binding.

The Makefile first runs the unmodified filter as a positive control. This arm
then replaces the real named TCAM lookup connection with a constant zero,
builds the same RTL boundary, and runs the same harness. Success means the
harness returns nonzero with its own FAIL verdict; a build failure does not
count because it would not prove the behavioral seam is observed.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILTER = HERE / "../../../hdl/ieee8021q/filtering/rx_mac_filter.sv"
TCAM = HERE / "../../../hdl/ieee8021q/filtering/tcam.sv"
HARNESS = HERE / "sim_main.cpp"
BINDING = ".lookup_key_i(dmac),"
TIED_OFF = ".lookup_key_i(48'b0),"

VFLAGS = [
    "--cc", "--exe", "--build", "-j", "0", "--top-module", "rx_mac_filter",
    "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL",
    "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM",
    "-Wno-PINCONNECTEMPTY", "-CFLAGS", "-std=c++17 -O2",
]


def main():
    source = FILTER.read_text()
    if source.count(BINDING) != 1:
        print("[FAIL] the named TCAM lookup binding was not found exactly once")
        print("1 checks: 0 PASS, 1 FAIL")
        return 1

    with tempfile.TemporaryDirectory(prefix="rx-filter-binding-") as tmp:
        work = Path(tmp)
        mutant = work / "rx_mac_filter.sv"
        mutant.write_text(source.replace(BINDING, TIED_OFF))
        obj = work / "obj_binding"
        exe_name = "Vrx_filter_tied_lookup"
        build = subprocess.run(
            ["verilator", *VFLAGS, "--Mdir", str(obj), str(TCAM),
             str(mutant), str(HARNESS), "-o", exe_name],
            capture_output=True, text=True)
        if build.returncode != 0:
            print("[FAIL] tied-off binding did not compile, so the behavioral "
                  "seam was not exercised")
            print(build.stderr[-800:])
            print("1 checks: 0 PASS, 1 FAIL")
            return 1

        run = subprocess.run([str(obj / exe_name)], capture_output=True, text=True)
        if run.returncode != 0 and "RESULT: FAIL" in run.stdout:
            print("[PASS] the real harness rejected a TCAM lookup tied to zero")
            print("1 checks: 1 PASS, 0 FAIL")
            return 0

        print("[FAIL] the real harness accepted a TCAM lookup tied to zero")
        if run.stdout:
            print(run.stdout[-800:])
        if run.stderr:
            print(run.stderr[-800:])
        print("1 checks: 0 PASS, 1 FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())
