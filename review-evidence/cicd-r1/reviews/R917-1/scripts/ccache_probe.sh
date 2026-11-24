#!/bin/bash
# ccache_probe.sh TREE OUT CPUS
# crf_rx's mutant campaign at TREE through OBJCACHE=ccache, cold then warm, with a
# private cache directory (never the user's shared cache), for comparison with the
# same campaign's output in the no-ccache whole-suite log.
set -u
TREE=$1 OUT=$2 CPUS=$3
HERE=$(cd "$(dirname "$0")" && pwd)
export VERILATOR="$HERE/vwrap.sh" VW_JOBS=2 VERILATOR_JOBS=2 MAKEFLAGS='-j1 --no-print-directory'
export OBJCACHE=ccache CCACHE_DIR="$OUT/ccache_dir" CCACHE_TEMPDIR="$OUT/ccache_tmp"
mkdir -p "$OUT" "$CCACHE_DIR" "$CCACHE_TEMPDIR"
ccache -z > /dev/null
for pass in cold warm; do
  /usr/bin/time -f '%e s wall %U s user %S s sys' -o "$OUT/$pass.time" \
    taskset -c "$CPUS" make -C "$TREE/tb/verilator/crf_rx" mutants > "$OUT/$pass.log" 2>&1
  echo "rc=$?" >> "$OUT/$pass.log"
  ccache -s -v > "$OUT/$pass.stats" 2>&1
done
echo done > "$OUT/DONE"
