#!/usr/bin/env bash
# #806: the full serial Yosys gate (Yosys 0.66, sv2v v0.0.12) in a clean clone at <rev>.
# usage: yosys_run.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/806-a701; C=$X/clone-yosys-${rev:0:8}; O=$X/r/yosys-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
cd "$C" || exit 2
source "$D/env.sh"
git rev-parse HEAD > "$O/head.txt"
yosys -V > "$O/versions.txt"; sv2v --version >> "$O/versions.txt"
s=$(date +%s); bash syn/yosys/run.sh --results "$X/yosys-results-${rev:0:8}" > "$O/run.log" 2>&1; echo $? > "$O/run.rc"
echo "$(( $(date +%s)-s ))s" > "$O/seconds.txt"
git status --porcelain --untracked-files=no > "$O/clone-status-after.txt"
echo YOSYS-DONE >> "$O/seconds.txt"
