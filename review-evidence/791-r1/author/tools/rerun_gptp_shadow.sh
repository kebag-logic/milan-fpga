#!/usr/bin/env bash
# rerun_gptp_shadow.sh: the gptp_shadow suite once more (#833: a lifecycle cleanup failure is re-run once and both
# results recorded), as scripts/run_all_suites.sh runs a suite, in shard 1's clone at the same head and env.
S=/data-2/milan/tmp/791-a765; OUT=$S/sweep/shard-1-rerun; mkdir -p "$OUT" "$S/tmp-sweep"
cd $LANES/791-a765-shard1 || exit 2
git rev-parse HEAD > "$OUT/head.txt"
env PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator \
  TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c \
  TMPDIR=$S/tmp-sweep MAKEFLAGS="-j4 --no-print-directory" \
  timeout 3600 make -C tb/verilator/gptp_shadow > "$OUT/gptp_shadow.log" 2>&1
echo $? > "$OUT/gptp_shadow.rc"
