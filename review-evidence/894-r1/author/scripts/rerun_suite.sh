#!/bin/bash
# One Verilator suite the sweep's wall clock killed, run again as scripts/run_all_suites.sh runs it (its make, then
# suite_tally.py --verdict on its log), in the shard's own clone at the head, with the sweep's environment and a wall
# clock of SECONDS. usage: rerun_suite.sh CLONE SUITE SECONDS OUTDIR
set -u
C=$1 S=$2 TMO=$3 O=$4
mkdir -p "$O" /data-2/milan/tmp/894-a773/tmp/rerun-$S
cd "$C" || exit 3
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l) suite $S wall clock $TMO s start $(date +%FT%T)" > "$O/$S.head"
env PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
    VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c \
    TMPDIR=/data-2/milan/tmp/894-a773/tmp/rerun-$S MAKEFLAGS="-j4 --no-print-directory" \
    timeout "$TMO" make -C "tb/verilator/$S" > "$O/$S.log" 2>&1
rc=$?
verdict=$(python3 scripts/suite_tally.py --verdict "$O/$S.log" 2>&1); vrc=$?
echo "make rc=$rc verdict rc=$vrc $verdict end $(date +%FT%T)" >> "$O/$S.head"
[ $rc -eq 0 ] && [ $vrc -eq 0 ]
