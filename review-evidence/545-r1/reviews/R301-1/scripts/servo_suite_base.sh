#!/usr/bin/env bash
# Runtime comparison: the mmcm_servo default target at the BASE commit,
# extracted into scratch and run with the same pinned simulator.
set -u
REPO=${REPO:-$REVIEWS/r301-1-545}
PKT=${PKT:-$REVIEWS/545-r301-1-packet}
BASE=5b73d3f47dfed519eb988c13d6beb1db664ef1e0
VERILATOR=${VERILATOR:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator}
T="$PKT/scratch/tree_base"
rm -rf "$T"; mkdir -p "$T"
git -C "$REPO" archive "$BASE" hdl tb/common tb/verilator/mmcm_servo | tar -x -C "$T"
grep -n "^all:" "$T/tb/verilator/mmcm_servo/Makefile"
make -C "$T/tb/verilator/mmcm_servo" VERILATOR="$VERILATOR" 2>&1
