#!/usr/bin/env python3
"""Elaborate and compile the obj_nxn recipe against a shape with no CRF sink.

No tracked config disables clocking.crf_sink, so no milan_dp leg elaborates the
datapath's no-CRF branches (g_ctr_no_crf_dirty, the constant-false ctr_crf_w). This
takes the suite's own obj_nxn recipe, swaps only the shape include directory for a
builder-generated one, and builds it (the harness is not run: it assumes the CRF
sink). Exit status is the simulator's build status.

usage: nocrf_elab.py TREE SHAPE_GEN_PARENT MDIR LOG
  SHAPE_GEN_PARENT is the directory holding gen/adp_shape_defaults.svh.
Environment: VERILATOR names the simulator executable.
"""
import os
import subprocess
import sys


def main():
    tree, shape, mdir, log = sys.argv[1:5]
    verilator = os.environ.get("VERILATOR", "verilator")
    suite = os.path.join(tree, "tb", "verilator", "milan_dp")
    out = subprocess.run(["make", "-n", "run", f"VERILATOR={verilator}", "VERILATOR_JOBS=4"],
                         cwd=suite, capture_output=True, text=True, check=True).stdout
    hits = [ln for ln in out.replace("\\\n", " ").splitlines()
            if "--Mdir obj_nxn " in ln and ln.rstrip().endswith("-o Vmilan_dp_nxn")]
    assert len(hits) == 1, hits
    cmd = hits[0]
    old_inc = "+incdir+../../../configs/generated/endstation_arty_4x4 "
    assert cmd.count(old_inc) == 1
    cmd = cmd.replace(old_inc, f"+incdir+{os.path.abspath(shape)} ", 1)
    cmd = cmd.replace("--Mdir obj_nxn ", f"--Mdir {os.path.abspath(mdir)} ", 1)
    # elaboration only: the harness C++ names CRF tally wires that a no-CRF model
    # optimises away, so it is not compiled
    head = "--cc --exe --build -j 4 "
    assert cmd.count(head) == 1 and cmd.rstrip().endswith(" sim_nxn.cpp -o Vmilan_dp_nxn")
    cmd = cmd.replace(head, "--lint-only ", 1)
    cmd = cmd.rstrip()[: -len(" sim_nxn.cpp -o Vmilan_dp_nxn")]
    cmd = cmd.replace(' -CFLAGS "-std=c++17 -O2 -Wall -Wextra"', "", 1)
    os.makedirs(mdir, exist_ok=True)
    with open(log, "w") as f:
        f.write(f"shape_include={os.path.basename(os.path.abspath(shape))}\n")
        f.flush()
        rc = subprocess.run(cmd, shell=True, cwd=suite, stdout=f,
                            stderr=subprocess.STDOUT).returncode
        f.write(f"\nbuild_exit={rc}\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
