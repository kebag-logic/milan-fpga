#!/usr/bin/env bash
set -u
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export HOME=$WORKSPACE_HOME VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$VALIDATION_STORAGE/839-a731b/gates/tmp TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c MAKEFLAGS="-j4 --no-print-directory"
cd $VALIDATION_STORAGE/839-a731b/gates/mut-wt-ba56827b/tb/verilator/milan_dp
echo "# head $(git rev-parse HEAD): make bootsa-build, then keep_mutant_logs.py for controls 7 to 11"
make bootsa-build > $VALIDATION_STORAGE/839-a731b/mutant-receipts-prereq-ba56827b.log 2>&1; echo "prerequisite build rc=$?"
python3 -I $MANAGEMENT/2026-09-23/839-a731b/receipts/gates/tools/keep_mutant_logs.py . $VALIDATION_STORAGE/839-a731b/mutant-work-ba56827b $VALIDATION_STORAGE/839-a731b/mutant-runs-ba56827b 2 7 8 9 10 11
echo "rc=$?"
git status --porcelain --ignored=no > $VALIDATION_STORAGE/839-a731b/mutant-runs-ba56827b/tree-after.txt
