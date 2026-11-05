#!/usr/bin/env bash
# The scheduled physical gPTP suite (tb/verilator/milan_dp_gptp) on a clean clone.
# Usage: physical_gptp.sh <clone> <log>
set -u
cd "$1" || exit 2
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator MAKEFLAGS="-j4 --no-print-directory" TMPDIR=$VALIDATION_STORAGE/840-a732/tmp-phys
mkdir -p "$TMPDIR"
{ echo "# head $(git rev-parse HEAD) gate: make -C tb/verilator/milan_dp_gptp"; make -C tb/verilator/milan_dp_gptp; } > "$2" 2>&1
rc=$?; echo "$rc" > "$2.rc"
git status --porcelain --untracked-files=no > "$2.tree-after"
