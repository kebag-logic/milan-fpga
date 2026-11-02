#!/bin/bash
# rtl-fast's firmware-verilator boundary step on a clean clone of the head, with CI's --no-print-directory.
set -u
H=$1
S=$MANAGEMENT/2026-09-23/665s2b-a683o/scripts
W=$VALIDATION_STORAGE/665s2b-a683o/lane-wt2
[ -d "$W" ] || "$S/clone.sh" "$W" "$H" > /dev/null 2>&1
cd "$W" || exit 3
. "$S/env.sh"
export TMPDIR=$VALIDATION_STORAGE/665s2b-a683o/tmp-lane MAKEFLAGS="-j8 --no-print-directory"
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:$PATH VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
{ echo "# head $H gate boundary_b with --no-print-directory"; python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator; echo "rc=$?"; } > "$VALIDATION_STORAGE/665s2b-a683o/lane-logs/boundary_b2.log" 2>&1
