#!/bin/bash
# One sweep suite again, alone, as run_all_suites.sh runs it (timeout at its suite_timeout, make -C, then
# suite_tally.py --verdict on its log), on a fresh clean clone at HEAD, with the sweep's environment.
# usage: rerun_suite.sh HEAD SUITE TIMEOUT_S
set -u
H=$1 SUITE=$2 TMO=$3 T=/data-2/milan/tmp/897-a776
C=$T/r4/rerun-$SUITE-${H:0:8} O=$T/r4/rerun-out-$SUITE-${H:0:8}
rm -rf "$C" "$O"; mkdir -p "$O" "$T/r4/tmp-rerun"
bash $T/scripts/clone.sh "$C" "$H" > "$O/clone.log" 2>&1 || exit 4
test "$(git -C "$C" rev-parse HEAD)" = "$H" || exit 4
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
export TMPDIR=$T/r4/tmp-rerun MAKEFLAGS="-j4 --no-print-directory"
cd "$C"
start=$(date +%s)
echo "HEAD $H suite $SUITE timeout $TMO start $(date +%T) cpus $(taskset -cp $$ | awk '{print $NF}')" > "$O/summary.txt"
timeout "$TMO" make -C "tb/verilator/$SUITE" > "$O/$SUITE.log" 2>&1; rc=$?
echo "make rc=$rc elapsed=$(( $(date +%s) - start ))s end $(date +%T)" >> "$O/summary.txt"
python3 scripts/suite_tally.py --verdict "$O/$SUITE.log" >> "$O/summary.txt" 2>&1; echo "verdict rc=$?" >> "$O/summary.txt"
git status --porcelain --untracked-files=no >> "$O/summary.txt"
exit $rc
