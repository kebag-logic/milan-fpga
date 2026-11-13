#!/bin/sh
# Run the engine arm at the exact head, --jobs 8, ccache on with an empty
# cache under scratch; record stdout, stderr, rc, wall and ccache stats.
. $REVIEWS/gptp104-r840-1-packet/scripts/env.sh
out=$P/receipts/fullarm
export CCACHE_DIR=$S/cc/fullarm
rm -rf "$CCACHE_DIR"; mkdir -p "$CCACHE_DIR"
cd $S/trees/head/tb/verilator/engine || exit 9
start=$(date +%s)
python3 mutants.py --jobs 8 > $out/head-jobs8-cold.stdout 2> $out/head-jobs8-cold.stderr
echo "rc=$?" > $out/head-jobs8-cold.rc
echo "wall_s=$(( $(date +%s) - start ))" >> $out/head-jobs8-cold.rc
ccache --print-stats > $out/head-jobs8-cold.ccache-stats
