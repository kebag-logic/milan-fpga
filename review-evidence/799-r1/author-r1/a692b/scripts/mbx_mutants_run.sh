#!/usr/bin/env bash
# #799: the mbx suite and its full mutant campaign (tb/verilator/mbx: make, make run-if2, make mutants) in the clean
# static clone at <rev>, run from inside the suite directory.
# usage: mbx_mutants_run.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/799-a692b; C=$X/clone-static-${rev:0:8}; O=$X/r/mbx-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
cd "$C/tb/verilator/mbx" || exit 2
source "$D/env.sh"
git -C "$C" rev-parse HEAD > "$O/head.txt"
s=$(date +%s); make > "$O/make.log" 2>&1; echo "$? $(( $(date +%s)-s ))s make" > "$O/table.txt"
s=$(date +%s); make run-if2 > "$O/run-if2.log" 2>&1; echo "$? $(( $(date +%s)-s ))s make run-if2" >> "$O/table.txt"
s=$(date +%s); make mutants > "$O/mutants.log" 2>&1; echo "$? $(( $(date +%s)-s ))s make mutants" >> "$O/table.txt"
git -C "$C" status --porcelain --untracked-files=no > "$O/clone-status-after.txt"
echo MBX-DONE >> "$O/table.txt"
