#!/bin/sh
# Run one mutation driver in an exported tree, recording its transcript, wall
# time, exit status and ccache statistics.
#   run_driver.sh TREE SUITE DRIVER OUTDIR TMPROOT CCACHEDIR LABEL
# The pinned simulator wrapper's directory must be first on PATH.
set -u
tree=$1 suite=$2 driver=$3 out=$4 tmproot=$5 cdir=$6 label=$7
mkdir -p "$out" "$tmproot" "$cdir"
name="$suite-$(basename "$driver" .py)-$label"
export TMPDIR="$tmproot" CCACHE_DIR="$cdir" OBJCACHE=ccache
export VERILATOR_JOBS=1 SIM_JOBS=1 MAKEFLAGS='-j1 --no-print-directory'
ccache -z >/dev/null 2>&1
start=$(date +%s)
( cd "$tree/tb/verilator/$suite" && timeout 5400 python3 "$driver" ) > "$out/$name.log" 2>&1
rc=$?
end=$(date +%s)
echo "rc=$rc wall=$((end - start))" > "$out/$name.rc"
ccache --print-stats 2>/dev/null | grep -E '^(direct_cache_hit|preprocessed_cache_hit|cache_miss|called_for_link|compiler_check_failed)' > "$out/$name.stats"
