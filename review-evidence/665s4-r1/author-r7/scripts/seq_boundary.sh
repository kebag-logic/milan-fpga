#!/bin/sh
# The firmware boundary gate, both modes, on one clean clone, as rtl-fast and firmware-verilator run it.
J="$MANAGEMENT/2026-09-23/665s4-a698h/scripts/job.sh"; C=$VALIDATION_STORAGE/scratch/665s4-a698h/wt-bnd
$J firmware_boundary $C python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
$J firmware_boundary_verilator $C python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
git -C $C status --porcelain --untracked-files=all --ignore-submodules=none > $VALIDATION_STORAGE/scratch/665s4-a698h/wt-bnd.status-after
