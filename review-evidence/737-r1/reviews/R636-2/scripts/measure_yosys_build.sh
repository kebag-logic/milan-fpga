#!/bin/sh
# Measure the cgroup memory peak of the workflow's Yosys source build recipe
# (config-gcc, the three Makefile.conf lines, make -jN) inside a bounded user scope.
# Usage: measure_yosys_build.sh <yosys-src> <jobs> <receipt-dir> [memory-max]
set -eu
src=$1; jobs=$2; out=$3; max=${4:-11G}
mkdir -p "$out"
g++ --version | head -1 > "$out/compiler.txt"
git -C "$src" rev-parse HEAD > "$out/source-head.txt"
systemd-run --user --scope --quiet -p MemoryMax="$max" -p MemorySwapMax=0 sh -c '
  cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
  src=$1; jobs=$2; out=$3
  start=$(date +%s)
  make -C "$src" config-gcc >"$out/build.log" 2>&1 &&
  printf "ENABLE_TCL := 0\nENABLE_READLINE := 0\nENABLE_PLUGINS := 0\n" >> "$src/Makefile.conf" &&
  make -C "$src" -j"$jobs" PREFIX="$out/prefix-unused" >>"$out/build.log" 2>&1
  rc=$?
  echo $rc > "$out/rc"
  echo $(( $(date +%s) - start )) > "$out/seconds"
  cat "$cg/memory.peak" > "$out/memory.peak"
  cat "$cg/memory.events" > "$out/memory.events"
  nproc > "$out/nproc"
' sh "$src" "$jobs" "$out"
printf 'rc=%s seconds=%s peak_bytes=%s\n' "$(cat "$out/rc")" "$(cat "$out/seconds")" "$(cat "$out/memory.peak")"
cat "$out/memory.events"
